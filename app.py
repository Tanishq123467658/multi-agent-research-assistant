import streamlit as st
import time
from pipeline import run_research_pipeline

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Research Intelligence",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@300;400;500&family=Syne:wght@400;600;800&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'DM Mono', monospace;
    background-color: #080C10;
    color: #E8E4DA;
}

.stApp {
    background: #080C10;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1100px; }

/* ── Hero Header ── */
.hero {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    margin-bottom: 3rem;
    padding-bottom: 2rem;
    border-bottom: 1px solid rgba(255,255,255,0.07);
}

.hero-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #5BE49B;
}

.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(2.4rem, 5vw, 3.8rem);
    line-height: 1.1;
    color: #F0EBE0;
    font-style: italic;
}

.hero-subtitle {
    font-size: 0.82rem;
    color: rgba(232, 228, 218, 0.45);
    letter-spacing: 0.02em;
    margin-top: 0.5rem;
}

/* ── Input Area ── */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 0 !important;
    color: #E8E4DA !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 1rem !important;
    padding: 1rem 1.2rem !important;
    caret-color: #5BE49B;
    transition: border-color 0.2s;
}

.stTextInput > div > div > input:focus {
    border-color: #5BE49B !important;
    box-shadow: 0 0 0 1px #5BE49B22 !important;
}

.stTextInput > div > div > input::placeholder {
    color: rgba(232,228,218,0.25) !important;
}

/* ── Button ── */
.stButton > button {
    background: #5BE49B !important;
    color: #080C10 !important;
    border: none !important;
    border-radius: 0 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.78rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    padding: 0.85rem 2.5rem !important;
    cursor: pointer !important;
    transition: all 0.15s !important;
    width: 100% !important;
}

.stButton > button:hover {
    background: #3fd484 !important;
    transform: translateY(-1px);
}

.stButton > button:active {
    transform: translateY(0px);
}

/* ── Pipeline Steps ── */
.step-container {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    margin: 2rem 0;
}

.step-card {
    display: flex;
    align-items: flex-start;
    gap: 1.2rem;
    padding: 1.1rem 1.3rem;
    border: 1px solid rgba(255,255,255,0.06);
    background: rgba(255,255,255,0.02);
    transition: all 0.3s;
}

.step-card.active {
    border-color: #5BE49B44;
    background: rgba(91, 228, 155, 0.04);
}

.step-card.done {
    border-color: rgba(91, 228, 155, 0.2);
    background: rgba(91, 228, 155, 0.03);
}

.step-icon {
    font-size: 1.1rem;
    min-width: 1.5rem;
    text-align: center;
    margin-top: 1px;
}

.step-meta {
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
}

.step-number {
    font-size: 0.62rem;
    letter-spacing: 0.2em;
    color: rgba(232,228,218,0.3);
    font-weight: 500;
    text-transform: uppercase;
}

.step-name {
    font-family: 'Syne', sans-serif;
    font-size: 0.88rem;
    font-weight: 600;
    color: #E8E4DA;
}

