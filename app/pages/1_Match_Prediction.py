import os
import sys
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Add project root to sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.components.predictor import ModelPredictor, load_dataset_metadata, get_player_stats
from app.ui_theme import apply_custom_css, render_sidebar_header, render_sidebar_footer, get_plotly_layout

# Page Configuration
st.set_page_config(
    page_title="Match Prediction — Cricket Performance Analytics",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply unified design system
apply_custom_css()
render_sidebar_header()

# -------------------------------------------------------------
# HEADER
# -------------------------------------------------------------
st.markdown('<div class="page-title">Match Performance Prediction</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="page-subtitle">Forecast individual player performance using historical match data.</div>',
    unsafe_allow_html=True
)
st.divider()

# Load metadata
metadata = load_dataset_metadata(PROJECT_ROOT)
all_teams = metadata.get("teams", [])
all_venues = metadata.get("venues", [])

# -------------------------------------------------------------
# 1. PLAYER SELECTION
# -------------------------------------------------------------
st.markdown('<div class="section-title">Player Selection</div>', unsafe_allow_html=True)

col_role, col_player = st.columns([1, 2])

with col_role:
    role = st.selectbox("Player Role", ["Batter", "Bowler"], index=0)
    role_key = role.lower()

available_players = metadata.get("batters" if role_key == "batter" else "bowlers", [])

if not available_players:
    st.error("No player data found in processed dataset. Please ensure data files are present.")
    st.stop()

# Default selection
default_player_name = "V Kohli" if role_key == "batter" and "V Kohli" in available_players else (
    "JJ Bumrah" if role_key == "bowler" and "JJ Bumrah" in available_players else available_players[0]
)
default_index = available_players.index(default_player_name) if default_player_name in available_players else 0

with col_player:
    selected_player = st.selectbox(
        "Player",
        available_players,
        index=default_index,
        help="Select a player from the historical database."
    )

# Retrieve historical stats for the selected player
player_stats = get_player_stats(selected_player, role_key, PROJECT_ROOT)

if not player_stats:
    st.warning(f"No historical records found for {selected_player}.")
    st.stop()

# -------------------------------------------------------------
# 2. MATCH CONTEXT
# -------------------------------------------------------------
st.markdown('<div class="section-title">Match Context</div>', unsafe_allow_html=True)

col_t1, col_t2, col_v = st.columns(3)

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

if player_team == opponent_team:
    st.warning("Note: Selected player team and opponent team are the same.")

# -------------------------------------------------------------
# 3. HISTORICAL FORM METRICS
# -------------------------------------------------------------
st.markdown('<div class="section-title">Historical Form Parameters</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Auto-filled based on player match history (editable for scenario modeling):</div>',
    unsafe_allow_html=True
)

col_f1, col_f2, col_f3, col_f4 = st.columns(4)

if role_key == "batter":
    with col_f1:
        prev_runs = st.number_input("Previous Match Runs", min_value=0.0, max_value=300.0, value=float(player_stats.get("prev_runs", 0.0)), step=1.0)
    with col_f2:
        last_5_avg = st.number_input("Last 5 Matches Avg", min_value=0.0, max_value=200.0, value=float(player_stats.get("last_5_avg", 0.0)), step=0.1)
    with col_f3:
        last_10_avg = st.number_input("Last 10 Matches Avg", min_value=0.0, max_value=200.0, value=float(player_stats.get("last_10_avg", 0.0)), step=0.1)
    with col_f4:
        career_avg = st.number_input("Career Average", min_value=0.0, max_value=150.0, value=float(player_stats.get("career_avg", 0.0)), step=0.1)
else:
    with col_f1:
        prev_wkts = st.number_input("Previous Match Wkts", min_value=0.0, max_value=10.0, value=float(player_stats.get("prev_wickets", 0.0)), step=1.0)
    with col_f2:
        last_5_wkts = st.number_input("Last 5 Matches Wkt Avg", min_value=0.0, max_value=6.0, value=float(player_stats.get("last_5_wkts", 0.0)), step=0.1)
    with col_f3:
        last_10_wkts = st.number_input("Last 10 Matches Wkt Avg", min_value=0.0, max_value=6.0, value=float(player_stats.get("last_10_wkts", 0.0)), step=0.1)
    with col_f4:
        career_wkt_avg = st.number_input("Career Wkt Average", min_value=0.0, max_value=5.0, value=float(player_stats.get("career_wkt_avg", 0.0)), step=0.1)

st.write("")

# -------------------------------------------------------------
# 4. PREDICTION GENERATION
# -------------------------------------------------------------
predict_btn = st.button("Generate Prediction", type="primary")

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
            val_format = f"{predicted_val:.2f} Wickets"

        # Result Presentation
        st.markdown(f"""
        <div class="result-container">
            <div class="result-player-name">{selected_player}</div>
            <div class="result-metric-label">{metric_label} (Next Match)</div>
            <div class="result-metric-val">{val_format}</div>
            <div style="font-size: 0.875rem; color: #475569;">
                Matchup: <strong>{player_team}</strong> vs <strong>{opponent_team}</strong> &bull; Venue: <strong>{venue}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Comparative Benchmarks
        k1, k2, k3, k4 = st.columns(4)
        delta_val = predicted_val - primary_benchmark

        k1.metric(
            label=f"Predicted {metric_label}",
            value=val_format,
            delta=f"{delta_val:+.2f} vs Career Avg"
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
        # 5. HISTORICAL FORM VS PREDICTION CHART
        # -------------------------------------------------------------
        recent_history = player_stats.get("recent_history", [])
        if recent_history:
            st.markdown('<div class="section-title">Recent Form Trend & Forecast Projection</div>', unsafe_allow_html=True)
            hist_df = pd.DataFrame(recent_history).sort_values("date")
            y_col = "runs" if role_key == "batter" else "wickets"

            # Create clean sequence labels
            match_labels = [f"Match {i+1} ({row['date'][:10]})" for i, row in hist_df.reset_index().iterrows()]
            
            fig = go.Figure()

            # Past match performance
            fig.add_trace(go.Scatter(
                x=match_labels,
                y=hist_df[y_col],
                mode="lines+markers",
                name="Historical Match Output",
                line=dict(color="#006699", width=2.5),
                marker=dict(size=6, color="#004C73")
            ))

            # Predicted value point
            fig.add_trace(go.Scatter(
                x=["Next Match (Forecast)"],
                y=[predicted_val],
                mode="markers",
                name="Model Forecast",
                marker=dict(size=12, color="#0284C7", symbol="diamond")
            ))

            layout_config = get_plotly_layout(
                title=f"{selected_player} — Historical Performance vs Model Projection",
                height=380,
                xaxis_title="Recent Match Timeline",
                yaxis_title=metric_label
            )
            fig.update_layout(**layout_config)
            fig.update_layout(
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )

            st.plotly_chart(fig, use_container_width=True)

        # -------------------------------------------------------------
        # 6. INPUT AUDIT SUMMARY
        # -------------------------------------------------------------
        with st.expander("Model Input Features (Verification Summary)"):
            audit_df = pd.DataFrame(list(input_features.items()), columns=["Feature Parameter", "Input Value"])
            st.dataframe(audit_df, use_container_width=True)

    except Exception as e:
        st.error(f"Error executing prediction: {str(e)}")

# Render sidebar footer
render_sidebar_footer()