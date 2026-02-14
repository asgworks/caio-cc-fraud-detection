"""
Feature Store Utilities
Provides helper functions for interacting with Feast feature store
"""
from typing import List, Dict, Optional
import pandas as pd
from feast import FeatureStore
from pathlib import Path


class FraudFeatureStore:
    """Wrapper for Feast FeatureStore with fraud detection specific methods"""
    
    def __init__(self, repo_path: str = "../feature_store"):
        """
        Initialize the feature store
        
        Args:
            repo_path: Path to the feature store repository
        """
        self.repo_path = Path(repo_path)
        self.store = FeatureStore(repo_path=str(self.repo_path))
    
    def get_historical_features(
        self,
        entity_df: pd.DataFrame,
        features: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Get historical features for training
        
        Args:
            entity_df: DataFrame with entity keys and timestamps
            features: List of features to retrieve. If None, uses fraud_detection_v1 service
            
        Returns:
            DataFrame with requested features joined
        """
        if features is None:
            # Use the default feature service
            features = ["fraud_detection_v1"]
        
        training_df = self.store.get_historical_features(
            entity_df=entity_df,
            features=features,
        ).to_df()
        
        return training_df
    
    def get_online_features(
        self,
        entity_rows: List[Dict],
        features: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Get online features for real-time prediction
        
        Args:
            entity_rows: List of entity dictionaries with keys
            features: List of features to retrieve
            
        Returns:
            DataFrame with features for each entity
        """
        if features is None:
            features = ["fraud_detection_v1"]
            
        feature_vector = self.store.get_online_features(
            features=features,
            entity_rows=entity_rows,
        ).to_df()
        
        return feature_vector
    
    def materialize(
        self,
        start_date: str,
        end_date: str
    ):
        """
        Materialize features to online store for serving
        
        Args:
            start_date: Start date in ISO format (YYYY-MM-DD)
            end_date: End date in ISO format (YYYY-MM-DD)
        """
        from datetime import datetime
        
        start_dt = datetime.fromisoformat(start_date)
        end_dt = datetime.fromisoformat(end_date)
        
        self.store.materialize(
            start_date=start_dt,
            end_date=end_dt
        )
        print(f"Materialized features from {start_date} to {end_date}")
    
    def list_feature_views(self) -> List[str]:
        """List all available feature views"""
        return [fv.name for fv in self.store.list_feature_views()]
    
    def list_feature_services(self) -> List[str]:
        """List all available feature services"""
        return [fs.name for fs in self.store.list_feature_services()]
    
    def get_feature_service_features(self, service_name: str) -> List[str]:
        """Get all features in a feature service"""
        service = self.store.get_feature_service(service_name)
        features = []
        for projection in service.feature_view_projections:
            for feature in projection.features:
                features.append(f"{projection.name}:{feature.name}")
        return features


# Convenience function
def get_fraud_feature_store(repo_path: str = "../feature_store") -> FraudFeatureStore:
    """Get an instance of the fraud detection feature store"""
    return FraudFeatureStore(repo_path=repo_path)
