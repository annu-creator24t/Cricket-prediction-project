import os
import pandas as pd

from src.pipeline.data_ingestion import DataIngestion
from src.pipeline.data_preprocessing import DataPreprocessing
from src.pipeline.feature_engineering import FeatureEngineering
from src.pipeline.training_pipeline import ModelTrainer


def run_pipeline():

    print("\n==============================")
    print("CRICKET PERFORMANCE PIPELINE")
    print("==============================\n")

    # -------------------------------------------------
    # Step 1: Data Ingestion
    # -------------------------------------------------
    print("Step 1: Data Ingestion Started")

    ingestion = DataIngestion()
    deliveries_df, matches_df = ingestion.initiate_data_ingestion()

    print("Step 1: Completed\n")

    # -------------------------------------------------
    # Step 2: Data Preprocessing
    # -------------------------------------------------
    print("Step 2: Data Preprocessing Started")

    preprocessing = DataPreprocessing()
    merged_df = preprocessing.initiate_data_preprocessing(
        deliveries_df,
        matches_df
    )

    print("Step 2: Completed\n")

    # -------------------------------------------------
    # Step 3: Feature Engineering
    # -------------------------------------------------
    print("Step 3: Feature Engineering Started")

    feature_eng = FeatureEngineering()
    batter_df, bowler_df = feature_eng.initiate_feature_engineering(
        merged_df
    )

    print("Step 3: Completed\n")

    # -------------------------------------------------
    # Step 4: Model Training
    # -------------------------------------------------
    print("Step 4: Model Training Started")

    trainer = ModelTrainer()

    # Train Batter Model
    trainer.train(
        df=batter_df,
        target_column="runs_next_match",
        role_name="batter"
    )

    # Train Bowler Model
    trainer.train(
        df=bowler_df,
        target_column="wickets_next_match",
        role_name="bowler"
    )

    print("Step 4: Completed\n")

    print("Pipeline Execution Successful.")


if __name__ == "__main__":
    run_pipeline()
