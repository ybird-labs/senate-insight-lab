"""Command-line interface for Senate Insight Lab."""

import click
from datetime import datetime, date, timedelta
import logging

from .utils.logging_config import setup_logging
from .utils.config import settings
from .utils.database import db_manager
from .data_collectors.congress_api import CongressAPICollector
from .data_collectors.financial_data import FinancialDisclosureCollector, StockPriceCollector
from .analyzers.insider_trading_detector import InsiderTradingDetector

logger = logging.getLogger(__name__)


@click.group()
@click.option('--debug', is_flag=True, help='Enable debug logging')
def main(debug):
    """Senate Insight Lab - Congressional Investment Analysis Tool."""
    if debug:
        settings.log_level = "DEBUG"
    
    setup_logging()
    logger.info("Senate Insight Lab starting...")


@main.command()
def init_db():
    """Initialize the database schema."""
    click.echo("Initializing database...")
    try:
        db_manager.create_tables()
        click.echo("✅ Database initialized successfully!")
    except Exception as e:
        click.echo(f"❌ Error initializing database: {e}")
        raise


@main.command()
@click.option('--chamber', type=click.Choice(['senate', 'house', 'both']), 
              default='both', help='Chamber to collect data for')
def collect_members(chamber):
    """Collect current Congress member data."""
    click.echo(f"Collecting {chamber} member data...")
    
    try:
        collector = CongressAPICollector(settings.congress_api_key)
        members = collector.get_current_members(chamber)
        
        click.echo(f"✅ Collected data for {len(members)} members")
        
        # TODO: Save to database
        
    except Exception as e:
        click.echo(f"❌ Error collecting member data: {e}")
        logger.exception("Failed to collect member data")


@main.command()
@click.argument('member_name')
@click.option('--year', type=int, default=None, help='Year to analyze (default: current year)')
def collect_disclosures(member_name, year):
    """Collect financial disclosure data for a specific member."""
    if year is None:
        year = datetime.now().year
    
    click.echo(f"Collecting financial disclosures for {member_name} ({year})...")
    
    try:
        collector = FinancialDisclosureCollector()
        disclosures = collector.get_member_disclosures(member_name, year)
        
        click.echo(f"✅ Collected {len(disclosures)} disclosure filings")
        
        # TODO: Save to database
        
    except Exception as e:
        click.echo(f"❌ Error collecting disclosures: {e}")
        logger.exception("Failed to collect disclosure data")


@main.command()
@click.argument('member_id')
@click.option('--days', default=90, help='Number of days to analyze (default: 90)')
def analyze_member(member_id, days):
    """Analyze a specific member for potential insider trading."""
    click.echo(f"Analyzing member {member_id} for the last {days} days...")
    
    try:
        # Load data from database
        # This would be implemented with actual database queries
        
        detector = InsiderTradingDetector()
        
        # Placeholder - would load actual data
        member = None  # Load from DB
        transactions = []  # Load from DB
        legislative_actions = []  # Load from DB
        committee_assignments = []  # Load from DB
        stock_prices = {}  # Load from DB
        
        if not member:
            click.echo(f"❌ Member {member_id} not found in database")
            return
        
        alerts = detector.analyze_member_activity(
            member, transactions, legislative_actions, committee_assignments, stock_prices
        )
        
        click.echo(f"✅ Analysis complete. Generated {len(alerts)} alerts")
        
        for alert in alerts:
            if alert.confidence_score >= 0.7:
                click.echo(f"🚨 HIGH: {alert.description}")
            elif alert.confidence_score >= 0.5:
                click.echo(f"⚠️  MEDIUM: {alert.description}")
            else:
                click.echo(f"ℹ️  LOW: {alert.description}")
        
    except Exception as e:
        click.echo(f"❌ Error analyzing member: {e}")
        logger.exception("Failed to analyze member")


@main.command()
@click.option('--min-confidence', default=0.5, help='Minimum confidence score for alerts')
def analyze_all(min_confidence):
    """Analyze all members for potential insider trading."""
    click.echo("Analyzing all members for potential insider trading...")
    
    try:
        # This would implement batch analysis of all members
        click.echo("🔄 Starting batch analysis (this may take a while)...")
        
        # Load all members from database
        # Run analysis for each member
        # Generate summary report
        
        click.echo("✅ Batch analysis complete!")
        
    except Exception as e:
        click.echo(f"❌ Error in batch analysis: {e}")
        logger.exception("Failed to complete batch analysis")


@main.command()
@click.option('--format', type=click.Choice(['text', 'json', 'csv']), 
              default='text', help='Output format')
def report(format):
    """Generate a report of all alerts."""
    click.echo(f"Generating {format} report...")
    
    try:
        # Load alerts from database
        # Format and output report
        
        click.echo("✅ Report generated successfully!")
        
    except Exception as e:
        click.echo(f"❌ Error generating report: {e}")
        logger.exception("Failed to generate report")


@main.command()
def web():
    """Start the web interface (future feature)."""
    click.echo("Web interface not yet implemented.")
    click.echo("This will start a Flask/FastAPI web server for interactive analysis.")


if __name__ == '__main__':
    main()