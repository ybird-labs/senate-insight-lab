import asyncio
from playwright.async_api import async_playwright

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

async def access_senate_search():
    async with async_playwright() as p:
        # Launch browser (use headless=False initially to debug)
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # Step 1: Navigate to agreement page
        await page.goto("https://efdsearch.senate.gov/search/")

        # Step 2: Accept the agreement
        await page.check("#agree_statement")  # Check the checkbox

        # Step 3: Wait for navigation to search page
        await page.wait_for_url("**/home/", timeout=10000)

        # Now you're on the search interface
        print(f"Current URL: {page.url}")


async def main():
    await access_senate_search()

if __name__ == "__main__":
    asyncio.run(main())
