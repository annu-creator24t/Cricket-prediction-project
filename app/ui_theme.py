import streamlit as st

def apply_custom_css():
    """Injects clean, professional CSS across all Streamlit pages."""
    st.markdown("""
    <style>
        /* Typography & base fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            color: #1E293B;
            -webkit-font-smoothing: antialiased;
        }

        /* Hide Streamlit default Deploy button, top header & main menu */
        #MainMenu {visibility: hidden; display: none !important;}
        footer {visibility: hidden; display: none !important;}
        header[data-testid="stHeader"] {background: transparent; height: 0; min-height: 0;}
        .stDeployButton {display: none !important;}
        button[data-testid="stDeployButton"] {display: none !important;}
        div[data-testid="stToolbar"] {display: none !important;}
        div[data-testid="stDecoration"] {display: none !important;}
        div[data-testid="stStatusWidget"] {display: none !important;}
        div[data-testid="stHeaderActionElements"] {display: none !important;}

        /* Page layout container */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 3rem !important;
            max-width: 1140px;
        }

        /* Page title & subtitle */
        .page-title {
            font-size: 1.85rem;
            font-weight: 700;
            color: #0F172A;
            letter-spacing: -0.02em;
            margin-bottom: 0.25rem;
            line-height: 1.25;
        }

        .page-subtitle {
            font-size: 0.95rem;
            font-weight: 400;
            color: #64748B;
            margin-bottom: 1.5rem;
            line-height: 1.5;
        }

        /* Section Headings */
        .section-title {
            font-size: 1.15rem;
            font-weight: 600;
            color: #0F172A;
            margin-top: 1.25rem;
            margin-bottom: 0.25rem;
            letter-spacing: -0.01em;
        }

        .section-desc {
            font-size: 0.875rem;
            color: #64748B;
            margin-bottom: 1rem;
            line-height: 1.45;
        }

        /* Hero / Overview Header */
        .overview-header {
            padding-bottom: 1rem;
            margin-bottom: 1.25rem;
            border-bottom: 1px solid #E2E8F0;
        }

        /* Neutral KPI Item */
        .kpi-block {
            background-color: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 6px;
            padding: 0.85rem 1rem;
            height: 100%;
        }

        .kpi-block-label {
            font-size: 0.75rem;
            font-weight: 500;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-bottom: 0.25rem;
        }

        .kpi-block-value {
            font-size: 1.55rem;
            font-weight: 700;
            color: #0F172A;
            line-height: 1.2;
            font-feature-settings: "tnum";
        }

        .kpi-block-desc {
            font-size: 0.75rem;
            color: #64748B;
            margin-top: 0.2rem;
        }

        /* Overview Feature Box */
        .feature-box {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 6px;
            padding: 1.25rem;
            margin-bottom: 0.75rem;
            height: 100%;
        }

        .feature-box h4 {
            font-size: 1.05rem;
            font-weight: 600;
            color: #0F172A;
            margin-top: 0;
            margin-bottom: 0.4rem;
        }

        .feature-box p {
            font-size: 0.875rem;
            color: #475569;
            line-height: 1.5;
            margin-bottom: 0;
        }

        /* Prediction Result Panel */
        .result-panel {
            background-color: #F8FAFC;
            border: 1px solid #CBD5E1;
            border-left: 4px solid #006699;
            border-radius: 6px;
            padding: 1.25rem 1.5rem;
            margin-top: 1rem;
            margin-bottom: 1.25rem;
        }

        .result-player-title {
            font-size: 1.2rem;
            font-weight: 700;
            color: #0F172A;
            margin-bottom: 0.2rem;
        }

        .result-matchup-meta {
            font-size: 0.85rem;
            color: #475569;
            margin-bottom: 1rem;
        }

        .result-score-val {
            font-size: 2rem;
            font-weight: 700;
            color: #006699;
            line-height: 1.1;
            margin: 0.2rem 0;
            font-feature-settings: "tnum";
        }

        .result-empty-placeholder {
            background-color: #F8FAFC;
            border: 1px dashed #CBD5E1;
            border-radius: 6px;
            padding: 1.5rem;
            text-align: center;
            color: #64748B;
            font-size: 0.875rem;
            margin-top: 1rem;
            margin-bottom: 1.25rem;
        }

        /* Player Profile Header (Analytics) */
        .player-header {
            padding: 0.75rem 0 1rem 0;
            border-bottom: 1px solid #E2E8F0;
            margin-bottom: 1.25rem;
        }

        .player-name {
            font-size: 1.5rem;
            font-weight: 700;
            color: #0F172A;
            margin-bottom: 0.15rem;
        }

        .player-meta {
            font-size: 0.875rem;
            color: #64748B;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #F8FAFC;
            border-right: 1px solid #E2E8F0;
        }

        .sidebar-brand-wrapper {
            padding: 0.5rem 0 0.85rem 0;
            border-bottom: 1px solid #E2E8F0;
            margin-bottom: 1rem;
        }

        .sidebar-brand-title {
            font-size: 1rem;
            font-weight: 700;
            color: #0F172A;
            line-height: 1.2;
            margin-bottom: 0.15rem;
        }

        .sidebar-brand-sub {
            font-size: 0.8rem;
            color: #64748B;
        }

        .sidebar-footer {
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid #E2E8F0;
            font-size: 0.75rem;
            color: #64748B;
            line-height: 1.5;
        }

        .sidebar-footer strong {
            color: #334155;
        }

        /* Sidebar Navigation Active State */
        div[data-testid="stSidebarNav"] li a {
            border-radius: 4px;
            padding: 0.45rem 0.65rem;
            font-size: 0.875rem;
            color: #475569;
        }

        div[data-testid="stSidebarNav"] li a[aria-current="page"] {
            background-color: #E0F2FE !important;
            color: #006699 !important;
            font-weight: 600 !important;
        }

        /* Streamlit metric adjustments */
        div[data-testid="stMetric"] {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 6px;
            padding: 0.75rem 0.9rem;
        }

        div[data-testid="stMetricLabel"] p {
            font-size: 0.75rem !important;
            font-weight: 500 !important;
            color: #64748B !important;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }

        div[data-testid="stMetricValue"] div {
            font-size: 1.35rem !important;
            font-weight: 700 !important;
            color: #0F172A !important;
        }

        /* Buttons */
        div.stButton > button:first-child {
            background-color: #006699;
            color: #FFFFFF;
            font-weight: 600;
            font-size: 0.9rem;
            border: none;
            border-radius: 5px;
            padding: 0.55rem 1.4rem;
            transition: background-color 0.15s ease;
        }

        div.stButton > button:first-child:hover {
            background-color: #004C73;
            color: #FFFFFF;
        }

        /* Tables & Charts */
        div[data-testid="stDataFrame"] {
            border: 1px solid #E2E8F0;
            border-radius: 5px;
        }
    </style>
    """, unsafe_allow_html=True)


