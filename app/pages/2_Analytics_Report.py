import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

# Standardize path to project root
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

st.set_page_config(page_title="Player Analytics Report", page_icon="📊", layout="wide")

st.title("📊 Player Performance Intelligence & Analytics")
st.markdown("Detailed historical breakdown, opponent & venue insights, and machine learning model explainability.")
st.divider()

# Role selection
col_role, col_player = st.columns([1, 2])

with col_role:
    role = st.selectbox("Select Role", ["Batter", "Bowler"], index=0)
    role_key = role.lower()

# Load processed data
data_path = os.path.join(PROJECT_ROOT, "artifacts", "processed", f"{role_key}_training_data.csv")
summary_path = os.path.join(PROJECT_ROOT, "artifacts", "shap", f"{role_key}_shap_summary.png")
importance_path = os.path.join(PROJECT_ROOT, "artifacts", "shap", f"{role_key}_shap_importance.png")

if not os.path.exists(data_path):
    st.error(f"Dataset not found at `{data_path}`. Please run data preprocessing first.")
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

player_df = df[df[player_col] == player].sort_values("date")

if len(player_df) < 3:
    st.warning("Insufficient match history for deep statistical analysis (less than 3 matches recorded).")
    st.stop()

# -------------------------------------------------------------
# 1. PERFORMANCE SNAPSHOT
# -------------------------------------------------------------
st.subheader(f"Performance Snapshot — {player}")

last_5 = player_df.tail(5)
last_10 = player_df.tail(10)

k1, k2, k3, k4 = st.columns(4)

k1.metric("Last Match Score", f"{last_5[value_col].iloc[-1]:.0f} {unit_label}")
k2.metric("Last 5 Matches Avg", f"{last_5[value_col].mean():.2f} {unit_label}")
k3.metric("Last 10 Matches Avg", f"{last_10[value_col].mean():.2f} {unit_label}")
k4.metric("Career Average", f"{player_df[value_col].mean():.2f} {unit_label}")

st.divider()

# -------------------------------------------------------------
# 2. TREND & DISTRIBUTION
# -------------------------------------------------------------
col_trend, col_dist = st.columns(2)

with col_trend:
    st.subheader(f"Recent Match Trend (Last 15 Fixtures)")
    trend_df = player_df.tail(15)
    fig1 = px.line(
        trend_df,
        x="date",
        y=value_col,
        markers=True,
        labels={"date": "Match Date", value_col: unit_label},
        title=f"{player} — Match by Match {unit_label}"
    )
    fig1.update_traces(line_color="#2563EB", marker=dict(size=7))
    fig1.update_layout(template="plotly_white", height=380)
    st.plotly_chart(fig1, use_container_width=True)

with col_dist:
    st.subheader(f"Performance Distribution")
    fig2 = px.histogram(
        player_df,
        x=value_col,
        nbins=15,
        labels={value_col: unit_label},
        title=f"Frequency Distribution of {unit_label}"
    )
    fig2.update_traces(marker_color="#0D9488")
    fig2.update_layout(template="plotly_white", height=380)
    st.plotly_chart(fig2, use_container_width=True)

# -------------------------------------------------------------
# 3. VENUE & OPPOSITION IMPACT
# -------------------------------------------------------------
col_venue, col_opp = st.columns(2)

with col_venue:
    st.subheader("Top Venues by Average Performance")
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
        labels={"venue": "Venue", "Average": f"Avg {unit_label}"},
        title=f"Best Performing Venues (Top 8)"
    )
    fig3.update_traces(marker_color="#4F46E5")
    fig3.update_layout(template="plotly_white", height=380, xaxis_tickangle=-30)
    st.plotly_chart(fig3, use_container_width=True)

with col_opp:
    st.subheader("Opposition Breakdown")
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
        labels={opponent_col: "Opponent", "Average": f"Avg {unit_label}"},
        title=f"Performance vs Franchise Opponents"
    )
    fig4.update_traces(marker_color="#EA580C")
    fig4.update_layout(template="plotly_white", height=380, xaxis_tickangle=-30)
    st.plotly_chart(fig4, use_container_width=True)

# -------------------------------------------------------------
# 4. CONSISTENCY & MOMENTUM
# -------------------------------------------------------------
st.subheader("Consistency & Momentum Analysis")

std_dev = player_df[value_col].std()
momentum = last_5[value_col].mean() - last_10[value_col].mean()

c1, c2 = st.columns(2)
c1.metric("Performance Volatility (Std Dev)", f"{std_dev:.2f}", help="Standard deviation of match scores. Lower value indicates higher consistency.")
c2.metric("Short-Term Momentum Score", f"{momentum:+.2f}", help="Difference between last 5 match average and last 10 match average.")

if momentum > 0:
    st.success(f"📈 **Positive Momentum**: {player}'s recent 5 matches show higher output (+{momentum:.2f}) compared to their 10-match baseline.")
else:
    st.info(f"📉 **Consolidating / Normal Momentum**: {player}'s recent 5 matches are tracking slightly below or at their 10-match baseline ({momentum:.2f}).")

st.divider()

# -------------------------------------------------------------
# 5. SHAP EXPLAINABILITY
# -------------------------------------------------------------
st.subheader("🔍 Model Explainability (SHAP Analysis)")
st.markdown("""
SHAP (SHapley Additive exPlanations) values provide transparent attribution showing how different features 
(e.g., historical rolling averages, opposing team, match venue) influence the regression model's predictions.
""")

colA, colB = st.columns(2)

if os.path.exists(summary_path):
    colA.markdown("**SHAP Summary Distribution**")
    colA.image(
        Image.open(summary_path),
        caption=f"{role} Model — Feature Impact Distribution",
        use_container_width=True
    )
else:
    colA.info("SHAP Summary plot not found in `artifacts/shap/`.")

if os.path.exists(importance_path):
    colB.markdown("**Mean Feature Importance (SHAP Bar Plot)**")
    colB.image(
        Image.open(importance_path),
        caption=f"{role} Model — Global Feature Importance Ranking",
        use_container_width=True
    )
else:
    colB.info("SHAP Feature Importance plot not found in `artifacts/shap/`.")