.step-name.active { color: #5BE49B; }

.step-desc {
    font-size: 0.74rem;
    color: rgba(232,228,218,0.4);
    margin-top: 0.15rem;
}

/* ── Section Blocks ── */
.section-wrapper {
    margin-top: 2.5rem;
}

.section-label {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 0.75rem;
}

.section-label-text {
    font-family: 'Syne', sans-serif;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: rgba(232,228,218,0.4);
}

.section-line {
    flex: 1;
    height: 1px;
    background: rgba(255,255,255,0.06);
}

.content-block {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    padding: 1.5rem;
    font-size: 0.85rem;
    line-height: 1.8;
    color: rgba(232,228,218,0.8);
    white-space: pre-wrap;
    word-break: break-word;
}

.report-block {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-left: 3px solid #5BE49B;
    padding: 2rem;
    font-size: 0.9rem;
    line-height: 1.9;
    color: #E8E4DA;
    white-space: pre-wrap;
    word-break: break-word;
}

.feedback-block {
    background: rgba(255,200,100,0.04);
    border: 1px solid rgba(255,200,100,0.12);
    border-left: 3px solid #F5C842;
    padding: 1.5rem;
    font-size: 0.85rem;
    line-height: 1.8;
    color: rgba(232,228,218,0.8);
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── URL Chips ── */
.url-grid {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
}

.url-chip {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 0.5rem 0.8rem;
    font-size: 0.72rem;
    color: #5BE49B;
    word-break: break-all;
    font-family: 'DM Mono', monospace;
}

/* ── Stats Bar ── */
.stats-bar {
    display: flex;
    gap: 2rem;
    margin: 2rem 0;
    padding: 1.2rem 1.5rem;
    background: rgba(91, 228, 155, 0.05);
    border: 1px solid rgba(91, 228, 155, 0.15);
}

.stat-item {
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
}

.stat-value {
    font-family: 'DM Serif Display', serif;
    font-size: 1.6rem;
    color: #5BE49B;
    line-height: 1;
}

.stat-label {
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: rgba(232,228,218,0.35);
}

/* ── Error State ── */
.error-block {
    border: 1px solid rgba(255, 80, 80, 0.3);
    background: rgba(255, 80, 80, 0.05);
    border-left: 3px solid #FF5050;
    padding: 1.2rem 1.5rem;
    font-size: 0.85rem;
    color: #FF8080;
}

/* ── Divider ── */
hr { border-color: rgba(255,255,255,0.05) !important; margin: 2rem 0 !important; }

/* ── Spinner override ── */
.stSpinner > div {
    border-top-color: #5BE49B !important;
}
</style>
""", unsafe_allow_html=True)


# ─── Session State Init ──────────────────────────────────────────────────────
if "results" not in st.session_state:
    st.session_state.results = None
if "running" not in st.session_state:
    st.session_state.running = False
if "elapsed" not in st.session_state:
    st.session_state.elapsed = None


# ─── Hero ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <span class="hero-label">Multi-Agent Research System</span>
    <h1 class="hero-title">Research Intelligence</h1>
    <p class="hero-subtitle">Search → Scrape → Write → Review — fully automated, deeply researched.</p>
</div>
""", unsafe_allow_html=True)


# ─── Input ───────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1.2])

with col_input:
    topic = st.text_input(
        label="topic",
        placeholder="Enter a research topic, e.g. 'Quantum computing breakthroughs 2025'",
        label_visibility="collapsed"
    )

with col_btn:
    run_btn = st.button("▶  Run", disabled=st.session_state.running)


# ─── Pipeline Execution ──────────────────────────────────────────────────────
STEPS = [
    ("🔍", "01", "Search Agent",  "Querying the web for recent information"),
    ("📖", "02", "Reader Agent",  "Scraping and extracting page content"),
    ("✍️",  "03", "Writer Agent",  "Synthesising a structured report"),
    ("🧐", "04", "Critic Agent",  "Reviewing and providing feedback"),
]

if run_btn and topic.strip():
    st.session_state.running = True
    st.session_state.results = None

    # Steps display placeholder
    steps_ph = st.empty()
    status_ph = st.empty()

    def render_steps(active_idx, done_count):
        cards = ""
        for i, (icon, num, name, desc) in enumerate(STEPS):
            if i < done_count:
                cls = "done"; name_cls = ""; ico = "✅"
            elif i == active_idx:
                cls = "active"; name_cls = "active"; ico = icon
            else:
                cls = ""; name_cls = ""; ico = icon
            cards += f"""
            <div class="step-card {cls}">
                <span class="step-icon">{ico}</span>
                <div class="step-meta">
                    <span class="step-number">Step {num}</span>
                    <span class="step-name {name_cls}">{name}</span>
                    <span class="step-desc">{desc}</span>
                </div>
            </div>"""
        steps_ph.markdown(f'<div class="step-container">{cards}</div>', unsafe_allow_html=True)

    render_steps(0, 0)

    start = time.time()

    try:
        with status_ph:
            with st.spinner("Pipeline running…"):
                results = run_research_pipeline(topic.strip())
    except Exception as e:
        st.session_state.running = False
        st.markdown(f'<div class="error-block">❌ Pipeline error: {e}</div>', unsafe_allow_html=True)
        st.stop()

    elapsed = round(time.time() - start, 1)
    render_steps(-1, 4)
    status_ph.empty()

    st.session_state.results = results
    st.session_state.elapsed = elapsed
    st.session_state.running = False


elif run_btn and not topic.strip():
    st.warning("Please enter a research topic first.")


# ─── Results ─────────────────────────────────────────────────────────────────
if st.session_state.results:
    res = st.session_state.results

    # Stats bar
    url_count  = len(res.get("urls", []))
    scrape_len = len(res.get("scraped_content", ""))
    report_len = len(res.get("report", ""))

    st.markdown(f"""
    <div class="stats-bar">
        <div class="stat-item">
            <span class="stat-value">{url_count}</span>
            <span class="stat-label">URLs found</span>
        </div>
        <div class="stat-item">
            <span class="stat-value">{scrape_len:,}</span>
            <span class="stat-label">Chars scraped</span>
        </div>
        <div class="stat-item">
            <span class="stat-value">{report_len:,}</span>
            <span class="stat-label">Report chars</span>
        </div>
        <div class="stat-item">
            <span class="stat-value">{st.session_state.elapsed}s</span>
            <span class="stat-label">Total time</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Search Results
    if res.get("search_results"):
        st.markdown("""
        <div class="section-wrapper">
            <div class="section-label">
                <span class="section-label-text">🔍 Search Results</span>
                <div class="section-line"></div>
            </div>
        </div>""", unsafe_allow_html=True)
        st.markdown(f'<div class="content-block">{res["search_results"][:1500]}{"…" if len(res["search_results"]) > 1500 else ""}</div>', unsafe_allow_html=True)

    # ── URLs
    if res.get("urls"):
        st.markdown("""
        <div class="section-wrapper">
            <div class="section-label">
                <span class="section-label-text">🔗 Extracted URLs</span>
                <div class="section-line"></div>
            </div>
        </div>""", unsafe_allow_html=True)
        chips = "".join(f'<div class="url-chip">{u}</div>' for u in res["urls"])
        st.markdown(f'<div class="url-grid">{chips}</div>', unsafe_allow_html=True)

    # ── Scraped Content
    if res.get("scraped_content"):
        st.markdown("""
        <div class="section-wrapper">
            <div class="section-label">
                <span class="section-label-text">📖 Scraped Content Preview</span>
                <div class="section-line"></div>
            </div>
        </div>""", unsafe_allow_html=True)
        preview = res["scraped_content"][:1200]
        st.markdown(f'<div class="content-block">{preview}{"…" if len(res["scraped_content"]) > 1200 else ""}</div>', unsafe_allow_html=True)

    # ── Report
    if res.get("report"):
        st.markdown("""
        <div class="section-wrapper">
            <div class="section-label">
                <span class="section-label-text">✍️ Generated Report</span>
                <div class="section-line"></div>
            </div>
        </div>""", unsafe_allow_html=True)
        st.markdown(f'<div class="report-block">{res["report"]}</div>', unsafe_allow_html=True)

        # Download button
        st.download_button(
            label="⬇  Download Report (.txt)",
            data=res["report"],
            file_name=f"report_{topic[:30].replace(' ', '_')}.txt",
            mime="text/plain",
        )

    # ── Feedback
    if res.get("feedback"):
        st.markdown("""
        <div class="section-wrapper">
            <div class="section-label">
                <span class="section-label-text">🧐 Critic Feedback</span>
                <div class="section-line"></div>
            </div>
        </div>""", unsafe_allow_html=True)
        st.markdown(f'<div class="feedback-block">{res["feedback"]}</div>', unsafe_allow_html=True)


# ─── Empty State ─────────────────────────────────────────────────────────────
elif not st.session_state.running:
    st.markdown("""
    <div style="margin-top:3rem; text-align:center; color:rgba(232,228,218,0.18); font-size:0.8rem; letter-spacing:0.12em;">
        ↑  Enter a topic above and press Run to start the pipeline
    </div>
    """, unsafe_allow_html=True)