"""Main orchestrator for data collection and analysis pipeline."""

import asyncio
from typing import List, Dict, Any
import logging
from datetime import datetime, date, timedelta

from .data_collectors.congress_api import CongressAPICollector
from .data_collectors.financial_data import FinancialDisclosureCollector, StockPriceCollector
from .analyzers.insider_trading_detector import InsiderTradingDetector
from .utils.config import settings
from .utils.database import db_manager
from .models.congress_member import CongressMember
from .models.financial_disclosure import InsiderTradingAlert

logger = logging.getLogger(__name__)


class SenateInsightOrchestrator:
    """Orchestrates the data collection and analysis pipeline."""
    
    def __init__(self):
        """Initialize the orchestrator with data collectors and analyzers."""
        self.congress_collector = CongressAPICollector(settings.congress_api_key)
        self.disclosure_collector = FinancialDisclosureCollector()
        self.stock_collector = StockPriceCollector(settings.alpha_vantage_api_key)
        self.detector = InsiderTradingDetector()
        
    async def run_full_pipeline(self, chamber: str = "both") -> Dict[str, Any]:
        """
        Run the complete data collection and analysis pipeline.
        
        Args:
            chamber: Which chamber to analyze ("senate", "house", or "both")
            
        Returns:
            Dictionary with pipeline results and statistics
        """
        results = {
            "start_time": datetime.now(),
            "members_processed": 0,
            "alerts_generated": 0,
            "errors": [],
        }
        
        try:
            logger.info(f"Starting full pipeline for {chamber}")
            
            # Step 1: Collect member data
            logger.info("Collecting Congress member data...")
            members = self.congress_collector.get_current_members(chamber)
            results["members_collected"] = len(members)
            
            # Step 2: Process each member
            all_alerts = []
            
            for member in members:
                try:
                    member_alerts = await self._process_member(member)
                    all_alerts.extend(member_alerts)
                    results["members_processed"] += 1
                    
                    logger.info(f"Processed {member.name}: {len(member_alerts)} alerts")
                    
                except Exception as e:
                    error_msg = f"Error processing {member.name}: {str(e)}"
                    logger.error(error_msg)
                    results["errors"].append(error_msg)
            
            results["alerts_generated"] = len(all_alerts)
            results["end_time"] = datetime.now()
            results["duration"] = results["end_time"] - results["start_time"]
            
            # Step 3: Save results to database
            await self._save_results(all_alerts)
            
            logger.info(f"Pipeline complete. Processed {results['members_processed']} members, "
                       f"generated {results['alerts_generated']} alerts")
            
        except Exception as e:
            logger.exception("Pipeline failed")
            results["errors"].append(f"Pipeline failure: {str(e)}")
        
        return results
    
    async def _process_member(self, member: CongressMember) -> List[InsiderTradingAlert]:
        """Process a single member for potential insider trading."""
        alerts = []
        
        try:
            # Collect financial disclosures
            disclosures = self.disclosure_collector.get_member_disclosures(member.name)
            
            # Extract all transactions from disclosures
            transactions = []
            for disclosure in disclosures:
                transactions.extend(disclosure.transactions)
            
            if not transactions:
                logger.info(f"No transactions found for {member.name}")
                return alerts
            
            # Collect legislative actions
            legislative_actions = self.congress_collector.get_member_votes(
                member.member_id,
                start_date=date.today() - timedelta(days=365)
            )
            
            # Collect committee assignments
            committee_assignments = self.congress_collector.get_member_committees(member.member_id)
            
            # Collect stock price data for relevant tickers
            tickers = list(set(t.ticker for t in transactions))
            stock_prices = {}
            
            for ticker in tickers:
                try:
                    prices = self.stock_collector.get_stock_prices(
                        ticker,
                        start_date=date.today() - timedelta(days=365),
                        end_date=date.today()
                    )
                    stock_prices[ticker] = prices
                except Exception as e:
                    logger.warning(f"Could not get prices for {ticker}: {e}")
            
            # Run analysis
            alerts = self.detector.analyze_member_activity(
                member, transactions, legislative_actions, committee_assignments, stock_prices
            )
            
        except Exception as e:
            logger.error(f"Error processing member {member.name}: {e}")
        
        return alerts
    
    async def _save_results(self, alerts: List[InsiderTradingAlert]):
        """Save analysis results to database."""
        try:
            with db_manager.get_session() as session:
                # This would implement actual database saving
                # For now, just log the results
                logger.info(f"Would save {len(alerts)} alerts to database")
                
        except Exception as e:
            logger.error(f"Error saving results: {e}")
    
    def generate_summary_report(self, alerts: List[InsiderTradingAlert]) -> str:
        """Generate a summary report of the analysis results."""
        if not alerts:
            return "No potential insider trading alerts generated."
        
        # Count alerts by confidence level
        high_confidence = [a for a in alerts if a.confidence_score >= 0.7]
        medium_confidence = [a for a in alerts if 0.5 <= a.confidence_score < 0.7]
        low_confidence = [a for a in alerts if a.confidence_score < 0.5]
        
        # Count by member
        member_counts = {}
        for alert in alerts:
            member_counts[alert.member_id] = member_counts.get(alert.member_id, 0) + 1
        
        # Most flagged members
        top_members = sorted(member_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        report = f"""
Senate Insight Lab Analysis Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SUMMARY
=======
Total Alerts: {len(alerts)}
High Confidence (≥70%): {len(high_confidence)}
Medium Confidence (50-69%): {len(medium_confidence)}
Low Confidence (<50%): {len(low_confidence)}

TOP FLAGGED MEMBERS
==================
"""
        
        for member_id, count in top_members:
            report += f"{member_id}: {count} alerts\n"
        
        if high_confidence:
            report += "\nHIGH CONFIDENCE ALERTS\n" + "=" * 22 + "\n"
            for alert in high_confidence[:10]:  # Top 10
                report += f"• {alert.description}\n"
        
        return report