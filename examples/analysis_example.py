#!/usr/bin/env python3
"""
Advanced analysis example showing how to customize the detection algorithms.
"""

from datetime import date, timedelta
from senate_insight.models.congress_member import CongressMember, LegislativeAction, CommitteeAssignment
from senate_insight.models.financial_disclosure import StockTransaction, StockPrice
from senate_insight.analyzers.insider_trading_detector import InsiderTradingDetector


def create_sample_data():
    """Create sample data for demonstration."""
    
    # Sample Congress member
    member = CongressMember(
        member_id="S001",
        name="Jane Doe",
        chamber="Senate",
        state="CA",
        party="Democratic",
        start_date=date(2021, 1, 3),
        committees=["Banking", "Finance"]
    )
    
    # Sample stock transaction
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
    
    # Sample legislative action (tech-related bill)
    legislative_action = LegislativeAction(
        action_id="vote_001",
        member_id="S001",
        action_type="vote",
        bill_id="S.123",
        bill_title="Technology Innovation and Competition Act",
        action_date=date(2023, 10, 10).strftime("%Y-%m-%dT00:00:00"),
        position="Yes",
        industries_affected=["technology", "telecommunications"]
    )
    
    # Sample committee assignment
    committee = CommitteeAssignment(
        member_id="S001",
        committee_name="Banking, Housing, and Urban Affairs",
        committee_code="BANK",
        start_date=date(2021, 1, 3)
    )
    
    # Sample stock prices (showing price increase after transaction)
    base_price = 150.0
    stock_prices = []
    
    for i in range(-30, 31):  # 30 days before and after transaction
        price_date = date(2023, 10, 1) + timedelta(days=i)
        
        # Simulate price increase after transaction date
        if i <= 0:
            price = base_price + (i * 0.1)  # Slight decline before
        else:
            price = base_price + (i * 0.5)  # Increase after
        
        stock_prices.append(StockPrice(
            ticker="AAPL",
            price_date=price_date,
            open_price=price - 1,
            close_price=price,
            high_price=price + 2,
            low_price=price - 2,
            volume=1000000 + (i * 10000)  # Increasing volume
        ))
    
    return member, [transaction], [legislative_action], [committee], {"AAPL": stock_prices}


def main():
    """Run analysis example with sample data."""
    print("🔍 Senate Insight Lab - Analysis Example")
    print("=" * 45)
    
    # Create sample data
    member, transactions, legislative_actions, committees, stock_prices = create_sample_data()
    
    print(f"Analyzing member: {member.name}")
    print(f"Transactions: {len(transactions)}")
    print(f"Legislative actions: {len(legislative_actions)}")
    print(f"Stock prices: {len(stock_prices['AAPL'])} days")
    
    # Initialize detector
    detector = InsiderTradingDetector()
    
    # Run analysis
    alerts = detector.analyze_member_activity(
        member, transactions, legislative_actions, committees, stock_prices
    )
    
    print(f"\n📋 Analysis Results:")
    print(f"Alerts generated: {len(alerts)}")
    
    for alert in alerts:
        confidence_emoji = "🚨" if alert.confidence_score >= 0.7 else "⚠️" if alert.confidence_score >= 0.5 else "ℹ️"
        print(f"\n{confidence_emoji} Alert (Confidence: {alert.confidence_score:.2f})")
        print(f"   Type: {alert.alert_type}")
        print(f"   Description: {alert.description}")
    
    print("\n💡 This example shows how the system detects potential insider trading")
    print("   based on timing correlation between trades and legislative actions.")


if __name__ == "__main__":
    main()