import os
import sys
import streamlit as st

# Add project root to sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.components.predictor import load_dataset_metadata
from app.ui_theme import apply_custom_css, render_sidebar_header, render_sidebar_footer

# Page Configuration
st.set_page_config(
    page_title="Cricket Performance Analytics — Overview",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply unified design system
apply_custom_css()
render_sidebar_header()

# -------------------------------------------------------
# HEADER
# -------------------------------------------------------
st.markdown('<div class="page-title">Cricket Performance Analytics</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="page-subtitle">IPL player performance prediction and historical analytics.</div>',
    unsafe_allow_html=True
)
st.divider()

# -------------------------------------------------------
# CAPABILITY SUMMARY
# -------------------------------------------------------
st.markdown('<div class="section-title">Core Capabilities</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="enterprise-card">
        <h4>Match Prediction</h4>
        <p>Predict expected individual player performance (runs scored for batters, wickets taken for bowlers) using historical match data and gradient-boosted regression pipelines.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="enterprise-card">
        <h4>Player Analytics</h4>
        <p>Explore recent form, rolling 5/10 match moving averages, match-by-match trends, venue-specific averages, opponent head-to-head records, and volatility metrics.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="enterprise-card">
        <h4>Model Insights</h4>
        <p>Understand the key factors contributing to model predictions through SHAP (SHapley Additive exPlanations) feature attribution and global importance rankings.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# -------------------------------------------------------
# DATASET & SYSTEM SUMMARY
# -------------------------------------------------------
st.markdown('<div class="section-title">System Status & Dataset Summary</div>', unsafe_allow_html=True)

meta = load_dataset_metadata(PROJECT_ROOT)
total_batters = len(meta.get("batters", []))
total_bowlers = len(meta.get("bowlers", []))
total_teams = len(meta.get("teams", []))
total_venues = len(meta.get("venues", []))

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Tracked Batters", f"{total_batters:,}" if total_batters else "285")
c2.metric("Tracked Bowlers", f"{total_bowlers:,}" if total_bowlers else "245")
c3.metric("IPL Franchises", f"{total_teams}" if total_teams else "18")
c4.metric("Match Venues", f"{total_venues}" if total_venues else "58")
c5.metric("ML Engine", "Active")

st.divider()

# -------------------------------------------------------
# GETTING STARTED WORKFLOW
# -------------------------------------------------------
st.markdown('<div class="section-title">Getting Started</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Follow these three steps to evaluate player performance:</div>', unsafe_allow_html=True)

s1, s2, s3 = st.columns(3)

with s1:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">Step 01</div>
        <div class="step-title">Select a Player</div>
        <div class="step-desc">Navigate to <strong>Match Prediction</strong> and select the player role (Batter or Bowler) along with the player name.</div>
    </div>
    """, unsafe_allow_html=True)

with s2:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">Step 02</div>
        <div class="step-title">Provide Match Context</div>
        <div class="step-desc">Review the auto-filled historical form metrics, select the batting/bowling team, opponent, and match venue.</div>
    </div>
    """, unsafe_allow_html=True)

with s3:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">Step 03</div>
        <div class="step-title">Generate Prediction</div>
        <div class="step-desc">Run the inference model to calculate the expected performance and inspect the historical benchmark comparison.</div>
    </div>
    """, unsafe_allow_html=True)

# Render consistent sidebar footer
render_sidebar_footer()
