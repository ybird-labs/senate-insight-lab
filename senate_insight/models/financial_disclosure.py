"""Data models for financial disclosures and stock transactions."""

from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field


class StockTransaction(BaseModel):
    """Represents a stock transaction by a Congress member."""
    
    transaction_id: str = Field(..., description="Unique identifier for the transaction")
    member_id: str = Field(..., description="Congress member identifier")
    ticker: str = Field(..., description="Stock ticker symbol")
    company_name: str = Field(..., description="Company name")
    transaction_type: str = Field(..., description="Buy, Sell, Exchange")
    transaction_date: date = Field(..., description="Date of transaction")
    disclosure_date: date = Field(..., description="Date disclosed")
    amount_range: str = Field(..., description="Amount range (e.g., '$1,001-$15,000')")
    min_amount: Optional[Decimal] = Field(None, description="Minimum transaction amount")
    max_amount: Optional[Decimal] = Field(None, description="Maximum transaction amount")
    asset_type: str = Field(default="Stock", description="Type of asset")
    owner: str = Field(..., description="Who owns the asset (Self, Spouse, Child)")
    
    class Config:
        json_encoders = {
            date: lambda v: v.isoformat() if v else None,
            Decimal: lambda v: str(v) if v else None
        }


class FinancialDisclosure(BaseModel):
    """Represents a financial disclosure filing."""
    
    filing_id: str = Field(..., description="Unique filing identifier")
    member_id: str = Field(..., description="Congress member identifier")
    filing_type: str = Field(..., description="Type of filing (Annual, Periodic Transaction Report)")
    filing_date: date = Field(..., description="Date of filing")
    reporting_period_start: date = Field(..., description="Start of reporting period")
    reporting_period_end: date = Field(..., description="End of reporting period")
    transactions: List[StockTransaction] = Field(default_factory=list, description="Transactions in this filing")
    
    class Config:
        json_encoders = {
            date: lambda v: v.isoformat() if v else None
        }


class StockPrice(BaseModel):
    """Represents stock price data."""
    
    ticker: str = Field(..., description="Stock ticker symbol")
    price_date: date = Field(..., description="Date of price data")
    open_price: Decimal = Field(..., description="Opening price")
    close_price: Decimal = Field(..., description="Closing price")
    high_price: Decimal = Field(..., description="High price")
    low_price: Decimal = Field(..., description="Low price")
    volume: int = Field(..., description="Trading volume")
    
    class Config:
        json_encoders = {
            date: lambda v: v.isoformat() if v else None,
            Decimal: lambda v: str(v) if v else None
        }


class InsiderTradingAlert(BaseModel):
    """Represents a potential insider trading alert."""
    
    alert_id: str = Field(..., description="Unique alert identifier")
    member_id: str = Field(..., description="Congress member identifier")
    transaction_id: str = Field(..., description="Related transaction identifier")
    alert_type: str = Field(..., description="Type of alert (timing, committee_correlation, etc.)")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")
    description: str = Field(..., description="Human-readable description of the alert")
    legislative_actions: List[str] = Field(default_factory=list, description="Related legislative action IDs")
    price_movement_days: int = Field(..., description="Days after transaction for price movement")
    price_change_percent: Optional[float] = Field(None, description="Stock price change percentage")
    created_at: datetime = Field(default_factory=datetime.now, description="When alert was created")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }