import streamlit as st

from app import config, ingestor, retriever, generator

st.set_page_config(
    page_title="Knowledge Base",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Inject modern CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

#MainMenu, footer { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

.stApp { background: #0d1117; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #161b22 !important;
    border-right: 1px solid #21262d !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #238636, #2ea043) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.4) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px rgba(35,134,54,0.45) !important;
    background: linear-gradient(135deg, #2ea043, #3fb950) !important;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background: #161b22 !important;
    border: 1px solid #21262d !important;
    border-radius: 12px !important;
    margin: 6px 0 !important;
}

/* Chat input */
[data-testid="stChatInput"] textarea {
    background: #161b22 !important;
    color: #e6edf3 !important;
    border-color: #30363d !important;
}

/* Text input */
.stTextInput > div > div > input {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    color: #e6edf3 !important;
    font-size: 14px !important;
}
.stTextInput > div > div > input:focus {
    border-color: #58a6ff !important;
    box-shadow: 0 0 0 3px rgba(88,166,255,0.1) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid #21262d !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    color: #8b949e !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    padding: 0.75rem 1.5rem !important;
    border-radius: 0 !important;
}
.stTabs [aria-selected="true"] {
    color: #e6edf3 !important;
    border-bottom: 2px solid #58a6ff !important;
    background: transparent !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background: #161b22 !important;
    border: 1px solid #21262d !important;
    border-radius: 10px !important;
    padding: 1rem !important;
}
[data-testid="stMetricValue"] {
    color: #58a6ff !important;
    font-weight: 700 !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: #161b22 !important;
    border: 1px dashed #30363d !important;
    border-radius: 10px !important;
}

/* Expander */
[data-testid="stExpander"] {
    background: #161b22 !important;
    border: 1px solid #21262d !important;
    border-radius: 10px !important;
}

/* Alerts */
[data-testid="stAlert"] { border-radius: 8px !important; }

/* Typography */
h1 { color: #e6edf3 !important; font-weight: 700 !important; letter-spacing: -0.5px !important; }
h2, h3 { color: #c9d1d9 !important; font-weight: 600 !important; }
p, li, label { color: #c9d1d9 !important; line-height: 1.6 !important; }
hr { border-color: #21262d !important; }
code { background: #1f2937 !important; color: #79c0ff !important; border-radius: 4px !important; padding: 2px 6px !important; }

/* Citation styles */
.citations-block {
    margin-top: 14px;
    padding: 12px 16px;
    background: #0d1117;
    border: 1px solid #21262d;
    border-radius: 10px;
}
.citations-label {
    font-size: 11px;
    font-weight: 600;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 8px;
}
.citation-row {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 5px 0;
    border-bottom: 1px solid #161b22;
}
.citation-row:last-child { border-bottom: none; }
.ref-badge {
    background: #1f6feb;
    color: #fff;
    border-radius: 5px;
    padding: 1px 7px;
    font-size: 11px;
    font-weight: 700;
    min-width: 24px;
    text-align: center;
}
.ref-source { color: #c9d1d9; font-size: 13px; flex: 1; }
.ref-match { color: #3fb950; font-size: 12px; font-weight: 500; }

/* Search result cards */
.result-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 10px;
    padding: 14px 18px;
    margin: 8px 0;
    transition: border-color 0.2s;
}
.result-card:hover { border-color: #58a6ff; }
.result-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}
.result-source { color: #58a6ff; font-weight: 600; font-size: 13px; }
.result-score {
    background: rgba(63,185,80,0.15);
    color: #3fb950;
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 12px;
    font-weight: 600;
}
.result-text { color: #8b949e; font-size: 13px; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)


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
    st.markdown("## 🧠 Knowledge Base")
    st.markdown(f"<span style='color:#8b949e;font-size:12px;'>Collection: <code>{config.COLLECTION_NAME}</code></span>", unsafe_allow_html=True)
    chunk_count_placeholder = st.empty()
    chunk_count_placeholder.metric("Chunks stored", collection.count())

    st.divider()

    # Upload files
    st.markdown("**Upload Documents**")
    uploaded_files = st.file_uploader(
        "Upload",
        type=[ext.lstrip(".") for ext in config.SUPPORTED_EXTENSIONS],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )
    if uploaded_files and st.button("Ingest Uploaded Files", use_container_width=True):
        with st.spinner("Ingesting..."):
            results = {f.name: ingestor.ingest_from_bytes(f.name, f.read(), collection, embed_model) for f in uploaded_files}
        st.success(f"Ingested {len(results)} file(s)")
        for fname, count in results.items():
            st.markdown(f"<span style='color:#8b949e;font-size:13px;'>↳ **{fname}** — {count} chunks</span>", unsafe_allow_html=True)
        chunk_count_placeholder.metric("Chunks stored", collection.count())

    st.divider()

    # Ingest from data/ folder
    st.markdown("**Ingest from `data/` Folder**")
    st.caption(f"Supported: `{', '.join(sorted(config.SUPPORTED_EXTENSIONS))}`")
    if st.button("Scan & Ingest", use_container_width=True):
        with st.spinner("Ingesting..."):
            results = ingestor.ingest_all(config.DATA_DIR, collection, embed_model)
        if results:
            st.success(f"Ingested {len(results)} file(s)")
            for fname, count in results.items():
                st.markdown(f"<span style='color:#8b949e;font-size:13px;'>↳ **{fname}** — {count} chunks</span>", unsafe_allow_html=True)
            chunk_count_placeholder.metric("Chunks stored", collection.count())
        else:
            st.warning("No supported files found in `data/`.")

    st.divider()

    # Manage documents
    st.markdown("**Documents**")
    sources = ingestor.list_sources(collection)
    if not sources:
        st.caption("No documents ingested yet.")
    else:
        for source in sources:
            col1, col2 = st.columns([5, 1])
            col1.markdown(f"<span style='font-size:13px;color:#c9d1d9;'>📄 {source}</span>", unsafe_allow_html=True)
            if col2.button("✕", key=f"del_{source}", help=f"Delete {source}"):
                deleted = ingestor.delete_file(source, collection)
                st.success(f"Deleted **{source}** ({deleted} chunks)")
                chunk_count_placeholder.metric("Chunks stored", collection.count())
                st.rerun()

    st.divider()
    st.markdown(
        f"<span style='color:#8b949e;font-size:11px;'>Embed: <code>{config.EMBED_MODEL.split('/')[-1]}</code><br>"
        f"LLM: <code>{config.OLLAMA_MODEL}</code></span>",
        unsafe_allow_html=True
    )


# --- Main panel ---
st.markdown("# Personal Knowledge Base")
st.markdown("<span style='color:#8b949e;font-size:14px;'>Search and chat with your documents.</span>", unsafe_allow_html=True)
st.markdown("")

search_tab, ask_tab = st.tabs(["🔍  Search", "💬  Ask"])


# --- Search tab ---
with search_tab:
    query = st.text_input("", placeholder="Search your knowledge base...", label_visibility="collapsed")
    if st.button("Search", key="search_btn") and query:
        if collection.count() == 0:
            st.warning("No documents ingested yet. Upload files using the sidebar.")
        else:
            with st.spinner("Searching..."):
                hits = retriever.search(query, collection, embed_model)
            if hits:
                st.markdown(f"<span style='color:#8b949e;font-size:13px;'>{len(hits)} results</span>", unsafe_allow_html=True)
                for i, hit in enumerate(hits, 1):
                    st.markdown(f"""
                    <div class="result-card">
                        <div class="result-header">
                            <span class="result-source">[{i}] {hit['source']}</span>
                            <span class="result-score">{hit['similarity']}% match</span>
                        </div>
                        <div class="result-text">{hit['text'][:400]}{'...' if len(hit['text']) > 400 else ''}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No results found.")


# --- Ask tab ---
with ask_tab:
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant" and message.get("citations"):
                _hits = message["citations"]
                rows = "".join(
                    f'<div class="citation-row"><span class="ref-badge">[{i}]</span>'
                    f'<span class="ref-source">{h["source"]}</span>'
                    f'<span class="ref-match">{h["similarity"]}%</span></div>'
                    for i, h in enumerate(_hits, 1)
                )
                st.markdown(
                    f'<div class="citations-block"><div class="citations-label">References</div>{rows}</div>',
                    unsafe_allow_html=True,
                )

    if st.session_state.chat_history:
        if st.button("Clear conversation", key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()

    question = st.chat_input("Ask anything about your documents...")
    if question:
        if collection.count() == 0:
            st.warning("No documents ingested yet. Upload files using the sidebar.")
        else:
            with st.chat_message("user"):
                st.markdown(question)
            st.session_state.chat_history.append({"role": "user", "content": question})

            hits = retriever.search(question, collection, embed_model)

            if not hits:
                response = "No relevant context found in your knowledge base."
                with st.chat_message("assistant"):
                    st.markdown(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response, "citations": []})
            else:
                full_response = ""
                with st.chat_message("assistant"):
                    placeholder = st.empty()
                    for chunk in generator.generate(question, hits):
                        full_response += chunk
                        placeholder.markdown(full_response)

                    # Render citations inline
                    rows = "".join(
                        f'<div class="citation-row"><span class="ref-badge">[{i}]</span>'
                        f'<span class="ref-source">{h["source"]}</span>'
                        f'<span class="ref-match">{h["similarity"]}%</span></div>'
                        for i, h in enumerate(hits, 1)
                    )
                    st.markdown(
                        f'<div class="citations-block"><div class="citations-label">References</div>{rows}</div>',
                        unsafe_allow_html=True,
                    )

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": full_response,
                    "citations": hits,
                })
