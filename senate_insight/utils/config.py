"""Configuration management for Senate Insight Lab."""

import os
from typing import Optional
from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Application settings loaded from environment variables."""
    
    # API Keys
    congress_api_key: Optional[str] = Field(None)
    alpha_vantage_api_key: Optional[str] = Field(None)
    
    # Database Configuration
    database_url: str = Field("sqlite:///senate_insight.db")
    
    # Analysis Parameters
    timing_window_days: int = Field(30)
    significant_price_change: float = Field(0.05)
    min_confidence_threshold: float = Field(0.3)
    
    # Data Collection
    max_concurrent_requests: int = Field(5)
    request_delay_seconds: float = Field(1.0)
    
    # Logging
    log_level: str = Field("INFO")
    log_file: str = Field("senate_insight.log")
    
    def __init__(self, **data):
        # Load from environment variables
        env_data = {
            'congress_api_key': os.getenv('CONGRESS_API_KEY'),
            'alpha_vantage_api_key': os.getenv('ALPHA_VANTAGE_API_KEY'),
            'database_url': os.getenv('DATABASE_URL', 'sqlite:///senate_insight.db'),
            'timing_window_days': int(os.getenv('TIMING_WINDOW_DAYS', '30')),
            'significant_price_change': float(os.getenv('SIGNIFICANT_PRICE_CHANGE', '0.05')),
            'min_confidence_threshold': float(os.getenv('MIN_CONFIDENCE_THRESHOLD', '0.3')),
            'max_concurrent_requests': int(os.getenv('MAX_CONCURRENT_REQUESTS', '5')),
            'request_delay_seconds': float(os.getenv('REQUEST_DELAY_SECONDS', '1.0')),
            'log_level': os.getenv('LOG_LEVEL', 'INFO'),
            'log_file': os.getenv('LOG_FILE', 'senate_insight.log'),
        }
        env_data.update(data)
        super().__init__(**env_data)


# Global settings instance
settings = Settings()