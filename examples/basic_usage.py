#!/usr/bin/env python3
"""
Basic usage example for Senate Insight Lab.

This example demonstrates how to:
1. Collect Congressional member data
2. Analyze financial disclosures
3. Generate insider trading alerts
"""

import asyncio
from datetime import date, timedelta

from senate_insight.orchestrator import SenateInsightOrchestrator
from senate_insight.utils.logging_config import setup_logging
from senate_insight.utils.database import db_manager


async def main():
    """Run basic analysis example."""
    # Setup logging
    setup_logging()
    
    # Initialize database
    db_manager.create_tables()
    
    # Create orchestrator
    orchestrator = SenateInsightOrchestrator()
    
    print("🚀 Starting Senate Insight Lab Analysis")
    print("=" * 50)
    
    # Run analysis for Senate members only (smaller dataset)
    results = await orchestrator.run_full_pipeline(chamber="senate")
    
    # Print results
    print(f"\n📊 Analysis Results:")
    print(f"Members processed: {results['members_processed']}")
    print(f"Alerts generated: {results['alerts_generated']}")
    print(f"Duration: {results['duration']}")
    
    if results['errors']:
        print(f"\n❌ Errors ({len(results['errors'])}):")
        for error in results['errors'][:5]:  # Show first 5 errors
            print(f"  • {error}")


if __name__ == "__main__":
    asyncio.run(main())