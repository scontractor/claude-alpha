import streamlit as st

from app import config, ingestor, retriever, generator

st.set_page_config(page_title="Knowledge Base", layout="wide")


# --- Session state ---
if "embed_model" not in st.session_state:
    with st.spinner("Loading embedding model..."):
        st.session_state.embed_model = ingestor.load_embedding_model()

if "chroma_client" not in st.session_state:
    st.session_state.chroma_client = ingestor.get_client()

if "collection" not in st.session_state:
    st.session_state.collection = ingestor.get_collection(st.session_state.chroma_client)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

embed_model = st.session_state.embed_model
collection = st.session_state.collection


# --- Sidebar ---
with st.sidebar:
    st.title("Knowledge Base")
    st.markdown(f"**Collection:** `{config.COLLECTION_NAME}`")
    chunk_count_placeholder = st.empty()
    chunk_count_placeholder.metric("Chunks stored", collection.count())

    st.divider()

    # --- Upload files ---
    st.markdown("### Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload files",
        type=[ext.lstrip(".") for ext in config.SUPPORTED_EXTENSIONS],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )
    if uploaded_files and st.button("Ingest Uploaded Files", use_container_width=True):
        with st.spinner("Ingesting..."):
            results = {}
            for f in uploaded_files:
                count = ingestor.ingest_from_bytes(f.name, f.read(), collection, embed_model)
                results[f.name] = count
        st.success(f"Ingested {len(results)} file(s)")
        for fname, count in results.items():
            st.write(f"- **{fname}**: {count} chunks")
        chunk_count_placeholder.metric("Chunks stored", collection.count())

    st.divider()

    # --- Ingest from data/ folder ---
    st.markdown("### Ingest from `data/` Folder")
    st.caption(f"Supported: `{', '.join(sorted(config.SUPPORTED_EXTENSIONS))}`")
    if st.button("Ingest from data/", use_container_width=True):
        with st.spinner("Ingesting..."):
            results = ingestor.ingest_all(config.DATA_DIR, collection, embed_model)
        if results:
            st.success(f"Ingested {len(results)} file(s)")
            for fname, count in results.items():
                st.write(f"- **{fname}**: {count} chunks")
            chunk_count_placeholder.metric("Chunks stored", collection.count())
        else:
            st.warning("No supported files found in `data/`.")

    st.divider()

    # --- Manage documents ---
    st.markdown("### Manage Documents")
    sources = ingestor.list_sources(collection)
    if not sources:
        st.caption("No documents ingested yet.")
    else:
        for source in sources:
            col1, col2 = st.columns([4, 1])
            col1.markdown(f"`{source}`")
            if col2.button("✕", key=f"del_{source}", help=f"Delete {source}"):
                deleted = ingestor.delete_file(source, collection)
                st.success(f"Deleted **{source}** ({deleted} chunks)")
                chunk_count_placeholder.metric("Chunks stored", collection.count())
                st.rerun()

    st.divider()
    st.caption(f"Model: `{config.EMBED_MODEL}`\n\nLLM: `{config.OLLAMA_MODEL}`")


# --- Main panel ---
st.title("Personal Knowledge Base")

search_tab, ask_tab = st.tabs(["Search", "Ask"])


# --- Search tab ---
with search_tab:
    query = st.text_input("Search your knowledge base", placeholder="What do you want to find?")
    if st.button("Search", key="search_btn") and query:
        if collection.count() == 0:
            st.warning("No documents ingested yet.")
        else:
            with st.spinner("Searching..."):
                hits = retriever.search(query, collection, embed_model)
            if hits:
                st.markdown(f"**{len(hits)} results:**")
                for i, hit in enumerate(hits, 1):
                    with st.expander(f"#{i} — {hit['source']} ({hit['similarity']}% match)"):
                        st.markdown(hit["text"])
            else:
                st.info("No results found.")


# --- Ask tab ---
with ask_tab:
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Clear chat button
    if st.session_state.chat_history:
        if st.button("Clear conversation", key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()

    # Input
    question = st.chat_input("Ask anything about your documents...")
    if question:
        if collection.count() == 0:
            st.warning("No documents ingested yet.")
        else:
            # Show and store user message
            with st.chat_message("user"):
                st.markdown(question)
            st.session_state.chat_history.append({"role": "user", "content": question})

            # Retrieve context
            hits = retriever.search(question, collection, embed_model)

            if not hits:
                response = "No relevant context found in your knowledge base."
                with st.chat_message("assistant"):
                    st.markdown(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
            else:
                with st.expander("Sources used", expanded=False):
                    for hit in hits:
                        st.markdown(f"**{hit['source']}** ({hit['similarity']}% match)")
                        st.caption(hit["text"][:300] + "..." if len(hit["text"]) > 300 else hit["text"])
                        st.divider()

                # Stream response and capture it
                full_response = ""
                with st.chat_message("assistant"):
                    placeholder = st.empty()
                    for chunk in generator.generate(question, hits):
                        full_response += chunk
                        placeholder.markdown(full_response)

                st.session_state.chat_history.append({"role": "assistant", "content": full_response})
