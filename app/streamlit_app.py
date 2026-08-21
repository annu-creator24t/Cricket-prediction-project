import os
import sys
import streamlit as st
import pandas as pd

# Path configuration for both local execution and Streamlit Community Cloud
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
APP_DIR = CURRENT_DIR

for p in [PROJECT_ROOT, APP_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from src.components.predictor import load_dataset_metadata
except ImportError:
    from components.predictor import load_dataset_metadata

try:
    from app.ui_theme import apply_custom_css, render_sidebar_header, render_sidebar_footer, render_kpi
except ImportError:
    from ui_theme import apply_custom_css, render_sidebar_header, render_sidebar_footer, render_kpi

# Page Configuration
st.set_page_config(
    page_title="Cricket Performance Analytics",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply styling & sidebar
apply_custom_css()
render_sidebar_header()

# -------------------------------------------------------
# HEADER
# -------------------------------------------------------
st.markdown("""
<div class="overview-header">
    <div class="page-title">Cricket Performance Analytics</div>
    <div class="page-subtitle">
        Predict and analyze individual IPL player performance using historical match data and recent form.
    </div>
</div>
""", unsafe_allow_html=True)

# Navigation Links
col_nav1, col_nav2, _ = st.columns([1.2, 1.2, 2.5])
with col_nav1:
    st.page_link("pages/1_Match_Prediction.py", label="Match Prediction →", use_container_width=True)
with col_nav2:
    st.page_link("pages/2_Player_Analytics.py", label="Player Analytics →", use_container_width=True)

st.write("")

# -------------------------------------------------------
# DATASET
# -------------------------------------------------------
st.markdown('<div class="section-title">Dataset Summary (IPL 2008–2024)</div>', unsafe_allow_html=True)
st.markdown('<div class="section-desc">Historical ball-by-ball match records used for training and player statistics.</div>', unsafe_allow_html=True)

meta = load_dataset_metadata(PROJECT_ROOT)
total_batters = len(meta.get("batters", []))
total_bowlers = len(meta.get("bowlers", []))
total_venues = len(meta.get("venues", []))

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.markdown(render_kpi("Tracked Batters", f"{total_batters:,}" if total_batters else "285", "Player records"), unsafe_allow_html=True)
with c2:
    st.markdown(render_kpi("Tracked Bowlers", f"{total_bowlers:,}" if total_bowlers else "245", "Player records"), unsafe_allow_html=True)
with c3:
    st.markdown(render_kpi("IPL Matches", "1,100", "Ball-by-ball fixtures"), unsafe_allow_html=True)
with c4:
    st.markdown(render_kpi("Seasons", "2008–2024", "17 tournament editions"), unsafe_allow_html=True)
with c5:
    st.markdown(render_kpi("Match Venues", f"{total_venues}" if total_venues else "58", "Standardized grounds"), unsafe_allow_html=True)

st.write("")
st.divider()

# -------------------------------------------------------
# AVAILABLE ANALYSIS
# -------------------------------------------------------
st.markdown('<div class="section-title">Available Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="section-desc">Select an analysis workflow:</div>', unsafe_allow_html=True)

col_m1, col_m2 = st.columns(2)

with col_m1:
    st.markdown("""
    <div class="feature-box">
        <h4>Match Prediction</h4>
        <p>
            Configure player, opponent, and venue to generate expected runs or wickets 
            evaluated against recent 5-match, 10-match, and career averages.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_Match_Prediction.py", label="Open Match Prediction →", use_container_width=True)

with col_m2:
    st.markdown("""
    <div class="feature-box">
        <h4>Player Analytics</h4>
        <p>
            Review match-by-match output timelines, scoring distributions, venue statistics, 
            head-to-head opposition records, and model feature importance.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_Player_Analytics.py", label="Open Player Analytics →", use_container_width=True)

st.write("")
st.divider()

# -------------------------------------------------------
# MODEL EVALUATION
# -------------------------------------------------------
st.markdown('<div class="section-title">Model Evaluation</div>', unsafe_allow_html=True)
st.markdown('<div class="section-desc">Performance of trained regression models evaluated on the held-out test set (80/20 chronological split).</div>', unsafe_allow_html=True)

eval_data = [
    {
        "Role / Target": "Batter (Runs Scored)",
        "Model": "CatBoost Regressor",
        "Test RMSE": "22.29",
        "Test MAE": "16.92",
        "Test R²": "0.098",
        "Baseline RMSE": "23.47"
    },
    {
        "Role / Target": "Bowler (Wickets Taken)",
        "Model": "CatBoost Regressor",
        "Test RMSE": "1.07",
        "Test MAE": "0.84",
        "Test R²": "0.019",
        "Baseline RMSE": "1.08"
    }
]

st.dataframe(pd.DataFrame(eval_data), use_container_width=True, hide_index=True)

st.caption("Data source: Kaggle and Cricsheet ball-by-ball IPL dataset.")

# Render sidebar footer
render_sidebar_footer()
