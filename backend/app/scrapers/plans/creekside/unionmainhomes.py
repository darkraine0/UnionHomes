import requests
import re
from bs4 import BeautifulSoup
from ...base import BaseScraper
from typing import List, Dict

class UnionMainHomesCreeksidePlanScraper(BaseScraper):
    URLS = [
        "https://unionmainhomes.com/floorplans-all/?nh=creekside"
    ]

    def parse_sqft(self, text):
        """Extract square footage from text."""
        if not text:
            return None
        match = re.search(r'([\d,]+)', text)
        return int(match.group(1).replace(",", "")) if match else None

    def parse_price(self, text):
        """Extract price from text."""
        if not text:
            return None
        match = re.search(r'\$([\d,]+)', text)
        return int(match.group(1).replace(",", "")) if match else None

    def parse_beds(self, text):
        """Extract number of bedrooms from text."""
        if not text:
            return None
        match = re.search(r'(\d+)', text)
        return str(match.group(1)) if match else None

    def parse_baths(self, text):
        """Extract number of bathrooms from text."""
        if not text:
            return None
        match = re.search(r'(\d+\.?\d*)', text)
        return str(match.group(1)) if match else None

    def parse_stories(self, text):
        """Extract number of stories from text."""
        # Default to 1 story for single-family homes
        return "1"

    def parse_lot_size(self, text):
        """Extract lot size from text."""
        # Not available in the provided HTML structure
        return None

    def extract_plan_data(self, plan_card):
        """Extract data from a plan card div."""
        try:
            # Extract plan name from the item title
            plan_name = None
            title_elem = plan_card.find('h2', class_='item-title')
            if title_elem:
                title_link = title_elem.find('a')
                if title_link:
                    plan_name = title_link.get_text(strip=True)

            # Extract price
            price = None
            price_elem = plan_card.find('div', class_='item-price')
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                price = self.parse_price(price_text)

            # Extract features from the amenities list
            beds = None
            baths = None
            sqft = None
            stories = None

            amenities_list = plan_card.find('ul', class_='item-amenities')
            if amenities_list:
                amenities = amenities_list.find_all('li')
                for amenity in amenities:
                    amenity_text = amenity.get_text(strip=True)
                    
                    # Look for bed/bath/sqft information
                    if 'bds' in amenity_text:
                        beds = self.parse_beds(amenity_text)
                    elif 'ba' in amenity_text:
                        baths = self.parse_baths(amenity_text)
                    elif 'sqft' in amenity_text:
                        sqft = self.parse_sqft(amenity_text)

            # Extract stories (default to 1)
            stories = "1"

            # Extract lot size (not available in this structure)
            lot_size = None

            return {
                "price": price,
                "sqft": sqft,
                "stories": stories,
                "plan_name": plan_name,
                "beds": beds,
                "baths": baths,
                "lot_size": lot_size
            }

        except Exception as e:
            print(f"[UnionMainHomesCreeksidePlanScraper] Error extracting plan data: {e}")
            return None

    def fetch_plans(self) -> List[Dict]:
        try:
            print(f"[UnionMainHomesCreeksidePlanScraper] Fetching URLs: {self.URLS}")

            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/138.0.0.0 Safari/537.36"
                ),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "identity",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            }

            all_plans = []
            seen_plans = set()  # Track plans to prevent duplicates

            for url_idx, url in enumerate(self.URLS):
                try:
                    print(f"[UnionMainHomesCreeksidePlanScraper] Processing URL {url_idx + 1}: {url}")

                    resp = requests.get(url, headers=headers, timeout=15)
                    print(f"[UnionMainHomesCreeksidePlanScraper] URL {url_idx + 1} response status: {resp.status_code}")

                    if resp.status_code != 200:
                        print(f"[UnionMainHomesCreeksidePlanScraper] URL {url_idx + 1} request failed with status {resp.status_code}")
                        continue

                    soup = BeautifulSoup(resp.content, 'html.parser')

                    # Look for plan cards with class "item-listing-wrap"
                    plan_cards = soup.find_all('div', class_='item-listing-wrap')
                    print(f"[UnionMainHomesCreeksidePlanScraper] URL {url_idx + 1}: Found {len(plan_cards)} plan cards")

                    for card_idx, plan_card in enumerate(plan_cards):
                        try:
                            print(f"[UnionMainHomesCreeksidePlanScraper] URL {url_idx + 1}, Card {card_idx + 1}: Processing plan card")

                            # Extract data from the plan card
                            plan_data = self.extract_plan_data(plan_card)
                            if not plan_data:
                                print(f"[UnionMainHomesCreeksidePlanScraper] URL {url_idx + 1}, Card {card_idx + 1}: Failed to extract plan data")
                                continue

                            # Check for required fields - require plan_name
                            if not plan_data.get('plan_name'):
                                print(f"[UnionMainHomesCreeksidePlanScraper] URL {url_idx + 1}, Card {card_idx + 1}: Missing plan name")
                                continue

                            # Check for duplicate plans - use plan_name as unique identifier
                            plan_name = plan_data.get('plan_name')
                            if plan_name in seen_plans:
                                print(f"[UnionMainHomesCreeksidePlanScraper] URL {url_idx + 1}, Card {card_idx + 1}: Duplicate plan {plan_name}")
                                continue
                            seen_plans.add(plan_name)

                            # Calculate price per square foot if both price and sqft are available
                            price_per_sqft = None
                            if plan_data.get('price') and plan_data.get('sqft'):
                                price_per_sqft = round(plan_data['price'] / plan_data['sqft'], 2) if plan_data['sqft'] > 0 else None

                            # Create the final plan data
                            final_plan_data = {
                                "price": plan_data['price'],
                                "sqft": plan_data['sqft'],
                                "stories": plan_data['stories'],
                                "price_per_sqft": price_per_sqft,
                                "plan_name": plan_data['plan_name'],
                                "company": "UnionMain Homes",
                                "community": "Creekside",
                                "type": "plan",
                                "beds": plan_data['beds'],
                                "baths": plan_data['baths'],
                                "lot_size": plan_data['lot_size']
                            }

                            print(f"[UnionMainHomesCreeksidePlanScraper] URL {url_idx + 1}, Card {card_idx + 1}: {final_plan_data}")
                            all_plans.append(final_plan_data)

                        except Exception as e:
                            print(f"[UnionMainHomesCreeksidePlanScraper] URL {url_idx + 1}, Card {card_idx + 1}: Error processing card: {e}")
                            continue

                except Exception as e:
                    print(f"[UnionMainHomesCreeksidePlanScraper] Error processing URL {url_idx + 1}: {e}")
                    continue

            print(f"[UnionMainHomesCreeksidePlanScraper] Successfully processed {len(all_plans)} total plans across all URLs")
            return all_plans

        except Exception as e:
            print(f"[UnionMainHomesCreeksidePlanScraper] Error: {e}")
            return []
