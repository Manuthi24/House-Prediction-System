from pydantic import BaseModel, Field
from typing import Optional


class HouseFeatures(BaseModel):
    bedrooms: int = Field(..., ge=0, le=33, description="Number of bedrooms")
    bathrooms: float = Field(..., ge=0, le=8, description="Number of bathrooms")
    sqft_living: int = Field(..., ge=290, le=13540, description="Square footage of living space")
    sqft_lot: int = Field(..., ge=520, le=1651359, description="Square footage of lot")
    floors: float = Field(..., ge=1, le=3.5, description="Number of floors")
    waterfront: int = Field(..., ge=0, le=1, description="Waterfront property (0 or 1)")
    view: int = Field(..., ge=0, le=4, description="View quality (0-4)")
    condition: int = Field(..., ge=1, le=5, description="Condition of the house (1-5)")
    grade: int = Field(..., ge=1, le=13, description="Overall grade (1-13)")
    sqft_above: int = Field(..., ge=290, le=9410, description="Square footage above ground")
    sqft_basement: int = Field(..., ge=0, le=4820, description="Square footage of basement")
    yr_built: int = Field(..., ge=1900, le=2015, description="Year built")
    yr_renovated: int = Field(..., ge=0, le=2015, description="Year renovated (0 if never)")
    zipcode: int = Field(..., description="Zipcode")
    lat: float = Field(..., description="Latitude")
    long: float = Field(..., description="Longitude")
    sqft_living15: int = Field(..., description="Average sqft of 15 nearest neighbors living area")
    sqft_lot15: int = Field(..., description="Average sqft of 15 nearest neighbors lot")

    model_config = {
        "json_schema_extra": {
            "example": {
                "bedrooms": 3,
                "bathrooms": 2.0,
                "sqft_living": 1800,
                "sqft_lot": 7500,
                "floors": 1.0,
                "waterfront": 0,
                "view": 0,
                "condition": 3,
                "grade": 7,
                "sqft_above": 1800,
                "sqft_basement": 0,
                "yr_built": 1985,
                "yr_renovated": 0,
                "zipcode": 98178,
                "lat": 47.5112,
                "long": -122.257,
                "sqft_living15": 1340,
                "sqft_lot15": 5650,
            }
        }
    }


class PredictionResponse(BaseModel):
    predicted_price: float = Field(..., description="Predicted house price in USD")
    formatted_price: str = Field(..., description="Formatted price string")
    confidence_range: dict = Field(..., description="Low and high confidence range")
    model_version: str = Field(default="1.0.0")