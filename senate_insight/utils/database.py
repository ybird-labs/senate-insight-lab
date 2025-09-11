"""Database utilities and ORM setup."""

from sqlalchemy import create_engine, Column, String, Date, DateTime, Float, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date
from typing import Optional

from .config import settings

Base = declarative_base()


class CongressMemberDB(Base):
    """Database model for Congress members."""
    __tablename__ = "congress_members"
    
    member_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    chamber = Column(String, nullable=False)
    state = Column(String, nullable=False)
    district = Column(String)
    party = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)


class StockTransactionDB(Base):
    """Database model for stock transactions."""
    __tablename__ = "stock_transactions"
    
    transaction_id = Column(String, primary_key=True)
    member_id = Column(String, nullable=False)
    ticker = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    transaction_type = Column(String, nullable=False)
    transaction_date = Column(Date, nullable=False)
    disclosure_date = Column(Date, nullable=False)
    amount_range = Column(String, nullable=False)
    min_amount = Column(Float)
    max_amount = Column(Float)
    owner = Column(String, nullable=False)


class LegislativeActionDB(Base):
    """Database model for legislative actions."""
    __tablename__ = "legislative_actions"
    
    action_id = Column(String, primary_key=True)
    member_id = Column(String, nullable=False)
    action_type = Column(String, nullable=False)
    bill_id = Column(String, nullable=False)
    bill_title = Column(Text, nullable=False)
    action_date = Column(DateTime, nullable=False)
    position = Column(String)


class InsiderTradingAlertDB(Base):
    """Database model for insider trading alerts."""
    __tablename__ = "insider_trading_alerts"
    
    alert_id = Column(String, primary_key=True)
    member_id = Column(String, nullable=False)
    transaction_id = Column(String, nullable=False)
    alert_type = Column(String, nullable=False)
    confidence_score = Column(Float, nullable=False)
    description = Column(Text, nullable=False)
    price_movement_days = Column(Integer, nullable=False)
    price_change_percent = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


class DatabaseManager:
    """Manages database connections and operations."""
    
    def __init__(self, database_url: Optional[str] = None):
        """Initialize database connection."""
        self.database_url = database_url or settings.database_url
        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
    def create_tables(self):
        """Create all database tables."""
        Base.metadata.create_all(bind=self.engine)
        
    def get_session(self):
        """Get a database session."""
        return self.SessionLocal()


# Global database instance
db_manager = DatabaseManager()