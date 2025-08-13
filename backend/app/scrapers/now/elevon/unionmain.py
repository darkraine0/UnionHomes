import requests
from bs4 import BeautifulSoup
import re
from ...base import BaseScraper
from typing import List, Dict

class UnionMainElevonNowScraper(BaseScraper):
    URL = "https://unionmainhomes.com/all-homes/?nh=elevon"

    def parse_price(self, text):
        match = re.search(r'\$([\d,]+)', text)
        return int(match.group(1).replace(",", "")) if match else None

    def fetch_plans(self) -> List[Dict]:
        try:
            print(f"[UnionMainElevonNowScraper] Fetching URL: {self.URL}")
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                ),
                "Accept-Language": "en-US,en;q=0.9",
            }
            resp = requests.get(self.URL, headers=headers, timeout=10)
            print(f"[UnionMainElevonNowScraper] Response status: {resp.status_code}")
            soup = BeautifulSoup(resp.text, "html.parser")
            listings = []
            cards = soup.select('section#fp .item-listing-wrap')
            print(f"[UnionMainElevonNowScraper] Found {len(cards)} home cards.")
            for idx, card in enumerate(cards):
                price_tag = card.select_one('.item-price')
                price = self.parse_price(price_tag.get_text() if price_tag else "")
                if price is None:
                    print(f"[UnionMainElevonNowScraper] Skipping card {idx+1}: Missing price.")
                    continue
                h2 = card.select_one('.item-title a')
                plan_name = h2.get_text(strip=True) if h2 else ""
                sqft_tag = card.select_one('.h-area .hz-figure')
                sqft = int(sqft_tag.get_text(strip=True).replace(",", "")) if sqft_tag else None
                stories = ""
                price_per_sqft = round(price / sqft, 2) if price and sqft else None
                plan_data = {
                    "price": price,
                    "sqft": sqft,
                    "stories": stories,
                    "price_per_sqft": price_per_sqft,
                    "plan_name": plan_name,
                    "company": "UnionMain Homes",
                    "community": "Elevon",
                    "type": "now"
                }
                print(f"[UnionMainElevonNowScraper] Card {idx+1}: {plan_data}")
                listings.append(plan_data)
            return listings
        except Exception as e:
            print(f"[UnionMainElevonNowScraper] Error: {e}")
            return [] 