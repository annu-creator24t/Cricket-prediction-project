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

st.set_page_config(
    page_title="Cricket Performance Intelligence",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for clean, professional cricket dashboard
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 15px;
    }
    .metric-card h4 {
        margin-top: 0;
        color: #0F172A;
        font-size: 1.15rem;
    }
    .metric-card p {
        color: #475569;
        font-size: 0.95rem;
        margin-bottom: 0;
    }
    .status-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
        background-color: #DCFCE7;
        color: #166534;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# HEADER
# -------------------------------------------------------
st.markdown('<div class="main-title">🏏 Cricket Player Performance Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">End-to-End IPL Match Performance Forecasting & In-Depth Analytics</div>', unsafe_allow_html=True)

st.divider()

# -------------------------------------------------------
# MODULE CARDS
# -------------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h4>🎯 Match Performance Prediction</h4>
        <p>Forecast expected runs for batsmen and wickets for bowlers in upcoming fixtures using trained gradient-boosted regression pipelines.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h4>📊 Player Analytics & Breakdown</h4>
        <p>Comprehensive historical analysis including rolling 5/10 match averages, venue impacts, opponent matchups, and form volatility.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h4>🔍 Model Explainability (SHAP)</h4>
        <p>Transparent feature attribution explaining key predictive drivers like recent form, pitch venue, and career baseline trends.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# -------------------------------------------------------
# SYSTEM STATUS & DATASET OVERVIEW
# -------------------------------------------------------
st.subheader("System Status & Dataset Summary")

meta = load_dataset_metadata(PROJECT_ROOT)
total_batters = len(meta.get("batters", []))
total_bowlers = len(meta.get("bowlers", []))
total_teams = len(meta.get("teams", []))
total_venues = len(meta.get("venues", []))

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Tracked Batters", f"{total_batters:,}" if total_batters else "Loaded")
c2.metric("Tracked Bowlers", f"{total_bowlers:,}" if total_bowlers else "Loaded")
c3.metric("IPL Franchises", f"{total_teams}" if total_teams else "15+")
c4.metric("Match Venues", f"{total_venues}" if total_venues else "50+")
c5.metric("ML Engine", "Active (CatBoost/Ensemble)")

st.divider()

# -------------------------------------------------------
# QUICK NAVIGATION GUIDE
# -------------------------------------------------------
st.subheader("Getting Started")
st.markdown("""
1. **Match Prediction**: Navigate to **`1_Prediction`** from the left sidebar. Select a player (batter or bowler), review recent form parameters, and generate an immediate match forecast.
2. **Analytics Report**: Navigate to **`2_Analytics_Report`** from the left sidebar to explore historical trends, venue-specific averages, opponent head-to-head records, and SHAP explainability plots.
3. **Pipeline Retraining**: To retrain the regression models on updated data, execute `python main.py` in the terminal.
""")
