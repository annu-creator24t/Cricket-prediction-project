import os
import joblib
import numpy as np
import pandas as pd
import shap
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor


class ModelTrainer:

    def train(self, df: pd.DataFrame, target_column: str, role_name: str):

        print("\n==============================")
        print(f"Training started for: {role_name}")
        print("==============================")

        df = df.sort_values("date")

        split_index = int(len(df) * 0.8)
        train_df = df.iloc[:split_index]
        test_df = df.iloc[split_index:]

        if role_name == "batter":
            drop_cols = [
                "match_id", "runs", "balls", "fours",
                "sixes", "strike_rate", "date",
                "runs_next_match"
            ]
        else:
            drop_cols = [
                "match_id", "wickets", "balls",
                "runs_conceded", "economy",
                "date", "wickets_next_match"
            ]

        X_train = train_df.drop(columns=drop_cols)
        y_train = train_df[target_column]

        X_test = test_df.drop(columns=drop_cols)
        y_test = test_df[target_column]

        categorical_cols = X_train.select_dtypes(include=["object"]).columns.tolist()
        numeric_cols = X_train.select_dtypes(exclude=["object"]).columns.tolist()

        preprocessor = ColumnTransformer(
            transformers=[
                ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
                ("num", "passthrough", numeric_cols),
            ]
        )

        models = {
            "RandomForest": RandomForestRegressor(n_estimators=300, random_state=42),
            "ExtraTrees": ExtraTreesRegressor(n_estimators=300, random_state=42),
            "XGBoost": XGBRegressor(n_estimators=300, learning_rate=0.05, random_state=42),
            "LightGBM": LGBMRegressor(n_estimators=300, random_state=42),
            "CatBoost": CatBoostRegressor(
                iterations=300,
                learning_rate=0.05,
                depth=6,
                verbose=0,
                random_state=42
            )
        }

        results = []
        trained_pipelines = {}

        for name, model in models.items():

            print(f"\nTraining {name}...")

            pipeline = Pipeline([
                ("preprocessor", preprocessor),
                ("model", model)
            ])

            pipeline.fit(X_train, y_train)
            preds = pipeline.predict(X_test)

            rmse = np.sqrt(mean_squared_error(y_test, preds))
            mae = mean_absolute_error(y_test, preds)
            r2 = r2_score(y_test, preds)

            results.append({
                "Model": name,
                "RMSE": rmse,
                "MAE": mae,
                "R2": r2
            })

            trained_pipelines[name] = pipeline

            print(f"{name} RMSE: {rmse:.4f}")

        metrics_df = pd.DataFrame(results)

        os.makedirs("artifacts/models", exist_ok=True)
        metrics_df.to_csv(
            f"artifacts/models/{role_name}_metrics.csv",
            index=False
        )

        best_model_name = metrics_df.sort_values("RMSE").iloc[0]["Model"]
        best_pipeline = trained_pipelines[best_model_name]

        print(f"\nBest Model for {role_name}: {best_model_name}")

        # SHAP
        print("Generating SHAP plots...")

        X_test_transformed = best_pipeline.named_steps["preprocessor"].transform(X_test)

        explainer = shap.TreeExplainer(best_pipeline.named_steps["model"])
        shap_values = explainer.shap_values(X_test_transformed)

        os.makedirs("artifacts/shap", exist_ok=True)

        plt.figure()
        shap.summary_plot(shap_values, X_test_transformed, show=False)
        plt.tight_layout()
        plt.savefig(f"artifacts/shap/{role_name}_shap_summary.png")
        plt.close()

        plt.figure()
        shap.summary_plot(shap_values, X_test_transformed, plot_type="bar", show=False)
        plt.tight_layout()
        plt.savefig(f"artifacts/shap/{role_name}_shap_importance.png")
        plt.close()

        # Save Model
        joblib.dump(
            best_pipeline,
            f"artifacts/models/{role_name}_best_model.pkl"
        )

        print("Training Completed.\n")

        return best_pipeline
