import requests
import re
from bs4 import BeautifulSoup
from ...base import BaseScraper
from typing import List, Dict

class UnionMainCambridgePlanScraper(BaseScraper):
    URL = "https://unionmainhomes.com/cambridge-crossing/"
    
    def parse_sqft(self, text):
        """Extract square footage from text."""
        match = re.search(r'([\d,]+)', text)
        return int(match.group(1).replace(",", "")) if match else None

    def parse_price(self, text):
        """Extract base price from text."""
        match = re.search(r'from \$([\d,]+)', text)
        return int(match.group(1).replace(",", "")) if match else None

    def parse_beds(self, text):
        """Extract number of bedrooms from text."""
        match = re.search(r'(\d+)', text)
        return str(match.group(1)) if match else ""

    def parse_baths(self, text):
        """Extract number of bathrooms from text."""
        match = re.search(r'(\d+(?:\.\d+)?)', text)
        return str(match.group(1)) if match else ""

    def is_floor_plan(self, title):
        """Check if the title represents a floor plan (not an address)."""
        # Floor plans have names like "Cameron", "Mason", "Travis"
        # Addresses have patterns like "2809 Somerset Ln., Celina, TX 75009"
        address_pattern = r'\d+\s+[A-Za-z\s]+(?:Ln|Ct|St|Dr|Ave|Blvd)\.?,\s+[A-Za-z\s]+,\s+[A-Z]{2}\s+\d{5}'
        return not re.search(address_pattern, title)

    def fetch_plans(self) -> List[Dict]:
        try:
            print(f"[UnionMainCambridgePlanScraper] Fetching URL: {self.URL}")
            
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                ),
                "Accept-Language": "en-US,en;q=0.9",
            }
            
            resp = requests.get(self.URL, headers=headers, timeout=15)
            print(f"[UnionMainCambridgePlanScraper] Response status: {resp.status_code}")
            
            if resp.status_code != 200:
                print(f"[UnionMainCambridgePlanScraper] Request failed with status {resp.status_code}")
                return []
            
            soup = BeautifulSoup(resp.content, 'html.parser')
            plans = []
            
            # Find all floor plan items - look for items with class 'single-fp'
            # This targets the floor plans section specifically
            plan_items = soup.find_all('div', class_='single-fp')
            print(f"[UnionMainCambridgePlanScraper] Found {len(plan_items)} total items")
            
            for idx, item in enumerate(plan_items):
                try:
                    print(f"[UnionMainCambridgePlanScraper] Processing item {idx+1}")
                    
                    # Extract plan name
                    title_elem = item.find('h2', class_='item-title')
                    if not title_elem:
                        print(f"[UnionMainCambridgePlanScraper] Skipping item {idx+1}: No title found")
                        continue
                    
                    plan_name = title_elem.get_text(strip=True)
                    if not plan_name:
                        print(f"[UnionMainCambridgePlanScraper] Skipping item {idx+1}: Empty plan name")
                        continue
                    
                    # Check if this is actually a floor plan (not an address from the Now tab)
                    if not self.is_floor_plan(plan_name):
                        print(f"[UnionMainCambridgePlanScraper] Skipping item {idx+1}: This is an address, not a floor plan: {plan_name}")
                        continue
                    
                    # Extract base price
                    price_elem = item.find('div', class_='item-price')
                    if not price_elem:
                        print(f"[UnionMainCambridgePlanScraper] Skipping item {idx+1}: No price found")
                        continue
                    
                    price_text = price_elem.get_text(strip=True)
                    base_price = self.parse_price(price_text)
                    if not base_price:
                        print(f"[UnionMainCambridgePlanScraper] Skipping item {idx+1}: Could not parse price from '{price_text}'")
                        continue
                    
                    # Extract square footage
                    area_elem = item.find('li', class_='h-area')
                    if not area_elem:
                        print(f"[UnionMainCambridgePlanScraper] Skipping item {idx+1}: No square footage found")
                        continue
                    
                    sqft_text = area_elem.get_text(strip=True)
                    sqft = self.parse_sqft(sqft_text)
                    if not sqft:
                        print(f"[UnionMainCambridgePlanScraper] Skipping item {idx+1}: Could not parse sqft from '{sqft_text}'")
                        continue
                    
                    # Extract bedrooms
                    beds_elem = item.find('li', class_='x-beds')
                    beds = self.parse_beds(beds_elem.get_text(strip=True)) if beds_elem else ""
                    
                    # Extract bathrooms
                    baths_elem = item.find('li', class_='x-baths')
                    baths = self.parse_baths(baths_elem.get_text(strip=True)) if baths_elem else ""
                    
                    # Calculate price per sqft
                    price_per_sqft = round(base_price / sqft, 2) if sqft > 0 else None
                    
                    # Extract address/community info
                    address_elem = item.find('address', class_='item-address')
                    address = address_elem.get_text(strip=True) if address_elem else plan_name
                    
                    plan_data = {
                        "price": base_price,
                        "sqft": sqft,
                        "stories": "1",  # Default to 1 story for single-family homes
                        "price_per_sqft": price_per_sqft,
                        "plan_name": plan_name,
                        "company": "UnionMain Homes",
                        "community": "Cambridge",
                        "type": "plan",  # This is for floor plans, not quick move-ins
                        "beds": beds,
                        "baths": baths,
                        "address": address
                    }
                    
                    print(f"[UnionMainCambridgePlanScraper] Floor Plan: {plan_data}")
                    plans.append(plan_data)
                    
                except Exception as e:
                    print(f"[UnionMainCambridgePlanScraper] Error processing item {idx+1}: {e}")
                    continue
            
            print(f"[UnionMainCambridgePlanScraper] Successfully processed {len(plans)} floor plans")
            return plans
            
        except Exception as e:
            print(f"[UnionMainCambridgePlanScraper] Error: {e}")
            return [] 