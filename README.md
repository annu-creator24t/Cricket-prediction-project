# Cricket Performance Analytics

An end-to-end Machine Learning and Analytics web application built for predicting IPL player match performance (Runs scored for Batters, Wickets taken for Bowlers) with explainable AI (SHAP) and comprehensive player performance analytics.

Developed as part of **Infosys Springboard**.

---

## Key Features

1. **Match Performance Prediction**:
   - Gradient Boosted regression models (CatBoost, XGBoost, LightGBM, Random Forest ensembles) trained on historical IPL deliveries and match datasets.
   - Dynamic player selection with automatic historical form autofill (previous match score, last 5 average, last 10 average, career average).
   - Scenario modeling for different venue and opposition franchise combinations.

2. **Player Performance Analytics**:
   - Rolling match performance trends (Last 15 matches).
   - Score and wicket frequency distributions.
   - Venue-specific averages and historical output.
   - Opposition breakdown against all IPL franchises.
   - Performance volatility (standard deviation) and short-term momentum tracking.

3. **Model Explainability (SHAP)**:
   - Global feature importance rankings and summary impact distributions for model transparency.

---

## Project Architecture

```
cricket-performance-prediction/
├── app/
│   ├── streamlit_app.py               # Main dashboard entry point (Overview)
│   ├── ui_theme.py                    # Shared enterprise UI design system & styling
│   └── pages/
│       ├── 1_Match_Prediction.py      # Match performance prediction interface
│       └── 2_Player_Analytics.py      # Player analytics, trends & SHAP reports
├── artifacts/
│   ├── dataset/                       # Raw datasets (deliveries.csv, matches.csv)
│   ├── models/                        # Serialized ML pipelines & evaluation metrics
│   ├── processed/                     # Preprocessed training datasets
│   └── shap/                          # SHAP summary & importance plots
├── config/
│   └── config.yaml                    # System configuration & hyperparameters
├── data/
│   └── raw/                           # Initial dataset files
├── notebooks/                         # EDA, feature engineering & training notebooks
├── src/
│   ├── components/
│   │   ├── predictor.py               # Inference engine & player stats loader
│   │   ├── preprocessing.py           # Preprocessing paths and constants
│   │   └── trainer.py                 # Baseline & model training component
│   ├── pipeline/
│   │   ├── data_ingestion.py          # Raw data ingestion pipeline
│   │   ├── data_preprocessing.py      # Data cleaning & merging
│   │   ├── feature_engineering.py     # Rolling stats & match aggregation
│   │   └── training_pipeline.py       # Multi-model training, eval & SHAP generation
│   └── utils/
│       └── common.py                  # Common file & serialization helpers
├── main.py                            # End-to-end ML pipeline runner
├── requirements.txt                   # Project dependencies
└── setup.py                           # Package installer
```


---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.8 to 3.11
- Git

### 2. Installation
Clone the repository and install dependencies:

```bash
# Clone the repository
git clone <repository-url>
cd cricket-performance-prediction

# (Optional) Create and activate a virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Running the ML Pipeline (Optional / Retraining)
To run the full ingestion, preprocessing, feature engineering, and model training pipeline from scratch:

```bash
python main.py
```

This will:
1. Ingest deliveries and matches data.
2. Clean and merge ball-by-ball and match records.
3. Compute rolling 5/10 match metrics and career averages.
4. Train candidate regression models (CatBoost, XGBoost, LightGBM, Random Forest, Extra Trees) with a time-aware split.
5. Save the best models to `artifacts/models/` and SHAP visualizations to `artifacts/shap/`.

### 4. Starting the Web Application
Launch the Streamlit web dashboard:

```bash
streamlit run app/streamlit_app.py
```

The application will open automatically in your browser at `http://localhost:8501`.

---

## 📊 Model Evaluation Summary

| Role | Best Model | Test RMSE | Test MAE | Test R² |
| :--- | :--- | :--- | :--- | :--- |
| **Batter (Runs)** | CatBoost Regressor | ~22.29 | ~16.92 | ~0.098 |
| **Bowler (Wickets)** | CatBoost Regressor | ~1.07 | ~0.84 | ~0.019 |

---

## 🛡️ License & Acknowledgements
Developed as part of the Infosys Springboard internship/learning program.
