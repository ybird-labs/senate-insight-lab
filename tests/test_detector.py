"""Tests for insider trading detector."""

import pytest
from datetime import date, datetime, timedelta
from decimal import Decimal

from senate_insight.analyzers.insider_trading_detector import InsiderTradingDetector
from senate_insight.models.congress_member import CongressMember, LegislativeAction, CommitteeAssignment
from senate_insight.models.financial_disclosure import StockTransaction, StockPrice


class TestInsiderTradingDetector:
    """Tests for InsiderTradingDetector class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.detector = InsiderTradingDetector()
        
        self.member = CongressMember(
            member_id="S001",
            name="Test Member",
            chamber="Senate",
            state="CA",
            party="Democratic",
            start_date=date(2021, 1, 3)
        )
    
    def test_timing_score_calculation(self):
        """Test timing score calculation for transactions and legislative actions."""
        # Create transaction
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
        
        # Create legislative action after transaction (suspicious timing)
        legislative_action = LegislativeAction(
            action_id="vote_001",
            member_id="S001",
            action_type="vote",
            bill_id="S.123",
            bill_title="Technology Innovation Act affecting Apple Inc.",
            action_date=datetime(2023, 10, 10),  # 9 days after transaction
            position="Yes"
        )
        
        # Mock stock prices
        stock_prices = []
        for i in range(30):
            price_date = date(2023, 9, 15) + timedelta(days=i)
            stock_prices.append(StockPrice(
                ticker="AAPL",
                price_date=price_date,
                open_price=Decimal("150"),
                close_price=Decimal("151"),
                high_price=Decimal("152"),
                low_price=Decimal("149"),
                volume=1000000
            ))
        
        # Calculate timing score
        score = self.detector._calculate_timing_score(
            transaction, [legislative_action], stock_prices
        )
        
        # Should have high timing score (transaction before related action)
        assert score > 0.5
    
    def test_committee_correlation_score(self):
        """Test committee correlation scoring."""
        # Create transaction in tech stock
        transaction = StockTransaction(
            transaction_id="txn_002",
            member_id="S001",
            ticker="GOOGL",
            company_name="Alphabet Inc Technology",  # Contains "technology"
            transaction_type="Buy",
            transaction_date=date(2023, 10, 1),
            disclosure_date=date(2023, 10, 15),
            amount_range="$1,001-$15,000",
            owner="Self"
        )
        
        # Member serves on technology-related committee
        committee = CommitteeAssignment(
            member_id="S001",
            committee_name="Commerce, Science, and Transportation",  # Related to tech
            committee_code="COMM",
            start_date=date(2021, 1, 3)
        )
        
        score = self.detector._calculate_committee_correlation(transaction, [committee])
        
        # Should have positive correlation score
        assert score > 0.0
    
    def test_price_movement_score_buy(self):
        """Test price movement score for buy transactions."""
        transaction = StockTransaction(
            transaction_id="txn_003",
            member_id="S001",
            ticker="AAPL",
            company_name="Apple Inc.",
            transaction_type="Buy",
            transaction_date=date(2023, 10, 1),
            disclosure_date=date(2023, 10, 15),
            amount_range="$1,001-$15,000",
            owner="Self"
        )
        
        # Create stock prices showing increase after transaction
        stock_prices = []
        base_price = Decimal("150")
        
        # Prices before transaction
        for i in range(-10, 0):
            price_date = date(2023, 10, 1) + timedelta(days=i)
            stock_prices.append(StockPrice(
                ticker="AAPL",
                price_date=price_date,
                open_price=base_price,
                close_price=base_price,
                high_price=base_price + 2,
                low_price=base_price - 2,
                volume=1000000
            ))
        
        # Transaction day
        stock_prices.append(StockPrice(
            ticker="AAPL",
            price_date=date(2023, 10, 1),
            open_price=base_price,
            close_price=base_price,
            high_price=base_price + 2,
            low_price=base_price - 2,
            volume=1000000
        ))
        
        # Prices after transaction (significant increase)
        for i in range(1, 31):
            price_date = date(2023, 10, 1) + timedelta(days=i)
            # 20% price increase over 30 days
            new_price = base_price + (base_price * Decimal("0.20"))
            stock_prices.append(StockPrice(
                ticker="AAPL",
                price_date=price_date,
                open_price=new_price,
                close_price=new_price,
                high_price=new_price + 2,
                low_price=new_price - 2,
                volume=1000000
            ))
        
        score = self.detector._calculate_price_movement_score(transaction, stock_prices)
        
        # Should have high score for favorable price movement
        assert score >= 0.7
    
    def test_no_alerts_for_low_confidence(self):
        """Test that no alerts are generated for low confidence scores."""
        # Create minimal data that should result in low confidence
        transaction = StockTransaction(
            transaction_id="txn_004",
            member_id="S001",
            ticker="XYZ",
            company_name="Random Corp",
            transaction_type="Buy",
            transaction_date=date(2023, 10, 1),
            disclosure_date=date(2023, 10, 15),
            amount_range="$1,001-$15,000",
            owner="Self"
        )
        
        # No related legislative actions or committee assignments
        alerts = self.detector.analyze_member_activity(
            self.member, [transaction], [], [], {}
        )
        
        # Should generate no alerts due to lack of suspicious indicators
        assert len(alerts) == 0