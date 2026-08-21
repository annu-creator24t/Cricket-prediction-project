import streamlit as st

def apply_custom_css():
    """Injects unified enterprise CSS across all Streamlit pages."""
    st.markdown("""
    <style>
        /* Global typography & base spacing */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            color: #1E293B;
            -webkit-font-smoothing: antialiased;
        }

        /* Top header padding normalization */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 3rem !important;
            max-width: 1200px;
        }

        /* -------------------------------------------------- */
        /* TYPOGRAPHY HIERARCHY                              */
        /* -------------------------------------------------- */
        .page-header-container {
            margin-bottom: 1.5rem;
        }

        .page-eyebrow {
            font-size: 0.75rem;
            font-weight: 700;
            color: #006699;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.35rem;
        }

        .page-title {
            font-size: 1.85rem;
            font-weight: 700;
            color: #0F172A;
            letter-spacing: -0.025em;
            margin-bottom: 0.35rem;
            line-height: 1.25;
        }

        .page-subtitle {
            font-size: 0.95rem;
            font-weight: 400;
            color: #64748B;
            margin-bottom: 1.25rem;
            line-height: 1.55;
        }

        .section-header-block {
            margin-top: 1.5rem;
            margin-bottom: 1rem;
        }

        .section-eyebrow {
            font-size: 0.72rem;
            font-weight: 700;
            color: #0369A1;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 0.2rem;
        }

        .section-title {
            font-size: 1.15rem;
            font-weight: 600;
            color: #0F172A;
            letter-spacing: -0.01em;
            margin-bottom: 0.25rem;
        }

        .section-subtitle {
            font-size: 0.85rem;
            color: #64748B;
            margin-bottom: 0.75rem;
            line-height: 1.45;
        }

        /* -------------------------------------------------- */
        /* HERO & PRODUCT BANNER                              */
        /* -------------------------------------------------- */
        .hero-banner {
            background-color: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-left: 4px solid #006699;
            border-radius: 8px;
            padding: 1.5rem 1.75rem;
            margin-bottom: 1.75rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.03);
        }

        .hero-badge {
            display: inline-block;
            font-size: 0.72rem;
            font-weight: 700;
            background-color: #E0F2FE;
            color: #0369A1;
            padding: 3px 9px;
            border-radius: 4px;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 0.65rem;
        }

        .hero-title {
            font-size: 1.65rem;
            font-weight: 700;
            color: #0F172A;
            letter-spacing: -0.02em;
            margin-bottom: 0.4rem;
            line-height: 1.25;
        }

        .hero-desc {
            font-size: 0.925rem;
            color: #475569;
            line-height: 1.55;
            max-width: 900px;
            margin-bottom: 0;
        }

        /* -------------------------------------------------- */
        /* KPI CARD COMPONENT                                 */
        /* -------------------------------------------------- */
        .kpi-card {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-top: 3px solid #006699;
            border-radius: 8px;
            padding: 1rem 1.15rem;
            margin-bottom: 0.75rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.03);
            transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
            height: 100%;
        }

        .kpi-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 10px rgba(0, 102, 153, 0.07);
            border-color: #CBD5E1;
            border-top-color: #0284C7;
        }

        .kpi-category {
            font-size: 0.72rem;
            font-weight: 600;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.35rem;
        }

        .kpi-number {
            font-size: 1.65rem;
            font-weight: 700;
            color: #0F172A;
            line-height: 1.15;
            margin-bottom: 0.25rem;
            font-feature-settings: "tnum";
        }

        .kpi-subtext {
            font-size: 0.78rem;
            color: #64748B;
            line-height: 1.35;
        }

        /* -------------------------------------------------- */
        /* MODULE & FEATURE CARDS                             */
        /* -------------------------------------------------- */
        .module-card {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 1.35rem 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.03);
            transition: all 0.18s ease-in-out;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .module-card:hover {
            border-color: #BAE6FD;
            box-shadow: 0 4px 14px rgba(0, 102, 153, 0.08);
            transform: translateY(-2px);
        }

        .module-eyebrow {
            font-size: 0.72rem;
            font-weight: 700;
            color: #006699;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 0.35rem;
        }

        .module-title {
            font-size: 1.15rem;
            font-weight: 600;
            color: #0F172A;
            margin-bottom: 0.5rem;
        }

        .module-desc {
            font-size: 0.875rem;
            color: #475569;
            line-height: 1.5;
            margin-bottom: 1rem;
        }

        /* -------------------------------------------------- */
        /* PREDICTION RESULT PANEL                           */
        /* -------------------------------------------------- */
        .result-panel {
            background-color: #F0F9FF;
            border: 1px solid #BAE6FD;
            border-left: 4px solid #006699;
            border-radius: 8px;
            padding: 1.5rem 1.75rem;
            margin-top: 1.25rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 1px 4px 0 rgba(0, 102, 153, 0.05);
        }

        .result-eyebrow {
            font-size: 0.72rem;
            font-weight: 700;
            color: #0369A1;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.35rem;
        }

        .result-player-title {
            font-size: 1.35rem;
            font-weight: 700;
            color: #0F172A;
            margin-bottom: 0.25rem;
        }

        .result-matchup-meta {
            font-size: 0.875rem;
            color: #475569;
            margin-bottom: 1.15rem;
        }

        .result-score-box {
            background-color: #FFFFFF;
            border: 1px solid #BAE6FD;
            border-radius: 6px;
            padding: 1rem 1.5rem;
            display: inline-block;
            margin-bottom: 0.85rem;
        }

        .result-score-label {
            font-size: 0.75rem;
            font-weight: 600;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        .result-score-val {
            font-size: 2.25rem;
            font-weight: 700;
            color: #006699;
            line-height: 1.1;
            margin-top: 0.2rem;
            margin-bottom: 0.1rem;
            font-feature-settings: "tnum";
        }

        .result-footer-text {
            font-size: 0.8rem;
            color: #64748B;
            line-height: 1.45;
        }

        /* -------------------------------------------------- */
        /* PLAYER BANNER (ANALYTICS)                         */
        /* -------------------------------------------------- */
        .player-banner {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-left: 4px solid #006699;
            border-radius: 8px;
            padding: 1.25rem 1.5rem;
            margin-bottom: 1.25rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.03);
        }

        .player-banner-eyebrow {
            font-size: 0.72rem;
            font-weight: 700;
            color: #0369A1;
            text-transform: uppercase;
            letter-spacing: 0.07em;
            margin-bottom: 0.2rem;
        }

        .player-banner-name {
            font-size: 1.5rem;
            font-weight: 700;
            color: #0F172A;
            letter-spacing: -0.01em;
            margin-bottom: 0.25rem;
        }

        .player-banner-meta {
            font-size: 0.85rem;
            color: #64748B;
        }

        /* -------------------------------------------------- */
        /* CHART CONTAINER CARD                              */
        /* -------------------------------------------------- */
        .chart-container-card {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 1.25rem 1.25rem 0.75rem 1.25rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.02);
        }

        .chart-header-title {
            font-size: 0.95rem;
            font-weight: 600;
            color: #0F172A;
            margin-bottom: 0.15rem;
        }

        .chart-header-sub {
            font-size: 0.8rem;
            color: #64748B;
            margin-bottom: 0.5rem;
        }

        /* -------------------------------------------------- */
        /* SIDEBAR STYLING                                    */
        /* -------------------------------------------------- */
        section[data-testid="stSidebar"] {
            background-color: #F8FAFC;
            border-right: 1px solid #E2E8F0;
        }

        .sidebar-brand-wrapper {
            padding: 0.5rem 0 1rem 0;
            border-bottom: 1px solid #E2E8F0;
            margin-bottom: 1.25rem;
        }

        .sidebar-brand-title {
            font-size: 0.75rem;
            font-weight: 700;
            color: #006699;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 0.2rem;
        }

        .sidebar-brand-sub {
            font-size: 1.15rem;
            font-weight: 700;
            color: #0F172A;
            line-height: 1.2;
            letter-spacing: -0.01em;
            margin-bottom: 0.5rem;
        }

        .sidebar-badge {
            display: inline-block;
            font-size: 0.72rem;
            font-weight: 600;
            background-color: #E0F2FE;
            color: #0369A1;
            padding: 3px 8px;
            border-radius: 4px;
            letter-spacing: 0.02em;
        }

        .sidebar-footer {
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid #E2E8F0;
            font-size: 0.75rem;
            color: #64748B;
            line-height: 1.55;
        }

        .sidebar-footer strong {
            color: #334155;
        }

        /* Sidebar Navigation Active & Hover Enhancement */
        div[data-testid="stSidebarNav"] li {
            margin-bottom: 0.2rem;
        }

        div[data-testid="stSidebarNav"] li a {
            border-radius: 6px;
            padding: 0.45rem 0.75rem;
            font-size: 0.875rem;
            font-weight: 500;
            color: #475569;
            transition: all 0.15s ease;
        }

        div[data-testid="stSidebarNav"] li a:hover {
            background-color: #F1F5F9;
            color: #0F172A;
        }

        div[data-testid="stSidebarNav"] li a[aria-current="page"] {
            background-color: #E0F2FE !important;
            color: #006699 !important;
            font-weight: 600 !important;
            border-left: 3px solid #006699;
        }

        /* -------------------------------------------------- */
        /* STREAMLIT NATIVE METRIC CARDS                      */
        /* -------------------------------------------------- */
        div[data-testid="stMetric"] {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 0.85rem 1rem;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.02);
            transition: border-color 0.15s ease;
        }

        div[data-testid="stMetric"]:hover {
            border-color: #CBD5E1;
        }

        div[data-testid="stMetricLabel"] p {
            font-size: 0.75rem !important;
            font-weight: 600 !important;
            color: #64748B !important;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-bottom: 0.25rem !important;
        }

        div[data-testid="stMetricValue"] div {
            font-size: 1.45rem !important;
            font-weight: 700 !important;
            color: #0F172A !important;
            font-feature-settings: "tnum";
        }

        /* -------------------------------------------------- */
        /* INPUT CONTROLS & BUTTONS                           */
        /* -------------------------------------------------- */
        div[data-baseweb="select"] > div {
            border-color: #CBD5E1;
            border-radius: 6px;
            transition: border-color 0.15s ease, box-shadow 0.15s ease;
        }

        div[data-baseweb="select"] > div:focus-within {
            border-color: #0284C7 !important;
            box-shadow: 0 0 0 2px rgba(2, 132, 199, 0.15) !important;
        }

        div.stButton > button:first-child {
            background-color: #006699;
            color: #FFFFFF;
            font-weight: 600;
            font-size: 0.95rem;
            border: none;
            border-radius: 6px;
            padding: 0.6rem 1.75rem;
            transition: all 0.18s ease-in-out;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
        }

        div.stButton > button:first-child:hover {
            background-color: #004C73;
            color: #FFFFFF;
            border: none;
            box-shadow: 0 3px 6px rgba(0, 102, 153, 0.15);
            transform: translateY(-1px);
        }

        div.stButton > button:first-child:active {
            background-color: #003854;
            color: #FFFFFF;
            transform: translateY(0);
        }

        /* Dataframe styling */
        div[data-testid="stDataFrame"] {
            border: 1px solid #E2E8F0;
            border-radius: 6px;
            overflow: hidden;
        }
    </style>
    """, unsafe_allow_html=True)


