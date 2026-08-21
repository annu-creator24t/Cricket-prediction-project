import os
import sys
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Path configuration for both local execution and Streamlit Community Cloud
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
APP_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

for p in [PROJECT_ROOT, APP_DIR, CURRENT_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from src.components.predictor import ModelPredictor, load_dataset_metadata, get_player_stats
except ImportError:
    from components.predictor import ModelPredictor, load_dataset_metadata, get_player_stats

try:
    from app.ui_theme import apply_custom_css, render_sidebar_header, render_sidebar_footer, get_plotly_layout
except ImportError:
    from ui_theme import apply_custom_css, render_sidebar_header, render_sidebar_footer, get_plotly_layout

# Page Configuration
st.set_page_config(
    page_title="Match Prediction — Cricket Performance Analytics",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply styling & sidebar
apply_custom_css()
render_sidebar_header()

# Header
st.markdown("""
<div class="overview-header">
    <div class="page-title">Match Performance Prediction</div>
    <div class="page-subtitle">
        Select a player and match context to estimate individual performance against historical baselines.
    </div>
</div>
""", unsafe_allow_html=True)

# Load metadata
metadata = load_dataset_metadata(PROJECT_ROOT)
all_teams = metadata.get("teams", [])
all_venues = metadata.get("venues", [])

# -------------------------------------------------------------
# 1. PLAYER SELECTION
# -------------------------------------------------------------
st.markdown('<div class="section-title">Player Selection</div>', unsafe_allow_html=True)

col_role, col_player = st.columns([1, 2.5])

with col_role:
    role = st.selectbox("Player Role", ["Batter", "Bowler"], index=0)
    role_key = role.lower()

available_players = metadata.get("batters" if role_key == "batter" else "bowlers", [])

if not available_players:
    st.error("No player records found in the processed database.")
    st.stop()

# Default selection
default_player_name = "V Kohli" if role_key == "batter" and "V Kohli" in available_players else (
    "JJ Bumrah" if role_key == "bowler" and "JJ Bumrah" in available_players else available_players[0]
)
default_index = available_players.index(default_player_name) if default_player_name in available_players else 0

with col_player:
    selected_player = st.selectbox(
        "Select Player",
        available_players,
        index=default_index
    )

# Retrieve historical stats for the selected player
player_stats = get_player_stats(selected_player, role_key, PROJECT_ROOT)

if not player_stats:
    st.warning(f"No historical match records found for {selected_player}.")
    st.stop()

st.write("")

# -------------------------------------------------------------
# 2. MATCH CONTEXT
# -------------------------------------------------------------
st.markdown('<div class="section-title">Match Context</div>', unsafe_allow_html=True)

col_t1, col_t2, col_v = st.columns([1.2, 1.2, 1.6])

last_team = player_stats.get("last_team", "")
last_opp = player_stats.get("last_opponent", "")
last_ven = player_stats.get("last_venue", "")

team_idx = all_teams.index(last_team) if last_team in all_teams else 0
opp_idx = all_teams.index(last_opp) if last_opp in all_teams else (1 if len(all_teams) > 1 else 0)
ven_idx = all_venues.index(last_ven) if last_ven in all_venues else 0

with col_t1:
    player_team = st.selectbox(
        "Batting Team" if role_key == "batter" else "Bowling Team",
        all_teams,
        index=team_idx
    )

with col_t2:
    opponent_team = st.selectbox(
        "Opponent",
        all_teams,
        index=opp_idx
    )

with col_v:
    venue = st.selectbox("Venue", all_venues, index=ven_idx)

if player_team == opponent_team:
    st.caption("Note: Selected team and opponent are identical.")

st.write("")

# -------------------------------------------------------------
# 3. RECENT PERFORMANCE PARAMETERS
# -------------------------------------------------------------
st.markdown('<div class="section-title">Recent Performance</div>', unsafe_allow_html=True)
st.caption("Auto-populated from player history. Adjust values to simulate custom scenarios:")

col_f1, col_f2, col_f3, col_f4 = st.columns(4)

if role_key == "batter":
    with col_f1:
        prev_runs = st.number_input("Previous Match Runs", min_value=0.0, max_value=300.0, value=float(player_stats.get("prev_runs", 0.0)), step=1.0)
    with col_f2:
        last_5_avg = st.number_input("Last 5 Matches Average", min_value=0.0, max_value=200.0, value=float(player_stats.get("last_5_avg", 0.0)), step=0.1)
    with col_f3:
        last_10_avg = st.number_input("Last 10 Matches Average", min_value=0.0, max_value=200.0, value=float(player_stats.get("last_10_avg", 0.0)), step=0.1)
    with col_f4:
        career_avg = st.number_input("Career Average", min_value=0.0, max_value=150.0, value=float(player_stats.get("career_avg", 0.0)), step=0.1)
else:
    with col_f1:
        prev_wkts = st.number_input("Previous Match Wickets", min_value=0.0, max_value=10.0, value=float(player_stats.get("prev_wickets", 0.0)), step=1.0)
    with col_f2:
        last_5_wkts = st.number_input("Last 5 Matches Wkt Avg", min_value=0.0, max_value=6.0, value=float(player_stats.get("last_5_wkts", 0.0)), step=0.1)
    with col_f3:
        last_10_wkts = st.number_input("Last 10 Matches Wkt Avg", min_value=0.0, max_value=6.0, value=float(player_stats.get("last_10_wkts", 0.0)), step=0.1)
    with col_f4:
        career_wkt_avg = st.number_input("Career Wkt Average", min_value=0.0, max_value=5.0, value=float(player_stats.get("career_wkt_avg", 0.0)), step=0.1)

st.write("")

# -------------------------------------------------------------
# 4. PREDICTION TRIGGER
# -------------------------------------------------------------
predict_btn = st.button("Generate Prediction", type="primary")

if predict_btn:
    try:
        with st.spinner("Calculating prediction..."):
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
                model_info = "CatBoost Regressor &bull; IPL Batting dataset (Test MAE: 16.92)"
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
                model_info = "CatBoost Regressor &bull; IPL Bowling dataset (Test MAE: 0.84)"

        delta_val = predicted_val - primary_benchmark

        # -------------------------------------------------------------
        # RESULT PANEL
        # -------------------------------------------------------------
        st.markdown(f"""
        <div class="result-panel">
            <div class="result-player-title">{selected_player} ({role})</div>
            <div class="result-matchup-meta">
                {player_team} vs {opponent_team} &bull; {venue}
            </div>
            <div style="font-size: 0.8rem; font-weight: 600; color: #64748B; text-transform: uppercase; letter-spacing: 0.04em;">
                {metric_label}
            </div>
            <div class="result-score-val">{val_format}</div>
            <div style="font-size: 0.78rem; color: #64748B; margin-top: 0.4rem;">
                Model: {model_info}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Comparative Metrics
        k1, k2, k3, k4 = st.columns(4)

        k1.metric(
            label=f"Predicted {metric_label}",
            value=val_format,
            delta=f"{delta_val:+.2f} vs Career"
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
            label="Career Average",
            value=f"{career_avg:.1f} Runs" if role_key == "batter" else f"{career_wkt_avg:.2f} Wkts"
        )

        st.write("")

        # -------------------------------------------------------------
        # 5. HISTORICAL TIMELINE VS PREDICTION
        # -------------------------------------------------------------
        recent_history = player_stats.get("recent_history", [])
        if recent_history:
            st.markdown('<div class="section-title">Recent Match History vs Prediction</div>', unsafe_allow_html=True)

            hist_df = pd.DataFrame(recent_history).sort_values("date")
            y_col = "runs" if role_key == "batter" else "wickets"

            match_labels = [f"M{i+1} ({str(row['date'])[:10]})" for i, row in hist_df.reset_index().iterrows()]
            
            fig = go.Figure()

            # Past match line
            fig.add_trace(go.Scatter(
                x=match_labels,
                y=hist_df[y_col],
                mode="lines+markers",
                name="Actual Match Score",
                line=dict(color="#006699", width=2),
                marker=dict(size=6, color="#004C73")
            ))

            # Forecast point
            fig.add_trace(go.Scatter(
                x=["Next Match (Prediction)"],
                y=[predicted_val],
                mode="markers",
                name="Model Prediction",
                marker=dict(size=12, color="#0284C7", symbol="diamond")
            ))

            layout_config = get_plotly_layout(
                title=f"{selected_player} — Historical Output Timeline",
                height=350,
                xaxis_title="Recent Matches (Oldest → Latest)",
                yaxis_title=metric_label
            )
            fig.update_layout(**layout_config)
            fig.update_layout(
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )

            st.plotly_chart(fig, use_container_width=True)

        # -------------------------------------------------------------
        # 6. FEATURE AUDIT TABLE
        # -------------------------------------------------------------
        with st.expander("Model Input Features (Audit)"):
            audit_df = pd.DataFrame(list(input_features.items()), columns=["Feature", "Value"])
            audit_df["Value"] = audit_df["Value"].astype(str)
            st.dataframe(audit_df, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Error generating prediction: {str(e)}")

else:
    # Empty Placeholder State
    st.markdown("""
    <div class="result-empty-placeholder">
        Prediction results and recent form comparisons will appear here after you click <strong>Generate Prediction</strong>.
    </div>
    """, unsafe_allow_html=True)

# Render sidebar footer
render_sidebar_footer()