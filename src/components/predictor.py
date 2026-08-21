import os
import joblib
import pandas as pd
from typing import Dict, Any, List, Optional


def get_project_root() -> str:
    """Finds the project root directory reliably."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # current_dir is <root>/src/components, parent is <root>/src, grandparent is <root>
    root = os.path.abspath(os.path.join(current_dir, "..", ".."))
    return root


class ModelPredictor:

    def __init__(self, role_name: str, base_dir: Optional[str] = None):
        self.role_name = role_name.lower()
        if self.role_name not in ["batter", "bowler"]:
            raise ValueError(f"Invalid role_name '{role_name}'. Must be 'batter' or 'bowler'.")

        self.base_dir = base_dir or get_project_root()
        model_path = os.path.join(self.base_dir, "artifacts", "models", f"{self.role_name}_best_model.pkl")

        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model file not found at: {model_path}. Please train the model first or verify artifacts path."
            )

        self.pipeline = joblib.load(model_path)

        # Retrieve expected feature names from the fitted preprocessor
        self.expected_features = (
            self.pipeline.named_steps["preprocessor"]
            .feature_names_in_
        )

    def predict(self, input_data: Dict[str, Any]) -> float:
        """
        Runs model prediction on a single input data dictionary.
        Returns predicted float (e.g. expected runs for batter, expected wickets for bowler).
        """
        input_df = pd.DataFrame([input_data])

        # Add any missing features with default 0 / empty string
        for col in self.expected_features:
            if col not in input_df.columns:
                input_df[col] = 0

        # Ensure correct feature ordering
        input_df = input_df[self.expected_features]

        prediction = self.pipeline.predict(input_df)
        pred_value = float(prediction[0])

        # Cricket predictions shouldn't be negative
        return max(0.0, pred_value)


def load_dataset_metadata(base_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    Loads distinct players, teams, and venues from processed training data.
    """
    root = base_dir or get_project_root()
    batter_path = os.path.join(root, "artifacts", "processed", "batter_training_data.csv")
    bowler_path = os.path.join(root, "artifacts", "processed", "bowler_training_data.csv")

    metadata = {
        "batters": [],
        "bowlers": [],
        "teams": [],
        "venues": []
    }

    if os.path.exists(batter_path):
        b_df = pd.read_csv(batter_path)
        metadata["batters"] = sorted([p for p in b_df["batsman"].dropna().unique().tolist()])
        teams = set(b_df["batting_team"].dropna().unique().tolist() + b_df["bowling_team"].dropna().unique().tolist())
        venues = set(b_df["venue"].dropna().unique().tolist())
        metadata["teams"] = sorted(list(teams))
        metadata["venues"] = sorted(list(venues))

    if os.path.exists(bowler_path):
        bw_df = pd.read_csv(bowler_path)
        metadata["bowlers"] = sorted([p for p in bw_df["bowler"].dropna().unique().tolist()])
        teams = set(metadata["teams"] + bw_df["bowling_team"].dropna().unique().tolist() + bw_df["batting_team"].dropna().unique().tolist())
        venues = set(metadata["venues"] + bw_df["venue"].dropna().unique().tolist())
        metadata["teams"] = sorted(list(teams))
        metadata["venues"] = sorted(list(venues))

    return metadata


def get_player_stats(player_name: str, role: str, base_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    Fetches the latest recorded historical match stats and rolling averages for a given player.
    """
    root = base_dir or get_project_root()
    role = role.lower()
    file_name = f"{role}_training_data.csv"
    data_path = os.path.join(root, "artifacts", "processed", file_name)

    if not os.path.exists(data_path):
        return {}

    df = pd.read_csv(data_path)
    player_col = "batsman" if role == "batter" else "bowler"
    player_df = df[df[player_col] == player_name].sort_values("date")

    if player_df.empty:
        return {}

    latest_row = player_df.iloc[-1]
    history_records = player_df.tail(15).to_dict(orient="records")

    if role == "batter":
        runs_series = player_df["runs"].astype(float)
        return {
            "player": player_name,
            "role": "batter",
            "last_team": latest_row.get("batting_team", ""),
            "last_opponent": latest_row.get("bowling_team", ""),
            "last_venue": latest_row.get("venue", ""),
            "prev_runs": float(latest_row.get("runs", 0.0)),
            "last_5_avg": float(runs_series.tail(5).mean()),
            "last_10_avg": float(runs_series.tail(10).mean()),
            "career_avg": float(runs_series.mean()),
            "total_matches": len(player_df),
            "recent_history": history_records
        }
    else:
        wkts_series = player_df["wickets"].astype(float)
        return {
            "player": player_name,
            "role": "bowler",
            "last_team": latest_row.get("bowling_team", ""),
            "last_opponent": latest_row.get("batting_team", ""),
            "last_venue": latest_row.get("venue", ""),
            "prev_wickets": float(latest_row.get("wickets", 0.0)),
            "last_5_wkts": float(wkts_series.tail(5).mean()),
            "last_10_wkts": float(wkts_series.tail(10).mean()),
            "career_wkt_avg": float(wkts_series.mean()),
            "total_matches": len(player_df),
            "recent_history": history_records
        }

