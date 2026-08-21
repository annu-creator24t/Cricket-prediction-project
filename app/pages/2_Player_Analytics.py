import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

# Add project root to sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.components.predictor import get_player_stats, load_dataset_metadata
from app.ui_theme import (
    apply_custom_css,
    render_sidebar_header,
    render_sidebar_footer,
    render_page_header,
    render_section_header,
    get_plotly_layout
)

# Page Configuration
st.set_page_config(
    page_title="Player Analytics — Cricket Performance Analytics",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply styling & sidebar
apply_custom_css()
render_sidebar_header()

# Header
render_page_header(
    eyebrow="Intelligence & Diagnostics",
    title="Player Performance Analytics",
    subtitle="Historical trends, scoring distributions, opponent & venue breakdowns, and SHAP explainability insights."
)

# -------------------------------------------------------------
# 1. PLAYER SELECTION
# -------------------------------------------------------------
render_section_header(
    eyebrow="Step 01",
    title="Select Player Profile",
    subtitle="Choose discipline role and player to load historical performance analytics."
)

col_role, col_player = st.columns([1, 2.5])

with col_role:
    role = st.selectbox("Player Role", ["Batter", "Bowler"], index=0)
    role_key = role.lower()

# Load processed dataset
data_path = os.path.join(PROJECT_ROOT, "artifacts", "processed", f"{role_key}_training_data.csv")
summary_path = os.path.join(PROJECT_ROOT, "artifacts", "shap", f"{role_key}_shap_summary.png")
importance_path = os.path.join(PROJECT_ROOT, "artifacts", "shap", f"{role_key}_shap_importance.png")

if not os.path.exists(data_path):
    st.error(f"Dataset not found at `{data_path}`. Please verify artifacts path.")
    st.stop()

df = pd.read_csv(data_path)
player_col = "batsman" if role_key == "batter" else "bowler"
value_col = "runs" if role_key == "batter" else "wickets"
opponent_col = "bowling_team" if role_key == "batter" else "batting_team"
unit_label = "Runs" if role_key == "batter" else "Wickets"

available_players = sorted(df[player_col].dropna().unique().tolist())
default_player = "V Kohli" if role_key == "batter" and "V Kohli" in available_players else (
    "JJ Bumrah" if role_key == "bowler" and "JJ Bumrah" in available_players else available_players[0]
)
default_idx = available_players.index(default_player) if default_player in available_players else 0

with col_player:
    player = st.selectbox("Select Player", available_players, index=default_idx)

# Use unified stats computation
player_stats = get_player_stats(player, role_key, PROJECT_ROOT)
player_df = df[df[player_col] == player].sort_values("date")

if len(player_df) < 3 or not player_stats:
    st.warning("Insufficient match history for detailed statistical analysis (minimum 3 matches required).")
    st.stop()

last_team = player_stats.get("last_team", "IPL Franchise")
total_matches = len(player_df)

# -------------------------------------------------------------
# PLAYER IDENTITY HEADER
# -------------------------------------------------------------
st.markdown(f"""
<div class="player-banner">
    <div class="player-banner-eyebrow">Player Profile &bull; {role}</div>
    <div class="player-banner-name">{player}</div>
    <div class="player-banner-meta">
        Franchise: <strong>{last_team}</strong> &bull; Total Tracked Matches: <strong>{total_matches}</strong> &bull; Career Dataset: <strong>IPL 2008–2024</strong>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 2. PERFORMANCE SNAPSHOT
# -------------------------------------------------------------
render_section_header(
    eyebrow="Form Snapshot",
    title=f"Performance Benchmarks ({player})",
    subtitle="Recent match output compared against short-term, medium-term, and career averages."
)

last_match_val = player_stats["prev_runs"] if role_key == "batter" else player_stats["prev_wickets"]
last_5_avg = player_stats["last_5_avg"] if role_key == "batter" else player_stats["last_5_wkts"]
last_10_avg = player_stats["last_10_avg"] if role_key == "batter" else player_stats["last_10_wkts"]
career_avg = player_stats["career_avg"] if role_key == "batter" else player_stats["career_wkt_avg"]

k1, k2, k3, k4 = st.columns(4)
k1.metric("Last Match Output", f"{last_match_val:.0f} {unit_label}")
k2.metric("Last 5 Matches Avg", f"{last_5_avg:.2f} {unit_label}")
k3.metric("Last 10 Matches Avg", f"{last_10_avg:.2f} {unit_label}")
k4.metric("Career Average", f"{career_avg:.2f} {unit_label}")

st.write("")

# -------------------------------------------------------------
# 3. RECENT TREND & PERFORMANCE DISTRIBUTION
# -------------------------------------------------------------
col_trend, col_dist = st.columns(2)

with col_trend:
    st.markdown("""
    <div class="chart-container-card">
        <div class="chart-header-title">Recent Match Trend (Last 15 Fixtures)</div>
        <div class="chart-header-sub">Chronological scoring timeline across recent tournament appearances</div>
    </div>
    """, unsafe_allow_html=True)

    trend_df = player_df.tail(15).copy()
    trend_df["match_seq"] = [f"M{i+1}" for i in range(len(trend_df))]
    
    fig1 = px.line(
        trend_df,
        x="match_seq",
        y=value_col,
        markers=True,
        hover_data={"date": True, value_col: True, "venue": True},
        labels={"match_seq": "Match Sequence (Chronological)", value_col: unit_label, "date": "Date"}
    )
    fig1.update_traces(
        line_color="#006699",
        line_width=2.5,
        marker=dict(size=6, color="#004C73")
    )
    layout1 = get_plotly_layout(
        title=f"{player} — Match Output Timeline",
        height=350,
        xaxis_title="Match Sequence (Recent Fixtures)",
        yaxis_title=unit_label
    )
    fig1.update_layout(**layout1)
    st.plotly_chart(fig1, use_container_width=True)

with col_dist:
    st.markdown("""
    <div class="chart-container-card">
        <div class="chart-header-title">Score Frequency Distribution</div>
        <div class="chart-header-sub">Histogram of match performances across all recorded career fixtures</div>
    </div>
    """, unsafe_allow_html=True)

    fig2 = px.histogram(
        player_df,
        x=value_col,
        nbins=14,
        labels={value_col: f"{unit_label} Scored per Match", "count": "Match Frequency"}
    )
    fig2.update_traces(
        marker_color="#0284C7",
        marker_line_color="#FFFFFF",
        marker_line_width=1
    )
    layout2 = get_plotly_layout(
        title=f"{player} — Performance Distribution",
        height=350,
        xaxis_title=f"{unit_label} per Fixture",
        yaxis_title="Frequency (Matches)"
    )
    fig2.update_layout(**layout2)
    st.plotly_chart(fig2, use_container_width=True)

# -------------------------------------------------------------
# 4. VENUE & OPPOSITION IMPACT
# -------------------------------------------------------------
col_venue, col_opp = st.columns(2)

with col_venue:
    st.markdown("""
    <div class="chart-container-card">
        <div class="chart-header-title">Venue Performance Breakdown</div>
        <div class="chart-header-sub">Average output across top 8 stadium venues (minimum matches filtered)</div>
    </div>
    """, unsafe_allow_html=True)

    venue_avg = (
        player_df.groupby("venue")[value_col]
        .agg(["mean", "count"])
        .reset_index()
        .rename(columns={"mean": "Average", "count": "Matches"})
        .sort_values("Average", ascending=False)
        .head(8)
    )
    fig3 = px.bar(
        venue_avg,
        x="venue",
        y="Average",
        text_auto=".1f",
        hover_data=["Matches"],
        labels={"venue": "Venue", "Average": f"Avg {unit_label}"}
    )
    fig3.update_traces(marker_color="#006699")
    layout3 = get_plotly_layout(
        title=f"Highest Average Venues (Top 8)",
        height=350,
        xaxis_title="Stadium Venue",
        yaxis_title=f"Average {unit_label}"
    )
    fig3.update_layout(**layout3)
    fig3.update_layout(xaxis_tickangle=-30)
    st.plotly_chart(fig3, use_container_width=True)

with col_opp:
    st.markdown("""
    <div class="chart-container-card">
        <div class="chart-header-title">Opposition Head-to-Head Breakdown</div>
        <div class="chart-header-sub">Historical average output against major IPL franchise opponents</div>
    </div>
    """, unsafe_allow_html=True)

    opp_avg = (
        player_df.groupby(opponent_col)[value_col]
        .agg(["mean", "count"])
        .reset_index()
        .rename(columns={"mean": "Average", "count": "Matches"})
        .sort_values("Average", ascending=False)
        .head(8)
    )
    fig4 = px.bar(
        opp_avg,
        x=opponent_col,
        y="Average",
        text_auto=".1f",
        hover_data=["Matches"],
        labels={opponent_col: "Opponent", "Average": f"Avg {unit_label}"}
    )
    fig4.update_traces(marker_color="#0369A1")
    layout4 = get_plotly_layout(
        title=f"Performance vs Opponent Franchises",
        height=350,
        xaxis_title="Opponent Team",
        yaxis_title=f"Average {unit_label}"
    )
    fig4.update_layout(**layout4)
    fig4.update_layout(xaxis_tickangle=-30)
    st.plotly_chart(fig4, use_container_width=True)

# -------------------------------------------------------------
# 5. CONSISTENCY & MOMENTUM
# -------------------------------------------------------------
render_section_header(
    eyebrow="Form Diagnostics",
    title="Consistency & Momentum Analysis",
    subtitle="Evaluation of performance dispersion and short-term trajectory vs baseline."
)

std_dev = player_df[value_col].std()
momentum = last_5_avg - last_10_avg

c1, c2 = st.columns(2)
with c1:
    st.metric(
        label="Performance Volatility (Std Dev)",
        value=f"{std_dev:.2f}",
        help="Standard deviation of match scores. Lower value indicates higher consistency."
    )
with c2:
    st.metric(
        label="Short-Term Momentum Index",
        value=f"{momentum:+.2f}",
        help="Difference between Last 5 Matches Average and Last 10 Matches Average."
    )

if momentum > 0:
    st.success(f"**Positive Momentum**: {player}'s last 5 matches average ({last_5_avg:.2f}) is trending **+{momentum:.2f}** above their 10-match baseline ({last_10_avg:.2f}).")
else:
    st.info(f"**Neutral / Consolidating Momentum**: {player}'s last 5 matches average ({last_5_avg:.2f}) is tracking **{momentum:.2f}** relative to their 10-match baseline ({last_10_avg:.2f}).")

st.divider()

# -------------------------------------------------------------
# 6. MODEL INSIGHTS (SHAP EXPLAINABILITY)
# -------------------------------------------------------------
render_section_header(
    eyebrow="Explainable AI",
    title="Model Insights & Feature Importance (SHAP)",
    subtitle="SHapley Additive exPlanations quantify the relative contribution of each feature to the model's predictions."
)

colA, colB = st.columns(2)

if os.path.exists(summary_path):
    with colA:
        st.markdown("**SHAP Feature Impact Distribution**")
        st.image(
            Image.open(summary_path),
            caption=f"{role} Model — Feature Impact Distribution (Top 10 Named Drivers)",
            use_container_width=True
        )
else:
    colA.info("SHAP Summary plot not available in artifacts directory.")

if os.path.exists(importance_path):
    with colB:
        st.markdown("**Mean Feature Importance Ranking**")
        st.image(
            Image.open(importance_path),
            caption=f"{role} Model — Mean Absolute SHAP Importance Ranking",
            use_container_width=True
        )
else:
    colB.info("SHAP Feature Importance plot not available in artifacts directory.")

# Render sidebar footer
render_sidebar_footer()
