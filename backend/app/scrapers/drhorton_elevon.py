import requests
from bs4 import BeautifulSoup
from .base import BaseScraper
from typing import List, Dict

class DRHortonElevonScraper(BaseScraper):
    URL = "https://www.drhorton.com/texas/dallas/lavon/elevon"

    def fetch_plans(self) -> List[Dict]:
        try:
            response = requests.get(self.URL, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            plans = []
            # This is a placeholder. The actual selectors may need to be updated based on the real HTML structure.
            for card in soup.find_all("div", class_="plan-card"):
                plan_name = card.find("div", class_="plan-title").get_text(strip=True)
                price_text = card.find("div", class_="plan-price").get_text(strip=True)
                sqft_text = card.find("div", class_="plan-sqft").get_text(strip=True)
                stories_text = card.find("div", class_="plan-stories").get_text(strip=True)
                price = float(price_text.replace("$", "").replace(",", ""))
                sqft = int(sqft_text.replace(",", "").replace("Sq. Ft.", "").strip())
                price_per_sqft = round(price / sqft, 2) if sqft else 0
                plans.append({
                    "plan_name": plan_name,
                    "price": price,
                    "sqft": sqft,
                    "stories": stories_text,
                    "price_per_sqft": price_per_sqft
                })
            return plans
        except Exception as e:
            print(f"[DRHortonElevonScraper] Error: {e}")
            return [] 