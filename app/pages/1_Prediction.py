import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Standardize path to project root
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.components.predictor import ModelPredictor, load_dataset_metadata, get_player_stats

st.set_page_config(page_title="Performance Prediction", page_icon="🎯", layout="wide")

st.title("🎯 Player Match Performance Prediction")
st.markdown("Forecast expected individual player match performance using trained regression models.")
st.divider()

# Load metadata
metadata = load_dataset_metadata(PROJECT_ROOT)
all_teams = metadata.get("teams", [])
all_venues = metadata.get("venues", [])

# -------------------------------------------------------------
# 1. ROLE & PLAYER SELECTION
# -------------------------------------------------------------
col_role, col_player = st.columns([1, 2])

with col_role:
    role = st.selectbox("Select Player Role", ["Batter", "Bowler"], index=0)
    role_key = role.lower()

available_players = metadata.get("batters" if role_key == "batter" else "bowlers", [])

if not available_players:
    st.error("No player data found. Please ensure training data exists in `artifacts/processed/`.")
    st.stop()

# Default suggestions for quick selection
default_player_name = "V Kohli" if role_key == "batter" and "V Kohli" in available_players else (
    "JJ Bumrah" if role_key == "bowler" and "JJ Bumrah" in available_players else available_players[0]
)
default_index = available_players.index(default_player_name) if default_player_name in available_players else 0

with col_player:
    selected_player = st.selectbox(
        f"Select {role}",
        available_players,
        index=default_index,
        help="Type or select a player name from the historical dataset."
    )

# Retrieve historical stats for the selected player
player_stats = get_player_stats(selected_player, role_key, PROJECT_ROOT)

if not player_stats:
    st.warning(f"No historical records found for {selected_player}.")
    st.stop()

# -------------------------------------------------------------
# 2. MATCH CONTEXT & SCENARIO TUNING
# -------------------------------------------------------------
st.subheader("Match Context & Parameters")

with st.expander("⚙️ Match Conditions & Player Form (Auto-filled from player history)", expanded=True):
    col_t1, col_t2, col_v = st.columns(3)

    # Determine default teams and venue
    last_team = player_stats.get("last_team", "")
    last_opp = player_stats.get("last_opponent", "")
    last_ven = player_stats.get("last_venue", "")

    team_idx = all_teams.index(last_team) if last_team in all_teams else 0
    opp_idx = all_teams.index(last_opp) if last_opp in all_teams else (1 if len(all_teams) > 1 else 0)
    ven_idx = all_venues.index(last_ven) if last_ven in all_venues else 0

    with col_t1:
        player_team = st.selectbox(
            f"{'Batting' if role_key == 'batter' else 'Bowling'} Team",
            all_teams,
            index=team_idx
        )

    with col_t2:
        opponent_team = st.selectbox(
            f"Opponent ({'Bowling' if role_key == 'batter' else 'Batting'} Team)",
            all_teams,
            index=opp_idx
        )

    with col_v:
        venue = st.selectbox("Match Venue", all_venues, index=ven_idx)

    st.markdown("##### Historical Form Metrics")
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)

    if role_key == "batter":
        with col_f1:
            prev_runs = st.number_input("Runs in Previous Match", value=float(player_stats.get("prev_runs", 0.0)), step=1.0)
        with col_f2:
            last_5_avg = st.number_input("Last 5 Matches Average", value=float(player_stats.get("last_5_avg", 0.0)), step=0.1)
        with col_f3:
            last_10_avg = st.number_input("Last 10 Matches Average", value=float(player_stats.get("last_10_avg", 0.0)), step=0.1)
        with col_f4:
            career_avg = st.number_input("Career Average", value=float(player_stats.get("career_avg", 0.0)), step=0.1)
    else:
        with col_f1:
            prev_wkts = st.number_input("Wickets in Previous Match", value=float(player_stats.get("prev_wickets", 0.0)), step=1.0)
        with col_f2:
            last_5_wkts = st.number_input("Last 5 Matches Wkt Avg", value=float(player_stats.get("last_5_wkts", 0.0)), step=0.1)
        with col_f3:
            last_10_wkts = st.number_input("Last 10 Matches Wkt Avg", value=float(player_stats.get("last_10_wkts", 0.0)), step=0.1)
        with col_f4:
            career_wkt_avg = st.number_input("Career Wicket Average", value=float(player_stats.get("career_wkt_avg", 0.0)), step=0.1)

