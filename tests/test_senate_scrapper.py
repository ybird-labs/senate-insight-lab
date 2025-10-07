"""Tests for senate_scrapper module."""
import random
from unittest.mock import Mock, patch
import requests
from scrappers.senate_scrapper import Config, SenateScraper


class TestConfig:
    """Tests for the Config class."""

    def test_base_url_is_set(self):
        """Test that BASE_URL is properly configured."""
        assert Config.BASE_URL == "https://efdsearch.senate.gov"

    def test_search_url_is_set(self):
        """Test that SEARCH_URL is properly configured."""
        assert Config.SEARCH_URL == "https://efdsearch.senate.gov/search/"

    def test_min_delay_is_positive(self):
        """Test that MIN_DELAY is a positive number."""
        assert Config.MIN_DELAY > 0

    def test_max_delay_greater_than_min(self):
        """Test that MAX_DELAY is greater than MIN_DELAY."""
        assert Config.MAX_DELAY > Config.MIN_DELAY

    def test_headers_contains_user_agent(self):
        """Test that HEADERS contains a User-Agent."""
        assert 'User-Agent' in Config.HEADERS
        assert len(Config.HEADERS['User-Agent']) > 0

    def test_headers_contains_accept(self):
        """Test that HEADERS contains Accept header."""
        assert 'Accept' in Config.HEADERS

    def test_get_delay_returns_float(self):
        """Test that get_delay() returns a float."""
        delay = Config.get_delay()
        assert isinstance(delay, float)

    def test_get_delay_within_range(self):
        """Test that get_delay() returns a value within the specified range."""
        for _ in range(10):
            delay = Config.get_delay()
            assert Config.MIN_DELAY <= delay <= Config.MAX_DELAY


class TestSenateScraper:
    """Tests for the SenateScraper class."""

    def test_init_creates_session(self):
        """Test that __init__ creates a requests.Session object."""
        scraper = SenateScraper()
        assert isinstance(scraper.session, requests.Session)

    def test_init_sets_headers(self):
        """Test that __init__ sets headers from Config."""
        scraper = SenateScraper()
        for key, value in Config.HEADERS.items():
            assert scraper.session.headers.get(key) == value

    def test_session_is_reusable(self):
        """Test that the session can be used for multiple requests."""
        scraper = SenateScraper()
        assert scraper.session is not None
        # Verify session is the same object across multiple accesses
        session1 = scraper.session
        session2 = scraper.session
        assert session1 is session2
