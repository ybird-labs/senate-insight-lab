"""Data collector for financial disclosure data."""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
from datetime import datetime, date
import re
import logging
from decimal import Decimal

from ..models.financial_disclosure import FinancialDisclosure, StockTransaction, StockPrice

logger = logging.getLogger(__name__)


class FinancialDisclosureCollector:
    """Collects financial disclosure data from various sources."""
    
    def __init__(self):
        """Initialize the collector."""
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
    
    def get_member_disclosures(self, member_name: str, year: int = None) -> List[FinancialDisclosure]:
        """
        Get financial disclosures for a Congress member.
        
        Args:
            member_name: Name of the Congress member
            year: Year to search (defaults to current year)
            
        Returns:
            List of FinancialDisclosure objects
        """
        disclosures = []
        
        # This would integrate with actual disclosure databases
        # For now, this is a placeholder structure
        try:
            # Example: Senate financial disclosures are at efdsearch.senate.gov
            # House disclosures are at clerk.house.gov
            
            # Placeholder implementation - in reality, this would scrape or use APIs
            logger.info(f"Fetching disclosures for {member_name}, year {year}")
            
            # This would be implemented with actual data sources
            
        except Exception as e:
            logger.error(f"Error fetching disclosures for {member_name}: {e}")
        
        return disclosures
    
    def parse_disclosure_document(self, document_url: str) -> Optional[FinancialDisclosure]:
        """Parse a financial disclosure document."""
        try:
            response = self.session.get(document_url)
            response.raise_for_status()
            
            # Parse PDF or HTML content
            # This is a simplified implementation
            
            return None  # Placeholder
            
        except Exception as e:
            logger.error(f"Error parsing disclosure document {document_url}: {e}")
            return None
    
    def _extract_transactions_from_text(self, text: str, member_id: str) -> List[StockTransaction]:
        """Extract stock transactions from disclosure text."""
        transactions = []
        
        # Regex patterns for common disclosure formats
        patterns = [
            # Pattern for "TICKER - Company Name - Transaction Type - Amount Range - Date"
            r"([A-Z]{1,5})\s*-\s*(.+?)\s*-\s*(Buy|Sell|Sale)\s*-\s*(\$[\d,]+-\$[\d,]+)\s*-\s*(\d{1,2}/\d{1,2}/\d{2,4})",
            # Add more patterns as needed
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                try:
                    transaction = StockTransaction(
                        transaction_id=f"txn_{hash(match.group(0))}",
                        member_id=member_id,
                        ticker=match.group(1).upper(),
                        company_name=match.group(2).strip(),
                        transaction_type=match.group(3).title(),
                        transaction_date=self._parse_date(match.group(5)),
                        disclosure_date=date.today(),  # Would be extracted from document
                        amount_range=match.group(4),
                        owner="Self",  # Would be determined from context
                    )
                    
                    # Parse amount range
                    min_amt, max_amt = self._parse_amount_range(match.group(4))
                    transaction.min_amount = min_amt
                    transaction.max_amount = max_amt
                    
                    transactions.append(transaction)
                    
                except Exception as e:
                    logger.error(f"Error parsing transaction: {e}")
        
        return transactions
    
    def _parse_amount_range(self, amount_str: str) -> tuple[Optional[Decimal], Optional[Decimal]]:
        """Parse amount range string like '$1,001-$15,000'."""
        try:
            # Remove $ signs and commas
            clean_str = amount_str.replace("$", "").replace(",", "")
            
            if "-" in clean_str:
                parts = clean_str.split("-")
                min_amount = Decimal(parts[0])
                max_amount = Decimal(parts[1])
                return min_amount, max_amount
            else:
                # Single amount
                amount = Decimal(clean_str)
                return amount, amount
                
        except Exception as e:
            logger.error(f"Error parsing amount range {amount_str}: {e}")
            return None, None
    
    def _parse_date(self, date_str: str) -> Optional[date]:
        """Parse various date formats."""
        formats = [
            "%m/%d/%Y",
            "%m/%d/%y",
            "%Y-%m-%d",
            "%d/%m/%Y",
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        
        logger.warning(f"Could not parse date: {date_str}")
        return None


class StockPriceCollector:
    """Collects stock price data from financial APIs."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize with API key for services like Alpha Vantage."""
        self.api_key = api_key
        self.session = requests.Session()
    
    def get_stock_prices(self, ticker: str, start_date: date, end_date: date) -> List[StockPrice]:
        """Get stock price data for a ticker within date range."""
        prices = []
        
        try:
            # This would integrate with yfinance, Alpha Vantage, or other APIs
            import yfinance as yf
            
            stock = yf.Ticker(ticker)
            hist = stock.history(start=start_date, end=end_date)
            
            for date_idx, row in hist.iterrows():
                price = StockPrice(
                    ticker=ticker.upper(),
                    price_date=date_idx.date(),
                    open_price=Decimal(str(row['Open'])),
                    close_price=Decimal(str(row['Close'])),
                    high_price=Decimal(str(row['High'])),
                    low_price=Decimal(str(row['Low'])),
                    volume=int(row['Volume']),
                )
                prices.append(price)
                
        except Exception as e:
            logger.error(f"Error fetching stock prices for {ticker}: {e}")
        
        return prices