import os
import pandas as pd


class FeatureEngineering:

    def __init__(self):
        self.output_path = os.path.join("artifacts", "processed")
        os.makedirs(self.output_path, exist_ok=True)

    # ================= BATTER MATCH STATS =================
    def create_batter_match_stats(self, df):

        batter_df = (
            df.groupby(
                ["match_id", "batsman", "batting_team",
                 "bowling_team", "venue", "date"]
            )
            .agg(
                runs=("runs", "sum"),
                balls=("ball", "sum"),
                fours=("runs", lambda x: (x == 4).sum()),
                sixes=("runs", lambda x: (x == 6).sum())
            )
            .reset_index()
        )

        batter_df["strike_rate"] = (
            batter_df["runs"] / batter_df["balls"]
        ) * 100

        return batter_df

    # ================= BATTER TRAINING DATASET =================
    def build_batter_training_dataset(self, df):

        df = df.sort_values(["batsman", "date"])

        df["runs_next_match"] = df.groupby("batsman")["runs"].shift(-1)
        df["prev_runs"] = df.groupby("batsman")["runs"].shift(1)

        df["last_5_avg"] = (
            df.groupby("batsman")["runs"]
            .rolling(5).mean().shift(1)
            .reset_index(level=0, drop=True)
        )

        df["last_10_avg"] = (
            df.groupby("batsman")["runs"]
            .rolling(10).mean().shift(1)
            .reset_index(level=0, drop=True)
        )

        df["career_avg"] = (
            df.groupby("batsman")["runs"]
            .expanding().mean().shift(1)
            .reset_index(level=0, drop=True)
        )

        df = df.dropna()

        return df

    # ================= BOWLER MATCH STATS =================
    def create_bowler_match_stats(self, df):

        df["is_wicket"] = df["iswicket_delivery"]

        bowler_df = (
            df.groupby(
                ["match_id", "bowler", "bowling_team",
                 "batting_team", "venue", "date"]
            )
            .agg(
                wickets=("is_wicket", "sum"),
                balls=("ball", "sum"),
                runs_conceded=("runs", "sum")
            )
            .reset_index()
        )

        bowler_df["economy"] = (
            bowler_df["runs_conceded"] /
            bowler_df["balls"]
        ) * 6

        return bowler_df

    # ================= BOWLER TRAINING DATASET =================
    def build_bowler_training_dataset(self, df):

        df = df.sort_values(["bowler", "date"])

        df["wickets_next_match"] = df.groupby("bowler")["wickets"].shift(-1)
        df["prev_wickets"] = df.groupby("bowler")["wickets"].shift(1)

        df["last_5_wkts"] = (
            df.groupby("bowler")["wickets"]
            .rolling(5).mean().shift(1)
            .reset_index(level=0, drop=True)
        )

        df["last_10_wkts"] = (
            df.groupby("bowler")["wickets"]
            .rolling(10).mean().shift(1)
            .reset_index(level=0, drop=True)
        )

        df["career_wkt_avg"] = (
            df.groupby("bowler")["wickets"]
            .expanding().mean().shift(1)
            .reset_index(level=0, drop=True)
        )

        df = df.dropna()

        return df

    # ================= MASTER FEATURE PIPELINE =================
    def initiate_feature_engineering(self, merged_df):

        print("\nStarting Feature Engineering...")

        # Batter
        batter_stats = self.create_batter_match_stats(merged_df)
        batter_dataset = self.build_batter_training_dataset(batter_stats)

        # Bowler
        bowler_stats = self.create_bowler_match_stats(merged_df)
        bowler_dataset = self.build_bowler_training_dataset(bowler_stats)

        # Save both
        batter_dataset.to_csv(
            os.path.join(self.output_path, "batter_training_data.csv"),
            index=False
        )

        bowler_dataset.to_csv(
            os.path.join(self.output_path, "bowler_training_data.csv"),
            index=False
        )

        print("Feature engineering completed.")
        print("Saved batter_training_data.csv")
        print("Saved bowler_training_data.csv")

        return batter_dataset, bowler_dataset
