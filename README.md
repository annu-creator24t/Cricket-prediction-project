# Cricket Performance Analytics

An end-to-end Machine Learning web application built to predict individual player performance in the Indian Premier League (IPL) and deliver interactive performance analytics with explainable AI (SHAP).

Developed by **Annu Tiwari** as part of **Infosys Springboard**.

---

## 1. Project Overview

Predicting individual cricket player output is challenging due to the dynamic nature of match situations, venue characteristics, and short-term player form. This project builds a complete machine learning pipeline and interactive Streamlit web dashboard to:

1. **Forecast Match Performance**: Predict expected runs scored for batters and wickets taken for bowlers in upcoming fixtures using trained gradient-boosted regression models.
2. **Analyze Player Form**: Track match-by-match scoring timelines, rolling 5/10-match moving averages, score frequency distributions, and venue/opponent breakdowns.
3. **Explain Model Drivers**: Provide model transparency through SHAP (SHapley Additive exPlanations) feature attribution charts.

---

## 2. Dataset & Preprocessing

- **Data Source**: Ball-by-ball IPL dataset (2008–2024 seasons) comprising **1,100 total matches** and over **260,000 delivery records** sourced from open cricket databases (Cricsheet / Kaggle).
- **Tracked Scope**: 285 distinct batters and 245 distinct bowlers across 58 match venues.
- **Feature Engineering**:
  - `prev_runs` / `prev_wickets`: Player output in the immediately preceding match.
  - `last_5_avg` / `last_5_wkts`: Rolling moving average over the player's last 5 completed matches.
  - `last_10_avg` / `last_10_wkts`: Rolling moving average over the player's last 10 completed matches.
  - `career_avg` / `career_wkt_avg`: Expanding career baseline average up to the match date.
  - Categorical features: `batsman`/`bowler`, `batting_team`, `bowling_team`, and `venue` (One-Hot Encoded).

---

## 3. Machine Learning Methodology & Evaluation

- **Train/Test Split**: Chronological 80/20 time-aware split on match dates (preserving time-series order without future lookahead data leakage).
- **Candidate Models Evaluated**: CatBoost Regressor, XGBoost Regressor, LightGBM Regressor, Random Forest, and Extra Trees Regressors.
- **Selected Best Model**: **CatBoost Regressor** for both Batter and Bowler targets.

### Test Set Benchmark Results

| Role / Target | Selected Model | Test RMSE | Test MAE | Test R² | Baseline 10-Match Moving Avg RMSE |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Batter (Runs)** | CatBoost Regressor | **22.29** | **16.92** | **0.098** | 23.47 |
| **Bowler (Wickets)** | CatBoost Regressor | **1.07** | **0.84** | **0.019** | 1.08 |

*Note: High variance in individual T20 cricket innings makes individual runs and wickets difficult to predict with high R²; the regression models focus on outperforming naive moving average baselines and capturing venue/matchup signals.*

---

## 4. Project Structure

```
cricket-performance-prediction/
├── app/
│   ├── streamlit_app.py               # Overview dashboard & dataset summary
│   ├── ui_theme.py                    # Enterprise styling tokens & sidebar attribution
│   └── pages/
│       ├── 1_Match_Prediction.py      # Match prediction interface with scenario tuning
│       └── 2_Player_Analytics.py      # Player analytics, distributions & SHAP insights
├── artifacts/
│   ├── dataset/                       # Ingested matches.csv & deliveries.csv
│   ├── models/                        # Serialized .pkl pipelines & evaluation metrics
│   ├── processed/                     # Preprocessed training datasets
│   └── shap/                          # Named SHAP summary & importance charts
├── config/
│   └── config.yaml                    # System configuration & hyperparameters
├── data/
│   └── raw/                           # Raw input datasets
├── notebooks/                         # EDA, feature engineering & training notebooks
├── src/
│   ├── components/
│   │   ├── predictor.py               # Unified stats loader & inference engine
│   │   ├── preprocessing.py           # Artifact directory paths & constants
│   │   └── trainer.py                 # Multi-model training & SHAP generation
│   ├── pipeline/
│   │   ├── data_ingestion.py          # Data ingestion pipeline
│   │   ├── data_preprocessing.py      # Cleaning & delivery-match merging
│   │   ├── feature_engineering.py     # Rolling stats computation
│   │   └── training_pipeline.py       # End-to-end training pipeline runner
│   └── utils/
│       └── common.py                  # Serialization & file utilities
├── main.py                            # Pipeline execution script
├── requirements.txt                   # Dependency specifications
└── setup.py                           # Package installer
```

---

## 5. Setup & Running Instructions

### 1. Prerequisites
- Python 3.8 to 3.11 installed
- Git

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/annu-creator24t/Cricket-prediction-project.git
cd Cricket-prediction-project

# (Optional) Create a virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install required dependencies
pip install -r requirements.txt
```

### 3. Running the Web Application
```bash
python -m streamlit run app/streamlit_app.py
```
Open your browser at `http://localhost:8501`.

### 4. (Optional) Retraining Models from Scratch
```bash
python main.py
```
This runs data ingestion, cleaning, feature engineering, multi-model evaluation, and saves serialized models and named SHAP plots to `artifacts/`.

---

## 6. Project Attribution
- **Developer**: Annu Tiwari
- **Program**: Infosys Springboard Project Work
- **Evaluation**: Capstone Submission

