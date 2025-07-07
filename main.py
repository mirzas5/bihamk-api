from fastapi import FastAPI
from playwright.sync_api import sync_playwright
import re

app = FastAPI()

@app.get("/radars")
def scrape_radars():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://bihamk.ba/spi/radari", timeout=60000)

        card_sel = "article[wire\\:click^='loadModal']"
        page.wait_for_selector(card_sel, timeout=15000)
        cards = page.query_selector_all(card_sel)

        results = []

        for card in cards:
            title = card.query_selector("h3").inner_text().strip()
            radar_id = re.search(r"\d+", card.get_attribute("wire:click")).group(0)

            card.click()
            overlay_sel = "div.fixed.inset-0.z-\\[100\\]"
            page.wait_for_selector(overlay_sel, timeout=10000)

            modal_text = page.query_selector("div.text-editor").inner_text().strip()
            results.append({"id": radar_id, "title": title, "text": modal_text})

            close_btn = page.locator(f"{overlay_sel} span:has-text('Zatvori')").first
            close_btn.click()
            page.wait_for_selector(overlay_sel, state="hidden", timeout=10000)

        browser.close()
        return results