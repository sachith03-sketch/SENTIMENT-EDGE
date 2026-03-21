"""
app.py  ──  Sentiment-Driven Financial Insight Platform
Run with:  streamlit run app.py
"""

import streamlit as st

# ── Page config (MUST be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="SentimentEdge",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS — deep-navy dark theme ────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Reset & Base ── */
html, body, [class*="css"] {
    font-family: 'Syne', sans-serif !important;
    background-color: #0b0f19 !important;
    color: #e2e8f0 !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #0f1521 !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}
section[data-testid="stSidebar"] * { color: #cbd5e1 !important; }

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: #131928;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 16px 20px;
}
[data-testid="stMetricValue"]  { font-size: 1.8rem !important; font-weight: 700 !important; }
[data-testid="stMetricLabel"]  { font-size: 0.78rem !important; opacity: 0.65; letter-spacing: .06em; text-transform: uppercase; }
[data-testid="stMetricDelta"]  { font-size: 0.85rem !important; }

/* ── Tab strip ── */
[data-testid="stTabs"] button {
    font-family: 'Syne', sans-serif !important;
    font-weight: 600;
    letter-spacing: .04em;
    text-transform: uppercase;
    font-size: 0.78rem;
    border-radius: 6px 6px 0 0;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #00e5a0 !important;
    border-bottom: 2px solid #00e5a0 !important;
}

/* ── Inputs ── */
.stTextInput input, .stSelectbox select, .stNumberInput input {
    background: #131928 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    font-family: 'Syne', sans-serif !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #00e5a0, #00b4d8) !important;
    color: #0b0f19 !important;
    font-weight: 700 !important;
    font-family: 'Syne', sans-serif !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 2rem !important;
    transition: opacity 0.2s ease;
}
.stButton > button:hover { opacity: 0.88 !important; }

/* ── Expander ── */
details { background: #131928 !important; border-radius: 10px; padding: 2px 12px; }
summary { font-weight: 600; color: #94a3b8; }

/* ── Dataframe ── */
.stDataFrame { border-radius: 10px; overflow: hidden; }

/* ── Divider ── */
hr { border-color: rgba(255,255,255,0.07) !important; }

/* ── Success / Info / Error banners ── */
.stSuccess { background: rgba(0,229,160,0.12) !important; border: 1px solid #00e5a0 !important; border-radius: 8px !important; }
.stInfo    { background: rgba(56,189,248,0.10) !important; border: 1px solid #38bdf8 !important; border-radius: 8px !important; }
.stError   { background: rgba(255,77,109,0.12) !important; border: 1px solid #ff4d6d !important; border-radius: 8px !important; }
.stWarning { background: rgba(245,158,11,0.12) !important; border: 1px solid #f59e0b !important; border-radius: 8px !important; }

/* ── Code ── */
code { font-family: 'JetBrains Mono', monospace !important; background: #131928 !important; padding: 2px 6px; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar Logo & Nav ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 1rem 0 1.5rem 0;">
        <div style="font-size:1.7rem; font-weight:800; letter-spacing:-.02em;">
            📈 <span style="color:#00e5a0;">Sentiment</span>Edge
        </div>
        <div style="font-size:0.72rem; color:#64748b; letter-spacing:.08em; margin-top:4px;">
            FINANCIAL INSIGHT PLATFORM
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    page = st.radio(
        "Navigation",
        ["🏠  Overview",
         "🔍  Single Figure Analysis",
         "⚖️  Comparison Engine",
         "🤖  ML Predictions",
         "📋  Raw Data"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("### ⚙️ API Settings")
    api_key = st.text_input(
        "NewsAPI Key",
        type="password",
        placeholder="Paste your key here",
        help="Get a free key at newsapi.org",
    )
    page_size = st.slider("Articles per query", 10, 50, 20, 5)

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.68rem;color:#475569;line-height:1.6;'>"
        "Data: NewsAPI · Yahoo Finance<br>"
        "Sentiment: VADER NLP<br>"
        "ML: scikit-learn<br>"
        "</div>",
        unsafe_allow_html=True,
    )

# ── Route to pages ────────────────────────────────────────────────────────────
ctx = {"api_key": api_key, "page_size": page_size}

if page == "🏠  Overview":
    from pages.overview    import render; render(ctx)
elif page == "🔍  Single Figure Analysis":
    from pages.single      import render; render(ctx)
elif page == "⚖️  Comparison Engine":
    from pages.comparison  import render; render(ctx)
elif page == "🤖  ML Predictions":
    from pages.ml          import render; render(ctx)
elif page == "📋  Raw Data":
    from pages.raw_data    import render; render(ctx)