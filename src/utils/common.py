import os
import sys
import joblib
import pandas as pd


def save_object(file_path, obj):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    joblib.dump(obj, file_path)


def load_object(file_path):
    return joblib.load(file_path)


def read_csv_data(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    return pd.read_csv(path)
