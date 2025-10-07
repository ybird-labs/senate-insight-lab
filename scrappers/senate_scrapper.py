import random
import requests

class Config:
    BASE_URL = "https://efdsearch.senate.gov"
    SEARCH_URL = "https://efdsearch.senate.gov/search/"

    MIN_DELAY = 1.0  # Wait at least 1 second between requests
    MAX_DELAY = 3.0  # Wait at most 3 seconds between requests

    # Headers tell the website who we are
    HEADERS = {
        'User-Agent': 'Research Bot 1.0 (Educational Use)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    }

    @staticmethod
    def get_delay():
        """Returns a random delay between MIN_DELAY and MAX_DELAY"""
        return random.uniform(Config.MIN_DELAY, Config.MAX_DELAY)


class SenateScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(Config.HEADERS)



# class SenateScraper:
#     def __init__(self):
#         # Create a session to reuse connections
#         self.session = requests.Session()
#         self.session.headers.update(Config.HEADERS)
#         print("✅ Senate Scraper initialized")

#     def make_request(self, url):
#         """Downloads a web page safely with delays"""
#         print(f"🌐 Fetching: {url}")

#         # Wait before making request (be respectful!)
#         time.sleep(Config.get_delay())

#         try:
#             response = self.session.get(url, timeout=30)
#             if response.status_code == 200:
#                 print(f"✅ Success: {response.status_code}")
#                 return response
#             else:
#                 print(f"❌ Error: {response.status_code}")
#                 return None
#         except Exception as e:
#             print(f"❌ Request failed: {e}")
#             return None
