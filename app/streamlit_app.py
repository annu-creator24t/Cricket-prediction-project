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
from app.ui_theme import apply_custom_css, render_sidebar_header, render_sidebar_footer

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

# Header
st.title("Cricket Performance Analytics")
st.caption("IPL player match performance forecasting, historical analytics, and explainable AI insights.")
st.divider()

# Introduction
st.markdown("""
This project is an end-to-end Machine Learning web application developed as part of **Infosys Springboard**. 
It evaluates historical Indian Premier League (IPL) ball-by-ball records (2008–2024) to predict individual player match outcomes 
(expected runs for batsmen and expected wickets for bowlers) while providing interactive performance breakdowns and SHAP-based feature importance analysis.
""")

st.write("")

# -------------------------------------------------------
# DATASET & SYSTEM SUMMARY
# -------------------------------------------------------
st.subheader("Dataset Summary (IPL 2008–2024)")

meta = load_dataset_metadata(PROJECT_ROOT)
total_batters = len(meta.get("batters", []))
total_bowlers = len(meta.get("bowlers", []))
total_venues = len(meta.get("venues", []))

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Tracked Batters", f"{total_batters:,}" if total_batters else "285")
c2.metric("Tracked Bowlers", f"{total_bowlers:,}" if total_bowlers else "245")
c3.metric("Total IPL Matches", "1,100")
c4.metric("Seasons Covered", "2008–2024")
c5.metric("Match Venues", f"{total_venues}" if total_venues else "58")

st.divider()

# -------------------------------------------------------
# MODULES OVERVIEW
# -------------------------------------------------------
st.subheader("Application Modules")

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("""
    #### 1. Match Prediction
    - Select an individual batter or bowler and configure the upcoming match context (batting team, opponent, and venue).
    - Review auto-filled recent form parameters (previous match output, rolling 5-match average, rolling 10-match average, and career average).
    - Generate an immediate regression prediction comparing the expected score/wickets against the player's career baseline.
    """)

with col_b:
    st.markdown("""
    #### 2. Player Analytics
    - Examine historical match-by-match scoring timelines across recent fixtures.
    - Inspect score and wicket frequency distribution histograms.
    - Analyze venue-specific averages and opponent head-to-head records.
    - Review SHAP (SHapley Additive exPlanations) feature impact plots to understand model prediction drivers.
    """)

st.divider()

# -------------------------------------------------------
# MODEL BENCHMARKS
# -------------------------------------------------------
st.subheader("Model Evaluation Summary (Held-Out Test Set)")

eval_data = [
    {
        "Role / Target": "Batter (Runs Scored)",
        "Best Model": "CatBoost Regressor",
        "Test RMSE": "22.29",
        "Test MAE": "16.92",
        "Test R²": "0.098",
        "Baseline RMSE": "23.47"
    },
    {
        "Role / Target": "Bowler (Wickets Taken)",
        "Best Model": "CatBoost Regressor",
        "Test RMSE": "1.07",
        "Test MAE": "0.84",
        "Test R²": "0.019",
        "Baseline RMSE": "1.08"
    }
]
st.dataframe(pd.DataFrame(eval_data), use_container_width=True, hide_index=True)

st.caption("Models trained with a time-aware 80/20 train-test split on chronological match dates. Data source: Kaggle / Cricsheet open ball-by-ball IPL dataset.")

# Render sidebar footer
render_sidebar_footer()
