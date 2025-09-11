"""Tests for data models."""

import pytest
from datetime import date, datetime
from decimal import Decimal

from senate_insight.models.congress_member import CongressMember, LegislativeAction
from senate_insight.models.financial_disclosure import StockTransaction, InsiderTradingAlert


class TestCongressMember:
    """Tests for CongressMember model."""
    
    def test_create_congress_member(self):
        """Test creating a CongressMember instance."""
        member = CongressMember(
            member_id="S001",
            name="John Doe",
            chamber="Senate",
            state="CA",
            party="Democratic",
            start_date=date(2021, 1, 3)
        )
        
        assert member.member_id == "S001"
        assert member.name == "John Doe"
        assert member.chamber == "Senate"
        assert member.state == "CA"
        assert member.party == "Democratic"
        assert member.start_date == date(2021, 1, 3)


class TestStockTransaction:
    """Tests for StockTransaction model."""
    
    def test_create_stock_transaction(self):
        """Test creating a StockTransaction instance."""
        transaction = StockTransaction(
            transaction_id="txn_001",
            member_id="S001",
            ticker="AAPL",
            company_name="Apple Inc.",
            transaction_type="Buy",
            transaction_date=date(2023, 10, 1),
            disclosure_date=date(2023, 10, 15),
            amount_range="$1,001-$15,000",
            owner="Self"
        )
        
        assert transaction.ticker == "AAPL"
        assert transaction.company_name == "Apple Inc."
        assert transaction.transaction_type == "Buy"
        assert transaction.transaction_date == date(2023, 10, 1)
    
    def test_transaction_with_amounts(self):
        """Test transaction with min/max amounts."""
        transaction = StockTransaction(
            transaction_id="txn_002",
            member_id="S001",
            ticker="GOOGL",
            company_name="Alphabet Inc.",
            transaction_type="Sell",
            transaction_date=date(2023, 9, 15),
            disclosure_date=date(2023, 9, 30),
            amount_range="$15,001-$50,000",
            min_amount=Decimal("15001"),
            max_amount=Decimal("50000"),
            owner="Spouse"
        )
        
        assert transaction.min_amount == Decimal("15001")
        assert transaction.max_amount == Decimal("50000")
        assert transaction.owner == "Spouse"


class TestInsiderTradingAlert:
    """Tests for InsiderTradingAlert model."""
    
    def test_create_alert(self):
        """Test creating an InsiderTradingAlert instance."""
        alert = InsiderTradingAlert(
            alert_id="alert_001",
            member_id="S001",
            transaction_id="txn_001",
            alert_type="timing_correlation",
            confidence_score=0.75,
            description="Potential insider trading detected",
            price_movement_days=14,
            price_change_percent=12.5
        )
        
        assert alert.confidence_score == 0.75
        assert alert.alert_type == "timing_correlation"
        assert alert.price_change_percent == 12.5
    
    def test_confidence_score_validation(self):
        """Test confidence score is within valid range."""
        with pytest.raises(ValueError):
            InsiderTradingAlert(
                alert_id="alert_002",
                member_id="S001", 
                transaction_id="txn_001",
                alert_type="test",
                confidence_score=1.5,  # Invalid: > 1.0
                description="Test alert",
                price_movement_days=30
            )