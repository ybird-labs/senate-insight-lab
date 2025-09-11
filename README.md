# Senate Insight Lab

A comprehensive analysis tool for investigating Congressional members' investments and identifying potential insider trading patterns based on legislative activities and committee assignments.

## 🎯 Purpose

This project analyzes the relationship between Congressional members' stock trades and their legislative work to identify potential insider trading opportunities. It combines:

- Congressional voting records and committee assignments
- Financial disclosure data and stock transactions  
- Stock market performance data
- Advanced correlation analysis algorithms

## 🏗️ Architecture

```
senate_insight/
├── data_collectors/     # Data gathering modules
│   ├── congress_api.py     # Congressional data via APIs
│   └── financial_data.py   # Financial disclosures & stock prices
├── analyzers/          # Analysis engines
│   └── insider_trading_detector.py  # Main detection algorithms
├── models/            # Data models and schemas
│   ├── congress_member.py     # Congressional member models
│   └── financial_disclosure.py # Financial transaction models
└── utils/             # Utilities and configuration
    ├── config.py         # Configuration management
    ├── database.py       # Database ORM setup
    └── logging_config.py # Logging configuration
```

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/ybird-labs/senate-insight-lab.git
cd senate-insight-lab

# Install dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

### Configuration

```bash
# Copy example configuration
cp config/example.env .env

# Edit .env with your API keys
# You'll need:
# - Congress API key (from congress.gov)
# - Alpha Vantage API key (for stock data)
```

### Basic Usage

```bash
# Initialize database
senate-insight init-db

# Collect Congressional member data
senate-insight collect-members --chamber both

# Analyze a specific member
senate-insight analyze-member S001234

# Generate analysis report
senate-insight report --format json
```

## 📊 Analysis Features

### Detection Algorithms

1. **Timing Correlation Analysis**
   - Identifies trades made shortly before relevant legislative actions
   - Configurable time windows (default: 30 days)
   - Weights based on proximity to legislative events

2. **Committee Correlation Analysis**
   - Maps committee assignments to relevant industries
   - Scores trades based on member's oversight responsibilities
   - Identifies potential conflicts of interest

3. **Price Movement Analysis**
   - Analyzes stock performance following trades
   - Calculates abnormal returns
   - Identifies suspiciously profitable trades

4. **Volume Anomaly Detection**
   - Detects unusual trading volume around transaction dates
   - Uses statistical analysis to identify outliers
   - Correlates with potential information leaks

### Confidence Scoring

Each potential insider trading alert receives a confidence score (0-1) based on:
- **Timing** (30%): How close the trade was to relevant legislative action
- **Committee Correlation** (25%): Relevance of member's committees to the stock
- **Price Movement** (35%): Favorable price movement after the trade
- **Volume Anomaly** (10%): Unusual trading volume patterns

## 🔧 Configuration

Key configuration options in `.env`:

```bash
# Analysis thresholds
TIMING_WINDOW_DAYS=30              # Days to check before/after trades
SIGNIFICANT_PRICE_CHANGE=0.05      # 5% price movement threshold
MIN_CONFIDENCE_THRESHOLD=0.3       # Minimum alert confidence

# Data collection
MAX_CONCURRENT_REQUESTS=5          # API rate limiting
REQUEST_DELAY_SECONDS=1.0         # Delay between requests
```

## 📚 Examples

### Programmatic Usage

```python
from senate_insight.orchestrator import SenateInsightOrchestrator

# Initialize orchestrator
orchestrator = SenateInsightOrchestrator()

# Run analysis
results = await orchestrator.run_full_pipeline(chamber="senate")

# Generate report
report = orchestrator.generate_summary_report(results['alerts'])
print(report)
```

### CLI Usage

```bash
# Analyze all members with high confidence threshold
senate-insight analyze-all --min-confidence 0.7

# Collect disclosures for specific member
senate-insight collect-disclosures "Nancy Pelosi" --year 2023

# Generate CSV report
senate-insight report --format csv > insider_trading_report.csv
```

See `examples/` directory for more detailed usage examples.

## 🔍 Data Sources

### Congressional Data
- **Congress.gov API**: Voting records, bill sponsorships, committee assignments
- **House Clerk**: Financial disclosure filings
- **Senate Ethics**: Periodic transaction reports

### Financial Data
- **Financial Disclosure Reports**: Stock transactions, asset holdings
- **Yahoo Finance API**: Stock price and volume data
- **Alpha Vantage**: Advanced market data and indicators

### Data Processing
- **PDF Parsing**: Automated extraction from disclosure documents
- **OCR Integration**: Processing scanned financial forms
- **NLP Analysis**: Industry classification of legislation

## ⚖️ Legal and Ethical Considerations

**Important Disclaimers:**

1. **Educational Purpose**: This tool is for research and transparency purposes only
2. **No Investment Advice**: Results should not be used for investment decisions
3. **Data Accuracy**: Analysis depends on publicly available data which may be incomplete
4. **Legal Compliance**: Users must comply with all applicable laws and regulations
5. **Privacy Respect**: Only processes publicly disclosed information

**Ethical Guidelines:**
- Promotes government transparency and accountability
- Identifies potential conflicts of interest in public service
- Supports informed democratic participation
- Respects privacy of non-public information

## 🛡️ Security and Privacy

- No storage of private or confidential information
- All data sources are publicly available
- API keys and credentials stored securely
- Database encryption for sensitive analysis results
- Audit logging for all data access

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=senate_insight

# Run specific test categories
pytest tests/test_analyzers.py
```

## 📈 Performance Considerations

- **Batch Processing**: Efficient handling of large datasets
- **Rate Limiting**: Respectful API usage with configurable delays
- **Caching**: Reduces redundant API calls
- **Async Processing**: Concurrent data collection where possible
- **Database Optimization**: Indexed queries for fast analysis

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please read our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Congress.gov for providing public legislative data
- Financial disclosure databases for transparency
- Open source libraries that make this analysis possible
- Researchers studying government accountability and transparency

## 📞 Support

- **Issues**: Report bugs and feature requests on GitHub
- **Documentation**: See `docs/` directory for detailed guides  
- **Community**: Join discussions in GitHub Discussions

---

**Disclaimer**: This tool is for educational and research purposes. Always verify information independently and consult with legal professionals for compliance guidance.