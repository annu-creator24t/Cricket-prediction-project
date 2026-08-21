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

        # ---------------- TIME-AWARE SPLIT ----------------
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

        # ---------------- PREPROCESSOR ----------------
        categorical_cols = X_train.select_dtypes(include=["object"]).columns.tolist()
        numeric_cols = X_train.select_dtypes(exclude=["object"]).columns.tolist()

        preprocessor = ColumnTransformer(
            transformers=[
                ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
                ("num", "passthrough", numeric_cols),
            ]
        )

        # ---------------- BASELINE ----------------
        if "last_10_avg" in X_test.columns:
            baseline_pred = X_test["last_10_avg"]
        elif "last_10_wkts" in X_test.columns:
            baseline_pred = X_test["last_10_wkts"]
        else:
            baseline_pred = np.full(len(y_test), y_train.mean())

        baseline_rmse = np.sqrt(mean_squared_error(y_test, baseline_pred))
        baseline_mae = mean_absolute_error(y_test, baseline_pred)
        baseline_r2 = r2_score(y_test, baseline_pred)

        print("\nBaseline Results:")
        print("RMSE:", baseline_rmse)
        print("MAE:", baseline_mae)
        print("R2:", baseline_r2)

        # ---------------- MODELS ----------------
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

            pipeline = Pipeline(
                steps=[
                    ("preprocessor", preprocessor),
                    ("model", model),
                ]
            )

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

            print(f"{name} Results:")
            print("RMSE:", rmse)
            print("MAE:", mae)
            print("R2:", r2)

        # ---------------- SAVE METRICS ----------------
        metrics_df = pd.DataFrame(results)

        baseline_row = pd.DataFrame([{
            "Model": "Baseline",
            "RMSE": baseline_rmse,
            "MAE": baseline_mae,
            "R2": baseline_r2
        }])

        metrics_df = pd.concat([metrics_df, baseline_row], ignore_index=True)

        os.makedirs("artifacts/models", exist_ok=True)
        metrics_path = f"artifacts/models/{role_name}_metrics.csv"
        metrics_df.to_csv(metrics_path, index=False)

        print(f"\nMetrics saved at: {metrics_path}")

        # ---------------- SELECT BEST MODEL ----------------
        best_model_name = metrics_df[
            metrics_df["Model"] != "Baseline"
        ].sort_values("RMSE").iloc[0]["Model"]

        best_pipeline = trained_pipelines[best_model_name]

        print(f"\nBest Model for {role_name}: {best_model_name}")

        # ---------------- SHAP EXPLAINABILITY ----------------
        print("Generating SHAP plots with named features...")

        preprocessor_fitted = best_pipeline.named_steps["preprocessor"]
        model_fitted = best_pipeline.named_steps["model"]

        raw_feature_names = preprocessor_fitted.get_feature_names_out()
        if role_name == "batter":
            clean_names = [
                f.replace("cat__batsman_", "Batter: ")
                 .replace("cat__batting_team_", "Team: ")
                 .replace("cat__bowling_team_", "Opponent: ")
                 .replace("cat__venue_", "Venue: ")
                 .replace("num__", "")
                 .replace("_", " ")
                for f in raw_feature_names
            ]
        else:
            clean_names = [
                f.replace("cat__bowler_", "Bowler: ")
                 .replace("cat__bowling_team_", "Team: ")
                 .replace("cat__batting_team_", "Opponent: ")
                 .replace("cat__venue_", "Venue: ")
                 .replace("num__", "")
                 .replace("_", " ")
                for f in raw_feature_names
            ]

        X_test_transformed = preprocessor_fitted.transform(X_test)

        explainer = shap.TreeExplainer(model_fitted)
        sample_size = min(300, X_test_transformed.shape[0])
        sample_idx = np.random.RandomState(42).choice(X_test_transformed.shape[0], sample_size, replace=False)
        X_sample = X_test_transformed[sample_idx]
        shap_values = explainer.shap_values(X_sample)

        os.makedirs("artifacts/shap", exist_ok=True)

        plt.figure(figsize=(9, 6), dpi=150)
        shap.summary_plot(shap_values, X_sample, feature_names=clean_names, max_display=10, show=False)
        plt.title(f"{role_name.capitalize()} Model — Top Feature Impact Distribution (SHAP)", fontsize=12, pad=12)
        plt.tight_layout()
        plt.savefig(f"artifacts/shap/{role_name}_shap_summary.png", bbox_inches="tight")
        plt.close()

        plt.figure(figsize=(9, 6), dpi=150)
        shap.summary_plot(shap_values, X_sample, feature_names=clean_names, plot_type="bar", max_display=10, show=False)
        plt.title(f"{role_name.capitalize()} Model — Mean Absolute SHAP Feature Importance", fontsize=12, pad=12)
        plt.tight_layout()
        plt.savefig(f"artifacts/shap/{role_name}_shap_importance.png", bbox_inches="tight")
        plt.close()


        print("SHAP plots saved.")

        # ---------------- SAVE BEST MODEL ----------------
        model_path = f"artifacts/models/{role_name}_best_model.pkl"
        joblib.dump(best_pipeline, model_path)

        print(f"Best model saved at: {model_path}")

        return best_pipeline
