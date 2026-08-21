from setuptools import setup, find_packages

setup(
    name="cricket_performance_prediction",
    version="1.0.0",
    author="Your Name",
    description="IPL Player Performance Prediction System (Runs & Wickets)",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "scikit-learn",
        "xgboost",
        "lightgbm",
        "catboost",
        "shap",
        "matplotlib",
        "plotly",
        "streamlit",
        "joblib"
    ],
    python_requires=">=3.8",
)
