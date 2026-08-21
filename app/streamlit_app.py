import os
import sys
import streamlit as st
import pandas as pd

# Add project root to sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.components.predictor import load_dataset_metadata
from app.ui_theme import (
    apply_custom_css,
    render_sidebar_header,
    render_sidebar_footer,
    render_section_header,
    render_kpi_card
)

# Page Configuration
st.set_page_config(
    page_title="Cricket Performance Analytics",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply unified styling & sidebar
apply_custom_css()
render_sidebar_header()

# -------------------------------------------------------
# PRODUCT HERO BANNER
# -------------------------------------------------------
st.markdown("""
<div class="hero-banner">
    <div class="hero-badge">IPL Performance Intelligence Platform</div>
    <div class="hero-title">Cricket Performance Analytics</div>
    <div class="hero-desc">
        Predict individual player match outcomes (expected runs for batters and wickets for bowlers) 
        using historical IPL ball-by-ball data (2008–2024), player form trajectories, and match context.
    </div>
</div>
""", unsafe_allow_html=True)

# Quick action links
col_act1, col_act2, _ = st.columns([1.2, 1.2, 2.5])
with col_act1:
    st.page_link("pages/1_Match_Prediction.py", label="Open Match Prediction", icon="🎯", use_container_width=True)
with col_act2:
    st.page_link("pages/2_Player_Analytics.py", label="Explore Player Analytics", icon="📊", use_container_width=True)

st.write("")

# -------------------------------------------------------
# DATASET KPI SECTION
# -------------------------------------------------------
render_section_header(
    eyebrow="Dataset Overview",
    title="Historical Dataset Metrics (IPL 2008–2024)",
    subtitle="Standardized ball-by-ball historical records used for model training and performance profiling."
)

meta = load_dataset_metadata(PROJECT_ROOT)
total_batters = len(meta.get("batters", []))
total_bowlers = len(meta.get("bowlers", []))
total_venues = len(meta.get("venues", []))

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.markdown(render_kpi_card(
        category="Tracked Batters",
        number=f"{total_batters:,}" if total_batters else "285",
        subtext="Eligible IPL batters"
    ), unsafe_allow_html=True)

with c2:
    st.markdown(render_kpi_card(
        category="Tracked Bowlers",
        number=f"{total_bowlers:,}" if total_bowlers else "245",
        subtext="Eligible IPL bowlers"
    ), unsafe_allow_html=True)

with c3:
    st.markdown(render_kpi_card(
        category="IPL Matches",
        number="1,100",
        subtext="Ball-by-ball fixtures"
    ), unsafe_allow_html=True)

with c4:
    st.markdown(render_kpi_card(
        category="Seasons Covered",
        number="2008–2024",
        subtext="17 tournament editions"
    ), unsafe_allow_html=True)

with c5:
    st.markdown(render_kpi_card(
        category="Match Venues",
        number=f"{total_venues}" if total_venues else "58",
        subtext="Standardized grounds"
    ), unsafe_allow_html=True)

st.write("")

# -------------------------------------------------------
# APPLICATION MODULES
# -------------------------------------------------------
render_section_header(
    eyebrow="Core Capabilities",
    title="Application Modules",
    subtitle="Navigate to prediction forecasting and deep-dive statistical analytics."
)

col_mod1, col_mod2 = st.columns(2)

with col_mod1:
    st.markdown("""
    <div class="module-card">
        <div>
            <div class="module-eyebrow">Module 01</div>
            <div class="module-title">Match Performance Prediction</div>
            <div class="module-desc">
                Configure upcoming match context (batting team, bowling opponent, and venue) 
                to forecast player performance. Auto-fills rolling 5-match, 10-match, and career form metrics 
                with instant regression projections.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_Match_Prediction.py", label="Launch Prediction Engine →", use_container_width=True)

with col_mod2:
    st.markdown("""
    <div class="module-card">
        <div>
            <div class="module-eyebrow">Module 02</div>
            <div class="module-title">Player Performance Analytics</div>
            <div class="module-desc">
                Analyze individual match output timelines, frequency distributions, venue-specific averages, 
                and opposition head-to-head records alongside SHAP-based feature importance explainability.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_Player_Analytics.py", label="Explore Analytics & SHAP →", use_container_width=True)

st.write("")

# -------------------------------------------------------
# MODEL BENCHMARKS
# -------------------------------------------------------
render_section_header(
    eyebrow="Model Validation",
    title="Evaluation Benchmarks (Held-Out Test Set)",
    subtitle="Performance comparison of trained regression models against historical baseline metrics."
)

eval_data = [
    {
        "Target Role": "Batter (Runs Scored)",
        "Model Architecture": "CatBoost Regressor",
        "Test RMSE": "22.29",
        "Test MAE": "16.92",
        "Test R²": "0.098",
        "Baseline RMSE": "23.47"
    },
    {
        "Target Role": "Bowler (Wickets Taken)",
        "Model Architecture": "CatBoost Regressor",
        "Test RMSE": "1.07",
        "Test MAE": "0.84",
        "Test R²": "0.019",
        "Baseline RMSE": "1.08"
    }
]

st.dataframe(pd.DataFrame(eval_data), use_container_width=True, hide_index=True)

st.caption("Evaluation conducted on a chronological 80/20 train/test split. Data source: Kaggle & Cricsheet open ball-by-ball IPL dataset.")

# Render sidebar footer
render_sidebar_footer()
