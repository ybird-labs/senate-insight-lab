# Senate Insight Lab - Usage Guide

## Quick Start

### 1. Installation and Setup

```bash
# Clone the repository
git clone https://github.com/ybird-labs/senate-insight-lab.git
cd senate-insight-lab

# Install dependencies
pip install -r requirements.txt

# Configure environment (optional)
cp example.env .env
# Edit .env with your API keys
```

### 2. Basic Analysis

Run the comprehensive example to see the system in action:

```bash
python examples/comprehensive_example.py
```

This will demonstrate:
- Analysis of multiple Congress members
- Detection of timing correlations
- Committee-industry relationship scoring
- Price movement analysis
- Confidence-based alert prioritization

### 3. Understanding the Output

The system generates alerts with confidence scores:
- **🚨 High Confidence (≥70%)**: Strong indicators of potential insider trading
- **⚠️ Medium Confidence (50-69%)**: Suspicious patterns worth investigating
- **ℹ️ Low Confidence (<50%)**: Weak indicators, may be coincidental

## Analysis Components

### 1. Timing Correlation Analysis
Identifies trades made shortly before relevant legislative actions:
- Checks configurable time windows (default: 30 days)
- Higher scores for trades made 0-14 days before legislative action
- Considers relevance of legislation to the traded stock

### 2. Committee Correlation Analysis
Evaluates whether trades align with a member's oversight responsibilities:
- Maps committee assignments to relevant industries
- Scores trades based on member's committee oversight
- Example: Technology committee member trading tech stocks

### 3. Price Movement Analysis
Analyzes stock performance following trades:
- Examines price changes up to 30 days after transaction
- Higher scores for significant favorable movements
- Considers both buy and sell transactions

### 4. Volume Anomaly Detection
Detects unusual trading volume around transaction dates:
- Compares transaction day volume to historical baseline
- Uses statistical analysis (z-scores) to identify outliers
- May indicate potential information leaks

## Confidence Scoring Formula

Each alert receives a weighted confidence score:
```
Confidence = (Timing × 30%) + (Committee × 25%) + (Price Movement × 35%) + (Volume × 10%)
```

This formula can be adjusted in the `InsiderTradingDetector` class.

## Data Sources Integration

### Congressional Data
- **Congress.gov API**: Voting records and bill information
- **House Clerk**: Financial disclosure filings
- **Senate Ethics**: Periodic transaction reports

### Financial Data
- **Yahoo Finance**: Stock price and volume data
- **Alpha Vantage**: Advanced market indicators (with API key)

### Example API Configuration
```python
from senate_insight.data_collectors.congress_api import CongressAPICollector
from senate_insight.data_collectors.financial_data import StockPriceCollector

# Initialize collectors
congress_collector = CongressAPICollector(api_key="your_congress_api_key")
stock_collector = StockPriceCollector(api_key="your_alpha_vantage_key")

# Collect data
members = congress_collector.get_current_members("senate")
prices = stock_collector.get_stock_prices("AAPL", start_date, end_date)
```

## Customization

### Adjusting Detection Parameters

```python
from senate_insight.analyzers.insider_trading_detector import InsiderTradingDetector

detector = InsiderTradingDetector()
detector.timing_window_days = 45  # Extend time window
detector.significant_price_change = 0.03  # Lower threshold (3%)
detector.min_confidence_threshold = 0.2  # Include more alerts
```

### Custom Industry Mapping

You can extend the committee-industry mapping in `insider_trading_detector.py`:

```python
committee_industry_map = {
    "banking": ["financial", "bank", "insurance", "credit"],
    "energy": ["oil", "gas", "energy", "utility", "solar", "wind"],
    "technology": ["tech", "software", "internet", "telecommunications"],
    # Add custom mappings
    "agriculture": ["farming", "food", "agriculture", "livestock"],
}
```

## Best Practices

### 1. Data Quality
- Ensure complete financial disclosure data
- Verify stock price data accuracy
- Cross-reference legislative action details

### 2. Alert Investigation
- Manually review high-confidence alerts
- Consider broader context and market conditions
- Look for patterns across multiple transactions

### 3. Legal Compliance
- Only analyze publicly available information
- Respect privacy and legal boundaries
- Use results for transparency, not investment decisions

### 4. Performance Optimization
- Use batch processing for large datasets
- Implement caching for repeated API calls
- Configure rate limiting for API requests

## Troubleshooting

### Common Issues

**Import Errors**: Ensure all dependencies are installed
```bash
pip install -r requirements.txt
```

**API Rate Limits**: Adjust request delays in configuration
```python
settings.request_delay_seconds = 2.0
```

**Data Missing**: Check API key configuration and data source availability

**Low Alert Confidence**: Verify data completeness and adjust thresholds

### Performance Tips

1. **Batch Processing**: Process multiple members together
2. **Data Caching**: Store frequently accessed data locally
3. **Selective Analysis**: Focus on specific time periods or members
4. **Parallel Processing**: Use async/await for data collection

## Examples Directory

- `basic_usage.py`: Simple workflow demonstration
- `analysis_example.py`: Single-member detailed analysis
- `comprehensive_example.py`: Multi-member batch analysis with reporting

## Next Steps

1. **Extend Data Sources**: Add more financial disclosure databases
2. **Enhanced NLP**: Improve legislative text analysis
3. **Machine Learning**: Implement predictive models
4. **Web Interface**: Create interactive dashboard
5. **Real-time Monitoring**: Set up automated alert systems

## Support

For questions or issues:
1. Check existing GitHub Issues
2. Review the comprehensive README.md
3. Run the example files to verify setup
4. Open a new issue with detailed error information

Remember: This tool is for educational and transparency purposes only. Always comply with applicable laws and regulations.