def render_sidebar_header():
    """Renders clean sidebar branding."""
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-brand-wrapper">
            <div class="sidebar-brand-title">Cricket Performance</div>
            <div class="sidebar-brand-sub">Analytics Platform</div>
            <div class="sidebar-badge">IPL Machine Learning Intelligence</div>
        </div>
        """, unsafe_allow_html=True)


def render_sidebar_footer():
    """Renders clean project attribution and dataset provenance."""
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-footer">
            <strong>Project:</strong> Cricket Performance Analytics<br>
            <strong>Developer:</strong> Annu Tiwari<br>
            <strong>Dataset:</strong> IPL (2008–2024) via Cricsheet/Kaggle<br>
            <strong>Version:</strong> v2.0 Enterprise
        </div>
        """, unsafe_allow_html=True)


def render_page_header(eyebrow: str, title: str, subtitle: str):
    """Renders structured top-of-page header."""
    st.markdown(f"""
    <div class="page-header-container">
        <div class="page-eyebrow">{eyebrow}</div>
        <div class="page-title">{title}</div>
        <div class="page-subtitle">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)


def render_section_header(eyebrow: str, title: str, subtitle: str = ""):
    """Renders structured section title with category micro-eyebrow."""
    sub_html = f'<div class="section-subtitle">{subtitle}</div>' if subtitle else ''
    st.markdown(f"""
    <div class="section-header-block">
        <div class="section-eyebrow">{eyebrow}</div>
        <div class="section-title">{title}</div>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


def render_kpi_card(category: str, number: str, subtext: str):
    """Renders styled KPI card."""
    return f"""
    <div class="kpi-card">
        <div class="kpi-category">{category}</div>
        <div class="kpi-number">{number}</div>
        <div class="kpi-subtext">{subtext}</div>
    </div>
    """


def get_plotly_layout(title: str = "", height: int = 380, xaxis_title: str = None, yaxis_title: str = None):
    """Returns standardized Plotly enterprise layout config."""
    layout = {
        "title": {
            "text": title,
            "font": {"size": 13.5, "color": "#0F172A", "family": "Inter, sans-serif", "weight": 600}
        },
        "template": "plotly_white",
        "height": height,
        "margin": {"l": 45, "r": 25, "t": 45, "b": 45},
        "font": {"family": "Inter, sans-serif", "color": "#475569"},
        "xaxis": {
            "title": xaxis_title,
            "showgrid": True,
            "gridcolor": "#F1F5F9",
            "linecolor": "#CBD5E1",
            "tickfont": {"size": 11}
        },
        "yaxis": {
            "title": yaxis_title,
            "showgrid": True,
            "gridcolor": "#F1F5F9",
            "linecolor": "#CBD5E1",
            "tickfont": {"size": 11}
        },
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)"
    }
    return layout
