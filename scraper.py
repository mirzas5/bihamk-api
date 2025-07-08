# scraper.py
# (Very short sketch – paste your real Playwright code here!)
import asyncio, json, re
from playwright.async_api import async_playwright

async def scrape_radars() -> list[dict]:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://bihamk.ba/spi/radari")
        # … your existing selector logic …
        radars = [
            {"id": "412", "title": "...", "text": "..."},
            # ...
        ]
        await browser.close()
        return radars