import requests
import re
from bs4 import BeautifulSoup
from ...base import BaseScraper
from typing import List, Dict

class UnionMainCambridgeNowScraper(BaseScraper):
    URL = "https://unionmainhomes.com/cambridge-crossing/"
    
    def parse_sqft(self, text):
        """Extract square footage from text."""
        match = re.search(r'([\d,]+)', text)
        return int(match.group(1).replace(",", "")) if match else None

    def parse_price(self, text):
        """Extract price from text."""
        match = re.search(r'\$([\d,]+)', text)
        return int(match.group(1).replace(",", "")) if match else None

    def parse_beds(self, text):
        """Extract number of bedrooms from text."""
        match = re.search(r'(\d+)', text)
        return str(match.group(1)) if match else ""

    def parse_baths(self, text):
        """Extract number of bathrooms from text."""
        match = re.search(r'(\d+(?:\.\d+)?)', text)
        return str(match.group(1)) if match else ""

    def fetch_plans(self) -> List[Dict]:
        try:
            print(f"[UnionMainCambridgeNowScraper] Fetching URL: {self.URL}")
            
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                ),
                "Accept-Language": "en-US,en;q=0.9",
            }
            
            resp = requests.get(self.URL, headers=headers, timeout=15)
            print(f"[UnionMainCambridgeNowScraper] Response status: {resp.status_code}")
            
            if resp.status_code != 200:
                print(f"[UnionMainCambridgeNowScraper] Request failed with status {resp.status_code}")
                return []
            
            soup = BeautifulSoup(resp.content, 'html.parser')
            listings = []
            
            # Find all listing items - including hidden ones in the carousel
            # Look for all items with class 'item-listing-wrap' regardless of aria-hidden status
            listing_items = soup.find_all('div', class_='item-listing-wrap')
            print(f"[UnionMainCambridgeNowScraper] Found {len(listing_items)} total listing items")
            
            for idx, item in enumerate(listing_items):
                try:
                    print(f"[UnionMainCambridgeNowScraper] Processing listing {idx+1}")
                    
                    # Extract price
                    price_elem = item.find('li', class_='item-price')
                    if not price_elem:
                        print(f"[UnionMainCambridgeNowScraper] Skipping listing {idx+1}: No price found")
                        continue
                    
                    price_text = price_elem.get_text(strip=True)
                    price = self.parse_price(price_text)
                    if not price:
                        print(f"[UnionMainCambridgeNowScraper] Skipping listing {idx+1}: Could not parse price from '{price_text}'")
                        continue
                    
                    # Extract square footage
                    area_elem = item.find('li', class_='h-area')
                    if not area_elem:
                        print(f"[UnionMainCambridgeNowScraper] Skipping listing {idx+1}: No square footage found")
                        continue
                    
                    sqft_text = area_elem.get_text(strip=True)
                    sqft = self.parse_sqft(sqft_text)
                    if not sqft:
                        print(f"[UnionMainCambridgeNowScraper] Skipping listing {idx+1}: Could not parse sqft from '{sqft_text}'")
                        continue
                    
                    # Extract bedrooms
                    beds_elem = item.find('li', class_='h-beds')
                    beds = self.parse_beds(beds_elem.get_text(strip=True)) if beds_elem else ""
                    
                    # Extract bathrooms
                    baths_elem = item.find('li', class_='h-baths')
                    baths = self.parse_baths(baths_elem.get_text(strip=True)) if baths_elem else ""
                    
                    # Extract address/title
                    title_elem = item.find('h2', class_='item-title')
                    if not title_elem:
                        print(f"[UnionMainCambridgeNowScraper] Skipping listing {idx+1}: No title/address found")
                        continue
                    
                    address = title_elem.get_text(strip=True)
                    if not address:
                        print(f"[UnionMainCambridgeNowScraper] Skipping listing {idx+1}: Empty address")
                        continue
                    
                    # Calculate price per sqft
                    price_per_sqft = round(price / sqft, 2) if sqft > 0 else None
                    
                    # Check status - we want both "move-in ready" and "under construction" homes
                    # since "under construction" homes can also be available for purchase
                    status_elem = item.find('span', class_='label-status')
                    status = status_elem.get_text(strip=True) if status_elem else ""
                    
                    # Check if it's available (either move-in ready or under construction)
                    is_available = any(keyword in status.lower() for keyword in ["move-in ready", "under construction"])
                    
                    if not is_available:
                        print(f"[UnionMainCambridgeNowScraper] Skipping listing {idx+1}: Not available (status: {status})")
                        continue
                    
                    # Check if there's a move-in date (for under construction homes)
                    move_in_elem = item.find('li', class_=re.compile(r'h-move-in'))
                    move_in_date = ""
                    if move_in_elem:
                        move_in_text = move_in_elem.get_text(strip=True)
                        # Extract date information
                        date_match = re.search(r'(\d{4}-\d{2}(?:-\d{2})?|Now|Oct|Nov|Dec)', move_in_text)
                        if date_match:
                            move_in_date = date_match.group(1)
                    
                    # Check for price cuts
                    price_cut_elem = item.find('span', class_='price_diff')
                    price_cut = ""
                    if price_cut_elem:
                        price_cut = price_cut_elem.get_text(strip=True)
                    
                    plan_data = {
                        "price": price,
                        "sqft": sqft,
                        "stories": "1",  # Default to 1 story for single-family homes
                        "price_per_sqft": price_per_sqft,
                        "plan_name": address,
                        "company": "UnionMain Homes",
                        "community": "Cambridge",
                        "type": "now",
                        "beds": beds,
                        "baths": baths,
                        "address": address,
                        "status": status,
                        "move_in_date": move_in_date,
                        "price_cut": price_cut
                    }
                    
                    print(f"[UnionMainCambridgeNowScraper] Listing {idx+1}: {plan_data}")
                    listings.append(plan_data)
                    
                except Exception as e:
                    print(f"[UnionMainCambridgeNowScraper] Error processing listing {idx+1}: {e}")
                    continue
            
            print(f"[UnionMainCambridgeNowScraper] Successfully processed {len(listings)} available homes")
            return listings
            
        except Exception as e:
            print(f"[UnionMainCambridgeNowScraper] Error: {e}")
            return [] 