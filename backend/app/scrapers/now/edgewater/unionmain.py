import requests
import re
from bs4 import BeautifulSoup
from ...base import BaseScraper
from typing import List, Dict

class UnionMainEdgewaterNowScraper(BaseScraper):
    URL = "https://unionmainhomes.com/all-homes/?nh=edgewater"
    
    def parse_sqft(self, text):
        """Extract square footage from text."""
        match = re.search(r'([\d,]+)', text)
        return int(match.group(1).replace(",", "")) if match else None

    def parse_price(self, text):
        """Extract current price from text."""
        match = re.search(r'\$([\d,]+)', text)
        return int(match.group(1).replace(",", "")) if match else None

    def parse_beds(self, text):
        """Extract number of bedrooms from text."""
        match = re.search(r'(\d+(?:\.\d+)?)', text)
        return str(match.group(1)) if match else ""

    def parse_baths(self, text):
        """Extract number of bathrooms from text."""
        # Handle both "3" and "3.5" formats
        match = re.search(r'(\d+(?:\.\d+)?)', text)
        return str(match.group(1)) if match else ""

    def parse_stories(self, text):
        """Extract number of stories from text."""
        # Default to 2 stories for these homes based on the data
        return "2"

    def get_status(self, container):
        """Extract the status of the home."""
        status_label = container.find('span', class_='label-status')
        if status_label:
            status_text = status_label.get_text(strip=True).lower()
            if 'move-in ready' in status_text:
                return "move-in ready"
            elif 'under construction' in status_text:
                return "under construction"
            elif 'coming soon' in status_text:
                return "coming soon"
        return "unknown"

    def get_price_cut(self, container):
        """Extract price cut information if available."""
        price_diff = container.find('span', class_='price_diff')
        if price_diff:
            price_cut_text = price_diff.get_text(strip=True)
            # Extract the amount from "Price cut: $47,375"
            match = re.search(r'Price cut: \$([\d,]+)', price_cut_text)
            if match:
                return match.group(1)
        return ""

    def fetch_plans(self) -> List[Dict]:
        try:
            print(f"[UnionMainEdgewaterNowScraper] Fetching URL: {self.URL}")
            
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                ),
                "Accept-Language": "en-US,en;q=0.9",
            }
            
            resp = requests.get(self.URL, headers=headers, timeout=15)
            print(f"[UnionMainEdgewaterNowScraper] Response status: {resp.status_code}")
            
            if resp.status_code != 200:
                print(f"[UnionMainEdgewaterNowScraper] Request failed with status {resp.status_code}")
                return []
            
            soup = BeautifulSoup(resp.content, 'html.parser')
            listings = []
            seen_addresses = set()  # Track addresses to prevent duplicates
            
            # Find all home listings in the section
            home_listings = soup.find_all('div', class_='item-listing-wrap single-fp slide')
            print(f"[UnionMainEdgewaterNowScraper] Found {len(home_listings)} home listings")
            
            for idx, listing in enumerate(home_listings):
                try:
                    print(f"[UnionMainEdgewaterNowScraper] Processing listing {idx+1}")
                    
                    # Extract address from the title link
                    title_link = listing.find('h2', class_='item-title').find('a') if listing.find('h2', class_='item-title') else None
                    if not title_link:
                        print(f"[UnionMainEdgewaterNowScraper] Skipping listing {idx+1}: No title link found")
                        continue
                    
                    address = title_link.get_text(strip=True)
                    if not address:
                        print(f"[UnionMainEdgewaterNowScraper] Skipping listing {idx+1}: Empty address")
                        continue
                    
                    # Check for duplicate addresses
                    if address in seen_addresses:
                        print(f"[UnionMainEdgewaterNowScraper] Skipping listing {idx+1}: Duplicate address '{address}'")
                        continue
                    
                    seen_addresses.add(address)
                    
                    # Extract price
                    price_li = listing.find('li', class_='item-price')
                    if not price_li:
                        print(f"[UnionMainEdgewaterNowScraper] Skipping listing {idx+1}: No price found")
                        continue
                    
                    current_price = self.parse_price(price_li.get_text())
                    if not current_price:
                        print(f"[UnionMainEdgewaterNowScraper] Skipping listing {idx+1}: No current price found")
                        continue
                    
                    # Extract beds, baths, and sqft from amenities
                    amenities = listing.find('ul', class_='item-amenities item-amenities-without-icons')
                    beds = ""
                    baths = ""
                    sqft = None
                    
                    if amenities:
                        amenity_items = amenities.find_all('li')
                        for item in amenity_items:
                            item_class = item.get('class', [])
                            if 'h-beds' in item_class:
                                hz_figure = item.find('span', class_='hz-figure')
                                if hz_figure:
                                    beds = self.parse_beds(hz_figure.get_text())
                            elif 'h-baths' in item_class:
                                hz_figure = item.find('span', class_='hz-figure')
                                if hz_figure:
                                    baths = self.parse_baths(hz_figure.get_text())
                            elif 'h-area' in item_class:
                                hz_figure = item.find('span', class_='hz-figure')
                                if hz_figure:
                                    sqft = self.parse_sqft(hz_figure.get_text())
                    
                    if not sqft:
                        print(f"[UnionMainEdgewaterNowScraper] Skipping listing {idx+1}: No square footage found")
                        continue
                    
                    # Calculate price per sqft
                    price_per_sqft = round(current_price / sqft, 2) if sqft > 0 else None
                    
                    # Get status and price cut information
                    status = self.get_status(listing)
                    price_cut = self.get_price_cut(listing)
                    
                    # Determine if it's a quick move-in home
                    is_quick_move_in = status == "move-in ready"
                    
                    # Create plan name from address (extract street number and name)
                    plan_name_match = re.search(r'(\d+)\s+([A-Za-z]+)', address)
                    plan_name = f"{plan_name_match.group(1)} {plan_name_match.group(2)}" if plan_name_match else address
                    
                    plan_data = {
                        "price": current_price,
                        "sqft": sqft,
                        "stories": self.parse_stories(""),
                        "price_per_sqft": price_per_sqft,
                        "plan_name": plan_name,
                        "company": "UnionMain Homes",
                        "community": "Edgewater",
                        "type": "now",
                        "beds": beds,
                        "baths": baths,
                        "address": address,
                        "original_price": None,
                        "price_cut": price_cut
                    }
                    
                    # Add additional metadata
                    if status:
                        plan_data["status"] = status
                    
                    print(f"[UnionMainEdgewaterNowScraper] Listing {idx+1}: {plan_data}")
                    listings.append(plan_data)
                    
                except Exception as e:
                    print(f"[UnionMainEdgewaterNowScraper] Error processing listing {idx+1}: {e}")
                    continue
            
            print(f"[UnionMainEdgewaterNowScraper] Successfully processed {len(listings)} listings")
            return listings
            
        except Exception as e:
            print(f"[UnionMainEdgewaterNowScraper] Error: {e}")
            return []
