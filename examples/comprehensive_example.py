#!/usr/bin/env python3
"""
Comprehensive example showing the full Senate Insight Lab workflow.

This demonstrates:
1. Loading multiple members and transactions
2. Running batch analysis
3. Generating different types of alerts
4. Creating summary reports
"""

import sys
sys.path.insert(0, '.')

from datetime import date, timedelta, datetime
from decimal import Decimal
from senate_insight.models.congress_member import CongressMember, LegislativeAction, CommitteeAssignment
from senate_insight.models.financial_disclosure import StockTransaction, StockPrice
from senate_insight.analyzers.insider_trading_detector import InsiderTradingDetector


def create_comprehensive_dataset():
    """Create a comprehensive dataset for demonstration."""
    
    # Multiple Congress members
    members = [
        CongressMember(
            member_id="S001",
            name="Senator Tech",
            chamber="Senate",
            state="CA",
            party="Democratic",
            start_date=date(2021, 1, 3),
            committees=["Technology Committee", "Commerce"]
        ),
        CongressMember(
            member_id="H001",
            name="Rep Healthcare",
            chamber="House",
            state="TX",
            party="Republican",
            start_date=date(2021, 1, 3),
            committees=["Energy and Commerce", "Health Subcommittee"]
        ),
        CongressMember(
            member_id="S002",
            name="Senator Finance",
            chamber="Senate",
            state="NY",
            party="Democratic",
            start_date=date(2019, 1, 3),
            committees=["Banking", "Finance"]
        )
    ]
    
    # Multiple transactions with different patterns
    transactions = [
        # High suspicion: Tech stock bought before tech legislation
        StockTransaction(
            transaction_id="txn_001",
            member_id="S001",
            ticker="GOOGL",
            company_name="Alphabet Inc Technology",
            transaction_type="Buy",
            transaction_date=date(2023, 9, 15),
            disclosure_date=date(2023, 9, 30),
            amount_range="$15,001-$50,000",
            min_amount=Decimal("15001"),
            max_amount=Decimal("50000"),
            owner="Self"
        ),
        # Medium suspicion: Healthcare stock by healthcare committee member
        StockTransaction(
            transaction_id="txn_002",
            member_id="H001",
            ticker="PFE",
            company_name="Pfizer Inc Pharmaceutical",
            transaction_type="Buy",
            transaction_date=date(2023, 10, 5),
            disclosure_date=date(2023, 10, 20),
            amount_range="$1,001-$15,000",
            owner="Spouse"
        ),
        # Low suspicion: Bank stock with no committee correlation
        StockTransaction(
            transaction_id="txn_003",
            member_id="S001",  # Tech committee member buying bank stock
            ticker="JPM",
            company_name="JPMorgan Chase & Co",
            transaction_type="Sell",
            transaction_date=date(2023, 8, 1),
            disclosure_date=date(2023, 8, 15),
            amount_range="$1,001-$15,000",
            owner="Self"
        )
    ]
    
    # Legislative actions
    legislative_actions = [
        LegislativeAction(
            action_id="vote_001",
            member_id="S001",
            action_type="vote",
            bill_id="S.123",
            bill_title="AI and Technology Innovation Act affecting major tech companies",
            action_date=datetime(2023, 9, 25),  # 10 days after GOOGL purchase
            position="Yes",
            industries_affected=["technology", "artificial intelligence"]
        ),
        LegislativeAction(
            action_id="vote_002",
            member_id="H001",
            action_type="sponsor",
            bill_id="H.R.456",
            bill_title="Healthcare Innovation and Drug Pricing Reform",
            action_date=datetime(2023, 10, 15),  # 10 days after PFE purchase
            position="Sponsor",
            industries_affected=["healthcare", "pharmaceutical"]
        )
    ]
    
    # Committee assignments
    committees = [
        CommitteeAssignment(
            member_id="S001",
            committee_name="Commerce, Science, and Transportation",
            committee_code="COMM",
            start_date=date(2021, 1, 3)
        ),
        CommitteeAssignment(
            member_id="H001",
            committee_name="Energy and Commerce",
            committee_code="ENRG",
            start_date=date(2021, 1, 3)
        ),
        CommitteeAssignment(
            member_id="S002",
            committee_name="Banking, Housing, and Urban Affairs",
            committee_code="BANK",
            start_date=date(2019, 1, 3)
        )
    ]
    
    # Stock price data for all tickers
    stock_prices = {}
    
    # GOOGL - significant increase after transaction
    googl_prices = []
    base_price = 120.0
    for i in range(-30, 31):
        price_date = date(2023, 9, 15) + timedelta(days=i)
        if i <= 0:
            price = base_price + (i * 0.1)
        else:
            price = base_price + (i * 0.8)  # 24% increase over 30 days
        
        googl_prices.append(StockPrice(
            ticker="GOOGL",
            price_date=price_date,
            open_price=Decimal(str(price - 1)),
            close_price=Decimal(str(price)),
            high_price=Decimal(str(price + 2)),
            low_price=Decimal(str(price - 2)),
            volume=2000000 + (abs(i) * 100000)
        ))
    stock_prices["GOOGL"] = googl_prices
    
    # PFE - moderate increase
    pfe_prices = []
    base_price = 35.0
    for i in range(-30, 31):
        price_date = date(2023, 10, 5) + timedelta(days=i)
        if i <= 0:
            price = base_price
        else:
            price = base_price + (i * 0.2)  # 6% increase over 30 days
        
        pfe_prices.append(StockPrice(
            ticker="PFE",
            price_date=price_date,
            open_price=Decimal(str(price - 0.5)),
            close_price=Decimal(str(price)),
            high_price=Decimal(str(price + 1)),
            low_price=Decimal(str(price - 1)),
            volume=5000000
        ))
    stock_prices["PFE"] = pfe_prices
    
    # JPM - no significant movement
    jpm_prices = []
    base_price = 145.0
    for i in range(-30, 31):
        price_date = date(2023, 8, 1) + timedelta(days=i)
        price = base_price + (i * 0.05)  # Minimal movement
        
        jpm_prices.append(StockPrice(
            ticker="JPM",
            price_date=price_date,
            open_price=Decimal(str(price - 1)),
            close_price=Decimal(str(price)),
            high_price=Decimal(str(price + 2)),
            low_price=Decimal(str(price - 2)),
            volume=3000000
        ))
    stock_prices["JPM"] = jpm_prices
    
    return members, transactions, legislative_actions, committees, stock_prices


