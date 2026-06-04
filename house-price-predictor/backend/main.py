"""
FastAPI backend for King County House Price Predictor.

Start the server:
    uvicorn main:app --reload --port 8000
"""

import os
import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from schemas import HouseFeatures, PredictionResponse

# ── App setup ─────────────────────────────────────────────────────────────────

app = FastAPI(
    title="House Price Predictor API",
    description="Predicts King County (Seattle area) house prices using ML.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Model loading ─────────────────────────────────────────────────────────────

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "model.pkl")

_artifact: dict | None = None


def get_artifact() -> dict:
    global _artifact
    if _artifact is None:
        if not os.path.exists(MODEL_PATH):
            raise HTTPException(
                status_code=503,
                detail=(
                    "Model file not found. "
                    "Run `python model/train.py --data kc_house_data.csv` first."
                ),
            )
        _artifact = joblib.load(MODEL_PATH)
    return _artifact


# ── Feature engineering (mirrors train.py) ───────────────────────────────────

def engineer_features(data: dict) -> pd.DataFrame:
    df = pd.DataFrame([data])
    df["house_age"]           = 2015 - df["yr_built"]
    df["renovated"]           = (df["yr_renovated"] > 0).astype(int)
    df["total_sqft"]          = df["sqft_living"] + df["sqft_lot"]
    df["bed_bath_ratio"]      = df["bedrooms"] / (df["bathrooms"].replace(0, 0.5))
    df["price_per_sqft_proxy"] = df["sqft_living"] / (df["grade"] + 1)
    return df


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "House Price Predictor API is running."}


@app.get("/health", tags=["Health"])
def health():
    try:
        artifact = get_artifact()
        return {
            "status": "ok",
            "model_version": artifact.get("version", "unknown"),
            "metrics": artifact.get("metrics", {}),
        }
    except HTTPException as exc:
        return {"status": "degraded", "detail": exc.detail}


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
def predict(house: HouseFeatures):
    artifact = get_artifact()
    pipeline = artifact["pipeline"]
    features = artifact["features"]

    # Build feature-engineered dataframe
    df = engineer_features(house.model_dump())

    # Ensure column order matches training
    df = df[features]

    raw_pred = pipeline.predict(df)[0]
    price    = max(float(raw_pred), 0.0)

    # Rough ±12 % confidence interval (based on model RMSE ~$130 k)
    low  = price * 0.88
    high = price * 1.12

    return PredictionResponse(
        predicted_price=round(price, 2),
        formatted_price=f"${price:,.0f}",
        confidence_range={
            "low":  f"${low:,.0f}",
            "high": f"${high:,.0f}",
        },
        model_version=artifact.get("version", "1.0.0"),
    )


@app.get("/features", tags=["Meta"])
def feature_info():
    """Return feature names and descriptions for the frontend."""
    return {
        "features": [
            {"name": "bedrooms",      "label": "Bedrooms",           "type": "int",   "min": 0,   "max": 33},
            {"name": "bathrooms",     "label": "Bathrooms",          "type": "float", "min": 0,   "max": 8},
            {"name": "sqft_living",   "label": "Living Area (sqft)", "type": "int",   "min": 290, "max": 13540},
            {"name": "sqft_lot",      "label": "Lot Size (sqft)",    "type": "int",   "min": 520, "max": 1651359},
            {"name": "floors",        "label": "Floors",             "type": "float", "min": 1,   "max": 3.5},
            {"name": "waterfront",    "label": "Waterfront",         "type": "int",   "min": 0,   "max": 1},
            {"name": "view",          "label": "View (0–4)",         "type": "int",   "min": 0,   "max": 4},
            {"name": "condition",     "label": "Condition (1–5)",    "type": "int",   "min": 1,   "max": 5},
            {"name": "grade",         "label": "Grade (1–13)",       "type": "int",   "min": 1,   "max": 13},
            {"name": "sqft_above",    "label": "Above Ground (sqft)","type": "int",   "min": 290, "max": 9410},
            {"name": "sqft_basement", "label": "Basement (sqft)",    "type": "int",   "min": 0,   "max": 4820},
            {"name": "yr_built",      "label": "Year Built",         "type": "int",   "min": 1900,"max": 2015},
            {"name": "yr_renovated",  "label": "Year Renovated",     "type": "int",   "min": 0,   "max": 2015},
            {"name": "zipcode",       "label": "Zipcode",            "type": "int"},
            {"name": "lat",           "label": "Latitude",           "type": "float"},
            {"name": "long",          "label": "Longitude",          "type": "float"},
            {"name": "sqft_living15", "label": "Neighbors Avg Living (sqft)", "type": "int"},
            {"name": "sqft_lot15",    "label": "Neighbors Avg Lot (sqft)",    "type": "int"},
        ]
    }