def render_sidebar_header():
    """Renders simple, professional sidebar branding."""
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-brand-wrapper">
            <div class="sidebar-brand-title">Cricket Performance Analytics</div>
            <div class="sidebar-brand-sub">IPL Player Analysis</div>
        </div>
        """, unsafe_allow_html=True)


def render_sidebar_footer():
    """Renders project attribution and dataset source."""
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-footer">
            <strong>Project:</strong> Cricket Performance Analytics<br>
            <strong>Developer:</strong> Annu Tiwari<br>
            <strong>Dataset:</strong> IPL (2008–2024) via Cricsheet & Kaggle
        </div>
        """, unsafe_allow_html=True)


def render_kpi(label: str, value: str, note: str = ""):
    """Renders restrained, clean KPI block."""
    note_html = f'<div class="kpi-block-desc">{note}</div>' if note else ''
    return f"""
    <div class="kpi-block">
        <div class="kpi-block-label">{label}</div>
        <div class="kpi-block-value">{value}</div>
        {note_html}
    </div>
    """


def get_plotly_layout(title: str = "", height: int = 360, xaxis_title: str = None, yaxis_title: str = None):
    """Standardized clean Plotly layout configuration."""
    layout = {
        "title": {
            "text": title,
            "font": {"size": 13, "color": "#0F172A", "family": "Inter, sans-serif", "weight": 600}
        },
        "template": "plotly_white",
        "height": height,
        "margin": {"l": 50, "r": 25, "t": 40, "b": 40},
        "font": {"family": "Inter, sans-serif", "color": "#475569", "size": 11},
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