def main():
    """Run comprehensive analysis demonstration."""
    print("🏛️  Senate Insight Lab - Comprehensive Analysis")
    print("=" * 55)
    
    # Create dataset
    members, transactions, legislative_actions, committees, stock_prices = create_comprehensive_dataset()
    
    print(f"Dataset Overview:")
    print(f"  📊 Members: {len(members)}")
    print(f"  💰 Transactions: {len(transactions)}")
    print(f"  📜 Legislative Actions: {len(legislative_actions)}")
    print(f"  🏛️  Committee Assignments: {len(committees)}")
    print(f"  📈 Stock Price Days: {sum(len(prices) for prices in stock_prices.values())}")
    
    # Initialize detector
    detector = InsiderTradingDetector()
    
    # Analyze each member
    all_alerts = []
    
    for member in members:
        # Get member's data
        member_transactions = [t for t in transactions if t.member_id == member.member_id]
        member_actions = [a for a in legislative_actions if a.member_id == member.member_id]
        member_committees = [c for c in committees if c.member_id == member.member_id]
        
        if not member_transactions:
            continue
            
        print(f"\n🔍 Analyzing {member.name}...")
        print(f"   Transactions: {len(member_transactions)}")
        print(f"   Legislative Actions: {len(member_actions)}")
        print(f"   Committees: {[c.committee_name for c in member_committees]}")
        
        # Run analysis
        alerts = detector.analyze_member_activity(
            member, member_transactions, member_actions, member_committees, stock_prices
        )
        
        all_alerts.extend(alerts)
        
        # Display results for this member
        if alerts:
            for alert in alerts:
                confidence_emoji = "🚨" if alert.confidence_score >= 0.7 else "⚠️" if alert.confidence_score >= 0.5 else "ℹ️"
                print(f"   {confidence_emoji} Alert (Confidence: {alert.confidence_score:.2f})")
                print(f"      {alert.description}")
        else:
            print(f"   ✅ No suspicious patterns detected")
    
    # Summary report
    print(f"\n📋 Analysis Summary")
    print("=" * 25)
    print(f"Total Alerts Generated: {len(all_alerts)}")
    
    if all_alerts:
        # Categorize by confidence
        high_confidence = [a for a in all_alerts if a.confidence_score >= 0.7]
        medium_confidence = [a for a in all_alerts if 0.5 <= a.confidence_score < 0.7]
        low_confidence = [a for a in all_alerts if a.confidence_score < 0.5]
        
        print(f"  🚨 High Confidence (≥70%): {len(high_confidence)}")
        print(f"  ⚠️  Medium Confidence (50-69%): {len(medium_confidence)}")
        print(f"  ℹ️  Low Confidence (<50%): {len(low_confidence)}")
        
        # Top alerts
        sorted_alerts = sorted(all_alerts, key=lambda x: x.confidence_score, reverse=True)
        print(f"\n🔍 Top Suspicious Activities:")
        for i, alert in enumerate(sorted_alerts[:3], 1):
            print(f"  {i}. {alert.description}")
            print(f"     Confidence: {alert.confidence_score:.1%}")
    
    print(f"\n💡 This demonstrates the system's ability to:")
    print(f"   • Detect timing correlations between trades and legislative actions")
    print(f"   • Identify committee-industry relationships")
    print(f"   • Analyze post-transaction price movements")
    print(f"   • Score and prioritize suspicious activities")


if __name__ == "__main__":
    main()