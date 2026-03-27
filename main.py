import streamlit as st

from app import config, ingestor, retriever, generator

st.set_page_config(
    page_title="Knowledge Base",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
  -webkit-font-smoothing: antialiased !important;
}

#MainMenu, footer, [data-testid="stToolbar"] { display: none !important; }

/* ── BACKGROUND ── */
.stApp {
  background-color: #050508 !important;
  background-image: radial-gradient(circle, rgba(255,255,255,0.10) 1px, transparent 1px) !important;
  background-size: 28px 28px !important;
}
.stApp::before {
  content: '';
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 50% at 50% 0%, rgba(139,92,246,0.08) 0%, transparent 70%),
    radial-gradient(ellipse 60% 40% at 100% 100%, rgba(96,165,250,0.06) 0%, transparent 65%),
    radial-gradient(ellipse 100% 100% at 50% 50%, transparent 40%, #050508 100%);
  pointer-events: none;
  z-index: 0;
}
.main .block-container { position: relative; z-index: 1; }

/* ── KEYFRAMES ── */
@keyframes gradientShift {
  0%   { background-position: 0% 50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes glowPulse {
  0%, 100% { box-shadow: 0 0 8px 2px rgba(139,92,246,0.3), 0 0 20px 4px rgba(139,92,246,0.12); }
  50%       { box-shadow: 0 0 16px 4px rgba(139,92,246,0.55), 0 0 40px 8px rgba(96,165,250,0.2); }
}
@keyframes float {
  0%, 100% { transform: translateY(0px) scale(1); }
  33%       { transform: translateY(-20px) scale(1.03); }
  66%       { transform: translateY(10px) scale(0.97); }
}
@keyframes floatAlt {
  0%, 100% { transform: translateY(0px) scale(1); }
  40%       { transform: translateY(16px) scale(1.04); }
  70%       { transform: translateY(-12px) scale(0.97); }
}
@keyframes shimmer {
  0%   { transform: translateX(-100%) skewX(-12deg); }
  100% { transform: translateX(260%) skewX(-12deg); }
}
@keyframes dotBlink {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.5; }
}

/* ── ORBS ── */
.orb-container {
  position: fixed; inset: 0;
  pointer-events: none; z-index: 0; overflow: hidden;
}
.orb {
  position: absolute; border-radius: 50%; filter: blur(80px); opacity: 0.15;
}
.orb-purple {
  width: 560px; height: 560px;
  background: radial-gradient(circle, #8b5cf6 0%, #6d28d9 50%, transparent 70%);
  top: -160px; left: -100px;
  animation: float 16s ease-in-out infinite;
}
.orb-blue {
  width: 480px; height: 480px;
  background: radial-gradient(circle, #60a5fa 0%, #2563eb 50%, transparent 70%);
  top: 35%; right: -140px;
  opacity: 0.11;
  animation: floatAlt 20s ease-in-out infinite;
}
.orb-teal {
  width: 360px; height: 360px;
  background: radial-gradient(circle, #34d399 0%, #059669 50%, transparent 70%);
  bottom: -80px; left: 35%;
  opacity: 0.10;
  animation: float 24s ease-in-out infinite reverse;
}

/* ── HERO ── */
.hero-wrapper {
  padding: 3rem 0 2rem;
  animation: fadeInUp 0.7s ease both;
}
.hero-eyebrow {
  display: inline-flex; align-items: center; gap: 8px;
  background: rgba(139,92,246,0.12);
  border: 1px solid rgba(139,92,246,0.3);
  border-radius: 100px;
  padding: 5px 14px 5px 10px;
  font-size: 11px; font-weight: 700; color: #a78bfa;
  letter-spacing: 0.06em; text-transform: uppercase;
  margin-bottom: 1.25rem;
  animation: glowPulse 3s ease-in-out infinite;
}
.hero-dot {
  width: 7px; height: 7px; border-radius: 50%;
  background: #8b5cf6;
  box-shadow: 0 0 6px 2px rgba(139,92,246,0.7);
  animation: dotBlink 2s ease-in-out infinite;
}
.hero-title {
  font-size: clamp(2.2rem, 4.5vw, 3.6rem);
  font-weight: 800; line-height: 1.08;
  letter-spacing: -0.03em; margin: 0 0 1rem;
  background: linear-gradient(135deg, #f8fafc 0%, #c4b5fd 30%, #93c5fd 60%, #6ee7b7 100%);
  background-size: 300% 300%;
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: gradientShift 7s ease-in-out infinite;
}
.hero-sub {
  font-size: 1rem; color: #64748b; line-height: 1.7;
  max-width: 500px; margin: 0;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
  background: rgba(5,5,8,0.95) !important;
  border-right: 1px solid rgba(255,255,255,0.07) !important;
  backdrop-filter: blur(20px) !important;
}
[data-testid="stSidebar"]::before {
  content: '';
  position: absolute; inset: 0;
  background: linear-gradient(180deg, rgba(139,92,246,0.05) 0%, transparent 50%, rgba(52,211,153,0.03) 100%);
  pointer-events: none;
}

/* ── BUTTONS (main) ── */
.stButton > button {
  position: relative;
  background: linear-gradient(135deg, #7c3aed, #6d28d9, #4f46e5) !important;
  background-size: 200% 200% !important;
  color: #fff !important; border: none !important;
  border-radius: 10px !important;
  font-weight: 600 !important; font-size: 13px !important;
  letter-spacing: 0.01em !important;
  padding: 0.55rem 1.2rem !important;
  transition: all 0.25s ease !important;
  box-shadow: 0 0 0 1px rgba(139,92,246,0.3), 0 2px 8px rgba(139,92,246,0.25), inset 0 1px 0 rgba(255,255,255,0.1) !important;
  overflow: hidden !important;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 0 0 1px rgba(139,92,246,0.5), 0 6px 24px rgba(139,92,246,0.4), 0 2px 8px rgba(96,165,250,0.2), inset 0 1px 0 rgba(255,255,255,0.15) !important;
  animation: gradientShift 2s ease-in-out infinite !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* Sidebar buttons — teal variant */
[data-testid="stSidebar"] .stButton > button {
  background: rgba(52,211,153,0.1) !important;
  border: 1px solid rgba(52,211,153,0.25) !important;
  color: #34d399 !important;
  box-shadow: none !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
  background: rgba(52,211,153,0.18) !important;
  border-color: rgba(52,211,153,0.5) !important;
  box-shadow: 0 4px 20px rgba(52,211,153,0.2) !important;
  color: #6ee7b7 !important;
  animation: none !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
  background: transparent !important;
  border-bottom: 1px solid rgba(255,255,255,0.07) !important;
  gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
  color: #64748b !important; font-weight: 500 !important;
  font-size: 14px !important; padding: 0.75rem 1.5rem !important;
  border-radius: 0 !important; background: transparent !important;
  transition: color 0.2s !important;
}
.stTabs [data-baseweb="tab"]:hover { color: #cbd5e1 !important; }
.stTabs [aria-selected="true"] {
  color: #f8fafc !important;
  border-bottom: 2px solid #8b5cf6 !important;
  background: transparent !important;
}

/* ── CHAT MESSAGES ── */
[data-testid="stChatMessage"] {
  background: rgba(255,255,255,0.03) !important;
  border: 1px solid rgba(255,255,255,0.07) !important;
  border-radius: 14px !important;
  margin: 8px 0 !important;
  backdrop-filter: blur(12px) !important;
  animation: fadeInUp 0.4s ease both !important;
  transition: border-color 0.2s !important;
}
[data-testid="stChatMessage"]:hover { border-color: rgba(255,255,255,0.12) !important; }

/* ── CHAT INPUT ── */
[data-testid="stChatInput"] {
  background: rgba(255,255,255,0.03) !important;
  border: 1px solid rgba(255,255,255,0.1) !important;
  border-radius: 14px !important; backdrop-filter: blur(16px) !important;
  transition: border-color 0.25s, box-shadow 0.25s !important;
}
[data-testid="stChatInput"]:focus-within {
  border-color: rgba(139,92,246,0.5) !important;
  box-shadow: 0 0 0 3px rgba(139,92,246,0.12), 0 4px 20px rgba(139,92,246,0.15) !important;
}
[data-testid="stChatInput"] textarea {
  background: transparent !important; color: #f8fafc !important;
  caret-color: #8b5cf6 !important;
}

/* ── TEXT INPUT ── */
.stTextInput > div > div > input {
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid rgba(255,255,255,0.1) !important;
  border-radius: 10px !important; color: #f8fafc !important;
  font-size: 14px !important; backdrop-filter: blur(8px) !important;
  transition: border-color 0.25s, box-shadow 0.25s !important;
}
.stTextInput > div > div > input:focus {
  border-color: rgba(139,92,246,0.5) !important;
  box-shadow: 0 0 0 3px rgba(139,92,246,0.12) !important;
}
.stTextInput > div > div > input::placeholder { color: #334155 !important; }

/* ── METRICS ── */
[data-testid="stMetric"] {
  background: rgba(255,255,255,0.03) !important;
  border: 1px solid rgba(255,255,255,0.08) !important;
  border-radius: 12px !important; padding: 1rem !important;
  transition: border-color 0.2s !important;
}
[data-testid="stMetric"]:hover { border-color: rgba(139,92,246,0.3) !important; }
[data-testid="stMetricValue"] {
  background: linear-gradient(135deg, #a78bfa, #60a5fa) !important;
  -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important;
  background-clip: text !important; font-weight: 800 !important; font-size: 2rem !important;
}
[data-testid="stMetricLabel"] {
  color: #475569 !important; font-size: 11px !important;
  text-transform: uppercase !important; letter-spacing: 0.07em !important; font-weight: 600 !important;
}

/* ── FILE UPLOADER ── */
[data-testid="stFileUploader"] {
  background: rgba(255,255,255,0.02) !important;
  border: 1px dashed rgba(255,255,255,0.12) !important;
  border-radius: 12px !important; transition: all 0.25s !important;
}
[data-testid="stFileUploader"]:hover {
  background: rgba(139,92,246,0.05) !important;
  border-color: rgba(139,92,246,0.35) !important;
}

/* ── EXPANDER ── */
[data-testid="stExpander"] {
  background: rgba(255,255,255,0.03) !important;
  border: 1px solid rgba(255,255,255,0.08) !important;
  border-radius: 12px !important; backdrop-filter: blur(10px) !important;
  transition: border-color 0.2s !important;
}
[data-testid="stExpander"]:hover { border-color: rgba(139,92,246,0.25) !important; }

/* ── ALERTS ── */
[data-testid="stAlert"] { border-radius: 12px !important; }

/* ── TYPOGRAPHY ── */
h1 { color: #f8fafc !important; font-weight: 800 !important; letter-spacing: -0.03em !important; }
h2, h3 { color: #e2e8f0 !important; font-weight: 700 !important; letter-spacing: -0.02em !important; }
p, li { color: #94a3b8 !important; line-height: 1.7 !important; }
label { color: #64748b !important; font-size: 13px !important; font-weight: 500 !important; }
hr { border-color: rgba(255,255,255,0.07) !important; }
code {
  background: rgba(139,92,246,0.12) !important; color: #c4b5fd !important;
  border-radius: 5px !important; padding: 2px 7px !important;
  border: 1px solid rgba(139,92,246,0.2) !important;
}

/* ── RESULT CARDS ── */
.result-card {
  position: relative;
  background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
  border-radius: 14px; padding: 16px 20px; margin: 10px 0;
  backdrop-filter: blur(12px); overflow: hidden;
  transition: border-color 0.25s, transform 0.25s, box-shadow 0.25s;
  animation: fadeInUp 0.4s ease both;
}
.result-card:hover {
  border-color: rgba(96,165,250,0.4); transform: translateY(-2px);
  box-shadow: 0 0 0 1px rgba(96,165,250,0.1), 0 8px 32px rgba(96,165,250,0.1);
}
.result-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.result-source { color: #60a5fa; font-weight: 600; font-size: 13px; }
.result-score {
  background: rgba(52,211,153,0.12); color: #34d399;
  border: 1px solid rgba(52,211,153,0.2); border-radius: 100px;
  padding: 2px 10px; font-size: 11px; font-weight: 700;
}
.result-text { color: #64748b; font-size: 13px; line-height: 1.7; }

/* ── CITATIONS ── */
.citations-block {
  margin-top: 16px; padding: 14px 18px;
  background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.07);
  border-radius: 12px; backdrop-filter: blur(10px);
  animation: fadeInUp 0.5s ease both;
}
.citations-label {
  font-size: 10px; font-weight: 700; color: #475569;
  text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 10px;
}
.citation-row {
  display: flex; align-items: center; gap: 12px;
  padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.05);
  transition: padding-left 0.15s;
}
.citation-row:last-child { border-bottom: none; }
.citation-row:hover { padding-left: 4px; }
.ref-badge {
  background: linear-gradient(135deg, #7c3aed, #4f46e5); color: #fff;
  border-radius: 6px; padding: 2px 8px;
  font-size: 11px; font-weight: 700; min-width: 28px; text-align: center;
  box-shadow: 0 2px 8px rgba(139,92,246,0.3);
}
.ref-source { color: #cbd5e1; font-size: 13px; flex: 1; }
.ref-match { color: #34d399; font-size: 12px; font-weight: 600; }

/* ── STATUS BADGES ── */
.status-row { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 6px; }
.status-badge {
  display: inline-flex; align-items: center; gap: 6px;
  background: rgba(52,211,153,0.1); border: 1px solid rgba(52,211,153,0.25);
  border-radius: 100px; padding: 4px 12px;
  font-size: 11px; font-weight: 600; color: #34d399; letter-spacing: 0.03em;
}
.badge-dot {
  width: 6px; height: 6px; border-radius: 50%; background: #34d399;
  box-shadow: 0 0 6px rgba(52,211,153,0.7);
  animation: dotBlink 2s ease-in-out infinite;
}
.badge-purple {
  background: rgba(139,92,246,0.12); border-color: rgba(139,92,246,0.3); color: #a78bfa;
}
.badge-blue {
  background: rgba(96,165,250,0.1); border-color: rgba(96,165,250,0.25); color: #93c5fd;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.08); border-radius: 100px; }
::-webkit-scrollbar-thumb:hover { background: rgba(139,92,246,0.4); }
::selection { background: rgba(139,92,246,0.35); color: #f8fafc; }
</style>
""", unsafe_allow_html=True)

# ── BACKGROUND ORBS ─────────────────────────────────────────────────────────
st.markdown("""
<div class="orb-container" aria-hidden="true">
  <div class="orb orb-purple"></div>
  <div class="orb orb-blue"></div>
  <div class="orb orb-teal"></div>
</div>
""", unsafe_allow_html=True)


# ── SESSION STATE ────────────────────────────────────────────────────────────
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

llm_label = f"Claude · {config.CLAUDE_MODEL.split('-')[1]}" if config.ANTHROPIC_API_KEY else f"Ollama · {config.OLLAMA_MODEL}"


# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧠 Knowledge Base")

    st.markdown(f"""
    <div class="status-row">
      <span class="status-badge"><span class="badge-dot"></span>Local &amp; Private</span>
      <span class="status-badge badge-purple">{llm_label}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"<span style='color:#475569;font-size:11px;'>Collection: <code>{config.COLLECTION_NAME}</code></span>", unsafe_allow_html=True)
    chunk_placeholder = st.empty()
    chunk_placeholder.metric("Chunks stored", collection.count())

    st.divider()

    # Upload
    st.markdown("**Upload Documents**")
    uploaded_files = st.file_uploader(
        "upload",
        type=[ext.lstrip(".") for ext in config.SUPPORTED_EXTENSIONS],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )
    if uploaded_files and st.button("Ingest Uploaded Files", use_container_width=True):
        with st.spinner("Ingesting..."):
            results = {f.name: ingestor.ingest_from_bytes(f.name, f.read(), collection, embed_model) for f in uploaded_files}
        st.success(f"Ingested {len(results)} file(s)")
        for fname, count in results.items():
            st.markdown(f"<span style='color:#64748b;font-size:12px;'>↳ {fname} — {count} chunks</span>", unsafe_allow_html=True)
        chunk_placeholder.metric("Chunks stored", collection.count())

    st.divider()

    # Ingest from data/
    st.markdown("**Ingest from `data/` Folder**")
    st.caption(f"Supported: `{', '.join(sorted(config.SUPPORTED_EXTENSIONS))}`")
    if st.button("Scan & Ingest", use_container_width=True):
        with st.spinner("Scanning..."):
            results = ingestor.ingest_all(config.DATA_DIR, collection, embed_model)
        if results:
            st.success(f"Ingested {len(results)} file(s)")
            for fname, count in results.items():
                st.markdown(f"<span style='color:#64748b;font-size:12px;'>↳ {fname} — {count} chunks</span>", unsafe_allow_html=True)
            chunk_placeholder.metric("Chunks stored", collection.count())
        else:
            st.warning("No supported files found in `data/`.")

    st.divider()

    # Manage docs
    st.markdown("**Documents**")
    sources = ingestor.list_sources(collection)
    if not sources:
        st.caption("No documents ingested yet.")
    else:
        for source in sources:
            c1, c2 = st.columns([5, 1])
            c1.markdown(f"<span style='font-size:13px;color:#94a3b8;'>📄 {source}</span>", unsafe_allow_html=True)
            if c2.button("✕", key=f"del_{source}", help=f"Delete {source}"):
                deleted = ingestor.delete_file(source, collection)
                st.success(f"Deleted {source} ({deleted} chunks)")
                chunk_placeholder.metric("Chunks stored", collection.count())
                st.rerun()


# ── MAIN PANEL ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrapper">
  <div class="hero-eyebrow">
    <span class="hero-dot"></span>
    Personal Knowledge OS
  </div>
  <h1 class="hero-title">Your documents,<br>finally searchable.</h1>
  <p class="hero-sub">
    Upload PDFs, docs, and notes. Ask questions in plain English.
    Every answer is grounded in your documents with cited sources.
  </p>
</div>
""", unsafe_allow_html=True)

search_tab, ask_tab = st.tabs(["🔍  Search", "💬  Ask"])


# ── SEARCH TAB ───────────────────────────────────────────────────────────────
with search_tab:
    query = st.text_input("", placeholder="Search your knowledge base...", label_visibility="collapsed")
    if st.button("Search", key="search_btn") and query:
        if collection.count() == 0:
            st.warning("No documents ingested yet. Upload files using the sidebar.")
        else:
            with st.spinner("Searching..."):
                hits = retriever.search(query, collection, embed_model)
            if hits:
                st.markdown(f"<p style='color:#475569;font-size:13px;margin-bottom:4px;'>{len(hits)} results</p>", unsafe_allow_html=True)
                for i, hit in enumerate(hits, 1):
                    snippet = hit["text"][:420] + ("..." if len(hit["text"]) > 420 else "")
                    st.markdown(f"""
                    <div class="result-card">
                      <div class="result-header">
                        <span class="result-source">[{i}] {hit['source']}</span>
                        <span class="result-score">{hit['similarity']}% match</span>
                      </div>
                      <div class="result-text">{snippet}</div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.info("No results found.")


# ── ASK TAB ──────────────────────────────────────────────────────────────────
with ask_tab:
    # Render history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and msg.get("citations"):
                rows = "".join(
                    f'<div class="citation-row">'
                    f'<span class="ref-badge">[{i}]</span>'
                    f'<span class="ref-source">{h["source"]}</span>'
                    f'<span class="ref-match">{h["similarity"]}%</span>'
                    f'</div>'
                    for i, h in enumerate(msg["citations"], 1)
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

                    rows = "".join(
                        f'<div class="citation-row">'
                        f'<span class="ref-badge">[{i}]</span>'
                        f'<span class="ref-source">{h["source"]}</span>'
                        f'<span class="ref-match">{h["similarity"]}%</span>'
                        f'</div>'
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
