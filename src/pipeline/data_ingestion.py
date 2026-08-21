import os
import pandas as pd


class DataIngestion:

    def __init__(self):
        self.raw_path = os.path.join("data", "raw")
        self.artifacts_path = os.path.join("artifacts", "dataset")

        os.makedirs(self.artifacts_path, exist_ok=True)

    def initiate_data_ingestion(self):

        print("\nStarting Data Ingestion...")

        deliveries_path = os.path.join(self.raw_path, "deliveries.csv")
        matches_path = os.path.join(self.raw_path, "matches.csv")

        deliveries_df = pd.read_csv(deliveries_path)
        matches_df = pd.read_csv(matches_path)

        print("Data Loaded Successfully")
        print("Deliveries shape:", deliveries_df.shape)
        print("Matches shape:", matches_df.shape)

        # Save raw copies inside artifacts
        deliveries_df.to_csv(
            os.path.join(self.artifacts_path, "deliveries.csv"),
            index=False
        )

        matches_df.to_csv(
            os.path.join(self.artifacts_path, "matches.csv"),
            index=False
        )

        print("Raw data saved inside artifacts/dataset")

        return deliveries_df, matches_df
