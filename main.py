import streamlit as st

from app import config, ingestor, retriever, generator

st.set_page_config(page_title="Knowledge Base", layout="wide")


# --- Session state: cache heavy objects ---
if "embed_model" not in st.session_state:
    with st.spinner("Loading embedding model..."):
        st.session_state.embed_model = ingestor.load_embedding_model()

if "collection" not in st.session_state:
    client = ingestor.get_client()
    st.session_state.collection = ingestor.get_collection(client)

embed_model = st.session_state.embed_model
collection = st.session_state.collection


# --- Sidebar ---
with st.sidebar:
    st.title("Knowledge Base")
    st.markdown(f"**Collection:** `{config.COLLECTION_NAME}`")

    chunk_count = collection.count()
    st.metric("Chunks stored", chunk_count)

    st.divider()
    st.markdown("### Ingest Documents")
    st.markdown(f"Drop files into the `data/` folder, then click below.")
    st.markdown(f"Supported: `{', '.join(sorted(config.SUPPORTED_EXTENSIONS))}`")

    if st.button("Ingest Documents", use_container_width=True):
        with st.spinner("Ingesting..."):
            results = ingestor.ingest_all(config.DATA_DIR, collection, embed_model)
        if results:
            st.success(f"Ingested {len(results)} file(s)")
            for fname, count in results.items():
                st.write(f"- **{fname}**: {count} chunks")
            st.metric("Chunks stored", collection.count())
        else:
            st.warning("No supported files found in `data/`.")

    st.divider()
    st.caption(
        f"Model: `{config.EMBED_MODEL}`\n\nLLM: `{config.OLLAMA_MODEL}`"
    )


# --- Main panel ---
st.title("Personal Knowledge Base")

search_tab, ask_tab = st.tabs(["Search", "Ask"])


# --- Search tab ---
with search_tab:
    query = st.text_input("Search your knowledge base", placeholder="What do you want to find?")
    if st.button("Search", key="search_btn") and query:
        if collection.count() == 0:
            st.warning("No documents ingested yet. Add files to `data/` and click Ingest.")
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
    question = st.text_area("Ask a question", placeholder="Ask anything about your documents...")
    if st.button("Ask", key="ask_btn") and question:
        if collection.count() == 0:
            st.warning("No documents ingested yet. Add files to `data/` and click Ingest.")
        else:
            with st.spinner("Retrieving context..."):
                hits = retriever.search(question, collection, embed_model)

            if not hits:
                st.info("No relevant context found.")
            else:
                with st.expander("Sources used", expanded=False):
                    for hit in hits:
                        st.markdown(f"**{hit['source']}** ({hit['similarity']}% match)")
                        st.caption(hit["text"][:300] + "..." if len(hit["text"]) > 300 else hit["text"])
                        st.divider()

                st.markdown("**Answer:**")
                st.write_stream(generator.generate(question, hits))