# Validation check
if player_team == opponent_team:
    st.warning("⚠️ Warning: Selected player team and opponent team are the same.")

# -------------------------------------------------------------
# 3. PREDICTION ACTION & INFERENCE
# -------------------------------------------------------------
st.write("")
predict_btn = st.button("🏏 Generate Match Prediction", type="primary", use_container_width=False)

if predict_btn:
    try:
        predictor = ModelPredictor(role_key, PROJECT_ROOT)

        if role_key == "batter":
            input_features = {
                "batsman": selected_player,
                "batting_team": player_team,
                "bowling_team": opponent_team,
                "venue": venue,
                "prev_runs": prev_runs,
                "last_5_avg": last_5_avg,
                "last_10_avg": last_10_avg,
                "career_avg": career_avg
            }
            predicted_val = predictor.predict(input_features)
            primary_benchmark = career_avg
            metric_label = "Expected Runs"
            val_format = f"{predicted_val:.1f} Runs"
        else:
            input_features = {
                "bowler": selected_player,
                "bowling_team": player_team,
                "batting_team": opponent_team,
                "venue": venue,
                "prev_wickets": prev_wkts,
                "last_5_wkts": last_5_wkts,
                "last_10_wkts": last_10_wkts,
                "career_wkt_avg": career_wkt_avg
            }
            predicted_val = predictor.predict(input_features)
            primary_benchmark = career_wkt_avg
            metric_label = "Expected Wickets"
            val_format = f"{predicted_val:.2f} Wkts"

        st.markdown("---")
        st.subheader("Prediction Results")

        # KPI Metrics Cards
        k1, k2, k3, k4 = st.columns(4)
        delta_val = predicted_val - primary_benchmark

        k1.metric(
            label=f"🎯 {metric_label}",
            value=val_format,
            delta=f"{delta_val:+.2f} vs Career Avg",
            delta_color="normal"
        )

        k2.metric(
            label="Last 5 Matches Avg",
            value=f"{last_5_avg:.1f} Runs" if role_key == "batter" else f"{last_5_wkts:.2f} Wkts"
        )

        k3.metric(
            label="Last 10 Matches Avg",
            value=f"{last_10_avg:.1f} Runs" if role_key == "batter" else f"{last_10_wkts:.2f} Wkts"
        )

        k4.metric(
            label="Career Benchmark",
            value=f"{career_avg:.1f} Runs" if role_key == "batter" else f"{career_wkt_avg:.2f} Wkts"
        )

        st.write("")

        # -------------------------------------------------------------
        # 4. HISTORICAL FORM VS PREDICTION CHART
        # -------------------------------------------------------------
        recent_history = player_stats.get("recent_history", [])
        if recent_history:
            st.subheader(f"Recent Form & Forecast Projection ({selected_player})")
            hist_df = pd.DataFrame(recent_history)
            y_col = "runs" if role_key == "batter" else "wickets"

            fig = go.Figure()

            # Historical match performance line
            fig.add_trace(go.Scatter(
                x=hist_df["date"],
                y=hist_df[y_col],
                mode="lines+markers",
                name="Actual Matches",
                line=dict(color="#2563EB", width=2.5),
                marker=dict(size=7, color="#1D4ED8")
            ))

            # Predicted value marker
            next_label = "Upcoming Match"
            fig.add_trace(go.Scatter(
                x=[next_label],
                y=[predicted_val],
                mode="markers",
                name="Model Forecast",
                marker=dict(size=14, color="#DC2626", symbol="star")
            ))

            fig.update_layout(
                title=f"Actual Historical {metric_label} vs Next Match Prediction",
                xaxis_title="Match Date / Upcoming",
                yaxis_title=metric_label,
                template="plotly_white",
                height=420,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )

            st.plotly_chart(fig, use_container_width=True)

        # -------------------------------------------------------------
        # 5. INPUT PARAMETERS AUDIT TABLE
        # -------------------------------------------------------------
        with st.expander("📋 View Model Input Features"):
            audit_df = pd.DataFrame(list(input_features.items()), columns=["Feature Name", "Value"])
            st.dataframe(audit_df, use_container_width=True)

    except Exception as e:
        st.error(f"Error generating prediction: {str(e)}")