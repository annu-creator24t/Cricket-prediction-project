import os
import pandas as pd


class DataPreprocessing:

    def __init__(self):
        self.artifacts_path = os.path.join("artifacts", "processed")
        os.makedirs(self.artifacts_path, exist_ok=True)

    # --------------------------------------------------
    # Clean Matches
    # --------------------------------------------------
    def clean_matches(self, matches_df: pd.DataFrame):

        matches_df = matches_df.rename(columns={
            "id": "match_id",
            "match_date": "date",
            "winning_team": "winner"
        })

        matches_df["date"] = pd.to_datetime(
            matches_df["date"],
            errors="coerce"
        )

        keep_cols = [
            "match_id",
            "season",
            "city",
            "date",
            "venue",
            "team1",
            "team2",
            "toss_winner",
            "toss_decision",
            "winner"
        ]

        matches_df = matches_df[keep_cols]

        return matches_df

    # --------------------------------------------------
    # Clean Deliveries
    # --------------------------------------------------
    def clean_deliveries(self, deliveries_df: pd.DataFrame):

        deliveries_df = deliveries_df.rename(columns={
            "id": "match_id",
            "innings": "inning",
            "overs": "over",
            "batter": "batsman",
            "batsman_run": "runs"
        })

        deliveries_df["ball"] = 1

        return deliveries_df

    # --------------------------------------------------
    # Merge
    # --------------------------------------------------
    def merge_data(self, deliveries_df, matches_df):

        merged_df = pd.merge(
            deliveries_df,
            matches_df,
            on="match_id",
            how="left"
        )

        merged_df["bowling_team"] = merged_df.apply(
            lambda x: x["team2"]
            if x["batting_team"] == x["team1"]
            else x["team1"],
            axis=1
        )

        return merged_df

    # --------------------------------------------------
    # Master Preprocessing Method
    # --------------------------------------------------
    def initiate_data_preprocessing(self, deliveries_df, matches_df):

        print("\nStarting Data Preprocessing...")

        matches_df = self.clean_matches(matches_df)
        deliveries_df = self.clean_deliveries(deliveries_df)

        merged_df = self.merge_data(deliveries_df, matches_df)

        print("Merged dataset shape:", merged_df.shape)

        # Save processed dataset
        output_path = os.path.join(
            self.artifacts_path,
            "cleaned_data.csv"
        )

        merged_df.to_csv(output_path, index=False)

        print("Processed data saved at:", output_path)

        return merged_df
