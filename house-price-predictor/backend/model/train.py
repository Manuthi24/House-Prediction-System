"""
Training script for the King County House Price Predictor.
Run this script to train the model and save it as model.pkl.

Usage:
    python train.py --data path/to/kc_house_data.csv
"""

import argparse
import os
import sys
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error

# ── Feature engineering ──────────────────────────────────────────────────────

FEATURES = [
    "bedrooms", "bathrooms", "sqft_living", "sqft_lot", "floors",
    "waterfront", "view", "condition", "grade", "sqft_above",
    "sqft_basement", "yr_built", "yr_renovated", "zipcode",
    "lat", "long", "sqft_living15", "sqft_lot15",
]

ENGINEERED = [
    "house_age", "renovated", "price_per_sqft_proxy",
    "total_sqft", "bed_bath_ratio",
]


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["house_age"] = 2015 - df["yr_built"]
    df["renovated"] = (df["yr_renovated"] > 0).astype(int)
    df["total_sqft"] = df["sqft_living"] + df["sqft_lot"]
    df["bed_bath_ratio"] = df["bedrooms"] / (df["bathrooms"].replace(0, 0.5))
    # proxy: sqft_living / (grade + 1)  – no leakage since grade is a known input
    df["price_per_sqft_proxy"] = df["sqft_living"] / (df["grade"] + 1)
    return df


# ── Main ──────────────────────────────────────────────────────────────────────

def train(data_path: str, output_path: str = None) -> None:
    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), "model.pkl")

    print(f"[1/5] Loading data from: {data_path}")
    df = pd.read_csv(data_path)
    print(f"      {len(df):,} rows loaded.")

    print("[2/5] Feature engineering …")
    df = engineer_features(df)
    all_features = FEATURES + ENGINEERED
    X = df[all_features]
    y = df["price"]

    print("[3/5] Splitting train / test …")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("[4/5] Training Gradient Boosting model …")
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", GradientBoostingRegressor(
            n_estimators=300,
            learning_rate=0.08,
            max_depth=5,
            min_samples_split=10,
            subsample=0.8,
            random_state=42,
        )),
    ])
    pipeline.fit(X_train, y_train)

    print("[5/5] Evaluating …")
    preds = pipeline.predict(X_test)
    mae  = mean_absolute_error(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    r2   = r2_score(y_test, preds)

    print(f"\n  MAE : ${mae:,.0f}")
    print(f"  RMSE: ${rmse:,.0f}")
    print(f"  R²  : {r2:.4f}")

    # Persist pipeline + metadata
    artifact = {
        "pipeline": pipeline,
        "features": all_features,
        "metrics": {"mae": mae, "rmse": rmse, "r2": r2},
        "version": "1.0.0",
    }
    joblib.dump(artifact, output_path)
    print(f"\n[OK] Model saved to: {output_path}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train house price model")
    parser.add_argument(
        "--data",
        required=True,
        help="Path to kc_house_data.csv",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Where to save model.pkl (default: same folder as train.py)",
    )
    args = parser.parse_args()

    if not os.path.exists(args.data):
        print(f"Error: data file not found: {args.data}", file=sys.stderr)
        sys.exit(1)

    train(args.data, args.output)