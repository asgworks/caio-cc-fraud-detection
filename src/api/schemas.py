"""
Pydantic schemas for API request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional


class TransactionRequest(BaseModel):
    """Request schema for fraud prediction"""
    trans_num: str = Field(..., description="Transaction ID")
    cc_num: str = Field(..., description="Credit card number")
    merchant: str = Field(..., description="Merchant name")
    amt: float = Field(..., description="Transaction amount", ge=0)
    city_pop: int = Field(..., description="City population", ge=0)
    category_encoded: int = Field(..., description="Transaction category code")
    gender_encoded: int = Field(..., description="Gender code (0=F, 1=M)")
    state_encoded: int = Field(..., description="State code")
    
    class Config:
        json_schema_extra = {
            "example": {
                "trans_num": "txn_12345",
                "cc_num": "1234567890123456",
                "merchant": "Amazon",
                "amt": 49.99,
                "city_pop": 50000,
                "category_encoded": 8,
                "gender_encoded": 1,
                "state_encoded": 5
            }
        }


class PredictionResponse(BaseModel):
    """Response schema for fraud prediction"""
    trans_num: str
    is_fraud: bool
    fraud_probability: float = Field(..., ge=0, le=1)
    model_version: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "trans_num": "txn_12345",
                "is_fraud": False,
                "fraud_probability": 0.02,
                "model_version": "fraud_detector/1"
            }
        }


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    mlflow_connected: bool
    feast_connected: bool
    model_loaded: bool
