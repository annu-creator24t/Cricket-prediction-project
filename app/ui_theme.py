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
        }

        /* Top header padding normalization */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 3rem !important;
            max-width: 1200px;
        }

        /* Typography Hierarchy */
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
            margin-bottom: 1.25rem;
            line-height: 1.5;
        }

        .section-title {
            font-size: 1.2rem;
            font-weight: 600;
            color: #0F172A;
            margin-top: 1rem;
            margin-bottom: 0.75rem;
            letter-spacing: -0.01em;
        }

        .section-subtitle {
            font-size: 0.875rem;
            color: #64748B;
            margin-bottom: 1rem;
        }

        /* Enterprise Cards */
        .enterprise-card {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 1.25rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04);
            height: 100%;
        }

        .enterprise-card h4 {
            font-size: 1rem;
            font-weight: 600;
            color: #006699;
            margin-top: 0;
            margin-bottom: 0.5rem;
        }

        .enterprise-card p {
            font-size: 0.875rem;
            color: #475569;
            line-height: 1.45;
            margin-bottom: 0;
        }

        /* Step Guide Cards */
        .step-card {
            background-color: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 1rem 1.25rem;
            margin-bottom: 0.75rem;
        }

        .step-number {
            display: inline-block;
            font-size: 0.75rem;
            font-weight: 700;
            color: #006699;
            background-color: #E0F2FE;
            padding: 2px 8px;
            border-radius: 4px;
            margin-bottom: 0.35rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .step-title {
            font-size: 0.95rem;
            font-weight: 600;
            color: #0F172A;
            margin-bottom: 0.2rem;
        }

        .step-desc {
            font-size: 0.85rem;
            color: #64748B;
            margin-bottom: 0;
            line-height: 1.4;
        }

        /* Prediction Result Box */
        .result-container {
            background-color: #F0F9FF;
            border: 1px solid #BAE6FD;
            border-left: 4px solid #006699;
            border-radius: 6px;
            padding: 1.25rem;
            margin-top: 1rem;
            margin-bottom: 1.5rem;
        }

        .result-player-name {
            font-size: 1.1rem;
            font-weight: 600;
            color: #0369A1;
            margin-bottom: 0.25rem;
        }

        .result-metric-label {
            font-size: 0.85rem;
            font-weight: 500;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .result-metric-val {
            font-size: 2rem;
            font-weight: 700;
            color: #0F172A;
            line-height: 1.1;
            margin-top: 0.2rem;
            margin-bottom: 0.5rem;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #F8FAFC;
            border-right: 1px solid #E2E8F0;
        }

        .sidebar-brand-title {
            font-size: 0.85rem;
            font-weight: 700;
            color: #006699;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            margin-bottom: 0.15rem;
        }

        .sidebar-brand-sub {
            font-size: 1.1rem;
            font-weight: 700;
            color: #0F172A;
            line-height: 1.2;
            margin-bottom: 0.5rem;
        }

        .sidebar-badge {
            display: inline-block;
            font-size: 0.7rem;
            font-weight: 600;
            background-color: #E2E8F0;
            color: #475569;
            padding: 2px 8px;
            border-radius: 4px;
            margin-bottom: 1rem;
        }

        .sidebar-footer {
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid #E2E8F0;
            font-size: 0.75rem;
            color: #94A3B8;
            line-height: 1.4;
        }

        /* Streamlit native metric card enhancement */
        div[data-testid="stMetric"] {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 0.85rem 1rem;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
        }

        div[data-testid="stMetricLabel"] p {
            font-size: 0.8rem !important;
            font-weight: 500 !important;
            color: #64748B !important;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }

        div[data-testid="stMetricValue"] div {
            font-size: 1.4rem !important;
            font-weight: 700 !important;
            color: #0F172A !important;
        }

        /* Buttons */
        div.stButton > button:first-child {
            background-color: #006699;
            color: #FFFFFF;
            font-weight: 600;
            font-size: 0.95rem;
            border: none;
            border-radius: 6px;
            padding: 0.55rem 1.5rem;
            transition: all 0.15s ease-in-out;
        }

        div.stButton > button:first-child:hover {
            background-color: #004C73;
            color: #FFFFFF;
            border: none;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        div.stButton > button:first-child:active {
            background-color: #003854;
            color: #FFFFFF;
        }

        /* Form Inputs */
        div[data-baseweb="select"] > div {
            border-color: #CBD5E1;
            border-radius: 6px;
        }

        input[type="number"], input[type="text"] {
            border-color: #CBD5E1 !important;
            border-radius: 6px !important;
        }
    </style>
    """, unsafe_allow_html=True)


def render_sidebar_header():
    """Renders clean corporate sidebar branding."""
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-brand-title">Cricket Performance</div>
        <div class="sidebar-brand-sub">Analytics</div>
        <div class="sidebar-badge">Infosys Springboard Project</div>
        """, unsafe_allow_html=True)


def render_sidebar_footer():
    """Renders consistent sidebar footer."""
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-footer">
            Cricket Analytics Platform<br>
            Developed for Infosys Springboard Evaluation
        </div>
        """, unsafe_allow_html=True)


def get_plotly_layout(title: str = "", height: int = 380, xaxis_title: str = None, yaxis_title: str = None):
    """Returns standardized Plotly enterprise layout config."""
    layout = {
        "title": {
            "text": title,
            "font": {"size": 14, "color": "#0F172A", "family": "Inter, sans-serif"}
        },
        "template": "plotly_white",
        "height": height,
        "margin": {"l": 40, "r": 20, "t": 40, "b": 40},
        "font": {"family": "Inter, sans-serif", "color": "#475569"},
        "xaxis": {
            "title": xaxis_title,
            "showgrid": True,
            "gridcolor": "#F1F5F9",
            "linecolor": "#CBD5E1"
        },
        "yaxis": {
            "title": yaxis_title,
            "showgrid": True,
            "gridcolor": "#F1F5F9",
            "linecolor": "#CBD5E1"
        },
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)"
    }
    return layout
