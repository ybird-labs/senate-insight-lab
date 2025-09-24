import asyncio
from datetime import datetime

from playwright.async_api import async_playwright


class Config:
    BASE_URL = "https://efdsearch.senate.gov"
    SEARCH_URL = "https://efdsearch.senate.gov/search/"

    MIN_DELAY = 1.0  # Wait at least 1 second between requests
    MAX_DELAY = 3.0  # Wait at most 3 seconds between requests

    # Headers tell the website who we are
    HEADERS = {
        "User-Agent": "Research Bot 1.0 (Educational Use)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
    }


async def fill_date_fields(page, from_date: str, to_date: str) -> None:
    """Fill date fields using exact IDs from the HTML"""
    try:
        # Fill From date field
        from_field = await page.query_selector("#fromDate")
        if from_field:
            await from_field.click()
            await from_field.fill(from_date)
            print(f"Filled From date with: {from_date}")
        else:
            print("From date field not found")

        # Fill To date field
        to_field = await page.query_selector("#toDate")
        if to_field:
            await to_field.click()
            await to_field.fill(to_date)
            print(f"Filled To date with: {to_date}")
        else:
            print("To date field not found")

    except Exception as e:
        print(f"Error filling date fields: {e}")


async def access_senate_search(from_date: str, to_date: str) -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # Step 1: Navigate to agreement page
        await page.goto("https://efdsearch.senate.gov/search/")

        # Step 2: Accept the agreement if checkbox is present
        agree_checkbox = await page.query_selector("#agree_statement")
        if agree_checkbox:
            await page.check("#agree_statement")  # Check the checkbox
            print("Agreement accepted - waiting for search interface to load")

            # Wait for the search form to appear after agreement
            try:
                await page.wait_for_selector(
                    'input[placeholder*="First name"], h2:text("Search Options")',
                    timeout=10000,
                )
                print("Search interface loaded successfully")
            except:
                print("Search interface didn't load as expected")
        else:
            print("Agreement checkbox not found - already on search interface")

        # Wait for search form to appear after agreement
        if agree_checkbox:
            print("Waiting for search form to load after agreement...")
            await page.wait_for_selector('input[type="text"]', timeout=10000)
            print("Search form loaded!")

        # Step 3: Fill in the date fields
        await fill_date_fields(page, from_date, to_date)

        # Step 4: Click the search button
        search_button = await page.query_selector('button[type="submit"]')
        if search_button:
            await search_button.click()
            print("Clicked Search Reports button")

            # Wait for search results to load
            try:
                await page.wait_for_selector(
                    "#filedReports, .dataTables_wrapper", timeout=15000
                )
                print("Search results loaded successfully")
            except:
                print("Search results didn't load as expected, but continuing...")
        else:
            print("Search button not found")

        # Now you're on the search interface - ready to search
        print(f"Current URL: {page.url}")
        print("Browser is open - you can now interact with the search interface")
        print("Use this time to plan your next steps and explore the interface")

        # Keep browser open for interaction and planning
        input("Press Enter to close the browser...")

        await browser.close()


async def main() -> None:
    # Use the 23rd of current month
    today = datetime.now().replace(day=23).strftime("%m/%d/%Y")
    await access_senate_search(from_date=today, to_date=today)


if __name__ == "__main__":
    asyncio.run(main())
