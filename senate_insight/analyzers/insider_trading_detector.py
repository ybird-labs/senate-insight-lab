"""Insider trading detection and analysis engine."""

from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional, Tuple
import logging
from dataclasses import dataclass
from statistics import mean, stdev

from ..models.congress_member import CongressMember, LegislativeAction, CommitteeAssignment
from ..models.financial_disclosure import StockTransaction, StockPrice, InsiderTradingAlert

logger = logging.getLogger(__name__)


@dataclass
class AnalysisMetrics:
    """Metrics for insider trading analysis."""
    timing_score: float = 0.0
    committee_correlation_score: float = 0.0
    price_movement_score: float = 0.0
    volume_anomaly_score: float = 0.0
    overall_suspicion_score: float = 0.0


class InsiderTradingDetector:
    """Detects potential insider trading patterns."""
    
    def __init__(self):
        """Initialize the detector with configurable parameters."""
        self.timing_window_days = 30  # Days before/after legislative action
        self.significant_price_change = 0.05  # 5% price change threshold
        self.min_confidence_threshold = 0.3
        
    def analyze_member_activity(
        self,
        member: CongressMember,
        transactions: List[StockTransaction],
        legislative_actions: List[LegislativeAction],
        committee_assignments: List[CommitteeAssignment],
        stock_prices: Dict[str, List[StockPrice]]
    ) -> List[InsiderTradingAlert]:
        """
        Analyze a member's trading activity for potential insider trading.
        
        Args:
            member: Congress member information
            transactions: Member's stock transactions
            legislative_actions: Member's legislative activities
            committee_assignments: Member's committee assignments
            stock_prices: Stock price data for relevant tickers
            
        Returns:
            List of insider trading alerts
        """
        alerts = []
        
        for transaction in transactions:
            # Get price data for this stock
            prices = stock_prices.get(transaction.ticker, [])
            if not prices:
                continue
            
            # Analyze this specific transaction
            metrics = self._analyze_transaction(
                transaction, member, legislative_actions, committee_assignments, prices
            )
            
            # Generate alert if suspicion score exceeds threshold
            if metrics.overall_suspicion_score >= self.min_confidence_threshold:
                alert = self._create_alert(transaction, member, metrics)
                alerts.append(alert)
        
        return alerts
    
    def _analyze_transaction(
        self,
        transaction: StockTransaction,
        member: CongressMember,
        legislative_actions: List[LegislativeAction],
        committee_assignments: List[CommitteeAssignment],
        stock_prices: List[StockPrice]
    ) -> AnalysisMetrics:
        """Analyze a single transaction for insider trading indicators."""
        metrics = AnalysisMetrics()
        
        # 1. Timing Analysis - Check if transaction preceded relevant legislative action
        metrics.timing_score = self._calculate_timing_score(
            transaction, legislative_actions, stock_prices
        )
        
        # 2. Committee Correlation - Check if member's committees relate to stock's industry
        metrics.committee_correlation_score = self._calculate_committee_correlation(
            transaction, committee_assignments
        )
        
        # 3. Price Movement Analysis - Check post-transaction price performance
        metrics.price_movement_score = self._calculate_price_movement_score(
            transaction, stock_prices
        )
        
        # 4. Volume Anomaly - Check for unusual trading volume
        metrics.volume_anomaly_score = self._calculate_volume_anomaly_score(
            transaction, stock_prices
        )
        
        # Calculate overall suspicion score (weighted average)
        metrics.overall_suspicion_score = (
            metrics.timing_score * 0.3 +
            metrics.committee_correlation_score * 0.25 +
            metrics.price_movement_score * 0.35 +
            metrics.volume_anomaly_score * 0.1
        )
        
        return metrics
    
    def _calculate_timing_score(
        self,
        transaction: StockTransaction,
        legislative_actions: List[LegislativeAction],
        stock_prices: List[StockPrice]
    ) -> float:
        """Calculate suspicion score based on timing relative to legislative actions."""
        score = 0.0
        
        # Find legislative actions within timing window
        window_start = transaction.transaction_date - timedelta(days=self.timing_window_days)
        window_end = transaction.transaction_date + timedelta(days=self.timing_window_days)
        
        relevant_actions = [
            action for action in legislative_actions
            if window_start <= action.action_date.date() <= window_end
            and self._is_action_relevant_to_stock(action, transaction.ticker, transaction.company_name)
        ]
        
        if relevant_actions:
            # Higher score if transaction was before legislative action
            for action in relevant_actions:
                days_difference = (action.action_date.date() - transaction.transaction_date).days
                
                if 0 <= days_difference <= 14:  # Transaction 0-14 days before action
                    score += 0.8
                elif -7 <= days_difference < 0:  # Transaction up to 7 days after action
                    score += 0.4
                elif 15 <= days_difference <= 30:  # Transaction 15-30 days before
                    score += 0.5
        
        return min(score, 1.0)
    
    def _calculate_committee_correlation(
        self,
        transaction: StockTransaction,
        committee_assignments: List[CommitteeAssignment]
    ) -> float:
        """Calculate score based on member's committee assignments relevance to stock."""
        # Map committees to industries they oversee
        committee_industry_map = {
            "banking": ["financial", "bank", "insurance", "credit"],
            "energy": ["oil", "gas", "energy", "utility", "solar", "wind"],
            "technology": ["tech", "software", "internet", "telecommunications"],
            "healthcare": ["pharma", "biotech", "medical", "hospital"],
            "defense": ["defense", "aerospace", "military"],
            "agriculture": ["agriculture", "food", "farming"],
            "transportation": ["airline", "automotive", "railroad", "shipping"],
        }
        
        # Get industries relevant to this stock
        company_lower = transaction.company_name.lower()
        stock_industries = []
        
        for industry, keywords in committee_industry_map.items():
            if any(keyword in company_lower for keyword in keywords):
                stock_industries.append(industry)
        
        if not stock_industries:
            return 0.0
        
        # Check if member serves on relevant committees
        member_committees = [assignment.committee_name.lower() for assignment in committee_assignments]
        
        for industry in stock_industries:
            if any(industry in committee for committee in member_committees):
                return 0.7  # High correlation
        
        return 0.0
    
    def _calculate_price_movement_score(
        self,
        transaction: StockTransaction,
        stock_prices: List[StockPrice]
    ) -> float:
        """Calculate score based on favorable price movement after transaction."""
        # Get price data around transaction date
        transaction_price = self._get_price_on_date(stock_prices, transaction.transaction_date)
        if not transaction_price:
            return 0.0
        
        # Check price movement in following weeks
        future_prices = [
            price for price in stock_prices
            if price.price_date > transaction.transaction_date
            and price.price_date <= transaction.transaction_date + timedelta(days=30)
        ]
        
        if not future_prices:
            return 0.0
        
        # Calculate maximum favorable movement
        if transaction.transaction_type.lower() in ["buy", "purchase"]:
            # For buys, look for price increases
            max_price = max(price.close_price for price in future_prices)
            price_change = (max_price - transaction_price.close_price) / transaction_price.close_price
        else:  # Sell
            # For sells, look for price decreases
            min_price = min(price.close_price for price in future_prices)
            price_change = (transaction_price.close_price - min_price) / transaction_price.close_price
        
        # Score based on magnitude of favorable movement
        if price_change >= 0.20:  # 20% or more
            return 1.0
        elif price_change >= 0.10:  # 10-20%
            return 0.7
        elif price_change >= 0.05:  # 5-10%
            return 0.4
        else:
            return 0.0
    
    def _calculate_volume_anomaly_score(
        self,
        transaction: StockTransaction,
        stock_prices: List[StockPrice]
    ) -> float:
        """Calculate score based on unusual trading volume around transaction date."""
        # Get volume data around transaction
        baseline_prices = [
            price for price in stock_prices
            if price.price_date < transaction.transaction_date - timedelta(days=7)
            and price.price_date >= transaction.transaction_date - timedelta(days=37)
        ]
        
        transaction_day_price = self._get_price_on_date(stock_prices, transaction.transaction_date)
        
        if not baseline_prices or not transaction_day_price:
            return 0.0
        
        # Calculate average baseline volume
        baseline_volumes = [price.volume for price in baseline_prices]
        avg_volume = mean(baseline_volumes)
        
        if len(baseline_volumes) > 1:
            volume_std = stdev(baseline_volumes)
        else:
            volume_std = avg_volume * 0.2  # Assume 20% standard deviation
        
        # Check if transaction day volume was unusually high
        volume_z_score = (transaction_day_price.volume - avg_volume) / max(volume_std, 1)
        
        if volume_z_score >= 3:  # 3+ standard deviations above normal
            return 0.8
        elif volume_z_score >= 2:  # 2+ standard deviations
            return 0.5
        elif volume_z_score >= 1:  # 1+ standard deviations
            return 0.2
        else:
            return 0.0
    
    def _get_price_on_date(self, stock_prices: List[StockPrice], target_date: date) -> Optional[StockPrice]:
        """Get stock price data for a specific date."""
        for price in stock_prices:
            if price.price_date == target_date:
                return price
        return None
    
    def _is_action_relevant_to_stock(self, action: LegislativeAction, ticker: str, company_name: str) -> bool:
        """Determine if a legislative action is relevant to a specific stock."""
        # Simple keyword matching - could be enhanced with NLP
        action_text = f"{action.bill_title} {' '.join(action.industries_affected)}".lower()
        company_lower = company_name.lower()
        ticker_lower = ticker.lower()
        
        return ticker_lower in action_text or any(
            word in action_text for word in company_lower.split() if len(word) > 3
        )
    
    def _create_alert(
        self,
        transaction: StockTransaction,
        member: CongressMember,
        metrics: AnalysisMetrics
    ) -> InsiderTradingAlert:
        """Create an insider trading alert from analysis results."""
        alert_type = "timing_correlation"
        if metrics.committee_correlation_score > 0.5:
            alert_type = "committee_correlation"
        
        description = (
            f"Potential insider trading detected: {member.name} "
            f"{transaction.transaction_type.lower()}ed {transaction.ticker} "
            f"on {transaction.transaction_date} with suspicion score {metrics.overall_suspicion_score:.2f}"
        )
        
        return InsiderTradingAlert(
            alert_id=f"alert_{transaction.transaction_id}_{int(datetime.now().timestamp())}",
            member_id=member.member_id,
            transaction_id=transaction.transaction_id,
            alert_type=alert_type,
            confidence_score=metrics.overall_suspicion_score,
            description=description,
            price_change_percent=None,  # Would be calculated from price data
            price_movement_days=30,
        )