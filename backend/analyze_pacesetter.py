import requests
from bs4 import BeautifulSoup
import re

def analyze_pacesetter():
    url = "https://elevontx.com/builder/pacesetter-homes/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    
    print(f"Analyzing Pacesetter URL: {url}")
    resp = requests.get(url, headers=headers)
    print(f"Status: {resp.status_code}")
    
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    # Look for all listing cards
    all_cards = soup.find_all('div', class_="ct-div-block collectable listing")
    print(f"\nFound {len(all_cards)} total listing cards")
    
    # Analyze each card
    for i, card in enumerate(all_cards[:5]):  # Look at first 5 cards
        print(f"\n--- Card {i+1} ---")
        print(f"Classes: {card.get('class', [])}")
        print(f"Data attributes: {dict(card.attrs)}")
        
        # Look for any text that might indicate inventory status
        card_text = card.get_text().lower()
        inventory_keywords = ['now', 'available', 'ready', 'move-in', 'inventory', 'quick move-in']
        found_keywords = [kw for kw in inventory_keywords if kw in card_text]
        if found_keywords:
            print(f"Found inventory keywords: {found_keywords}")
        
        # Look for price and sqft
        price_elements = card.find_all(text=re.compile(r'\$[\d,]+'))
        sqft_elements = card.find_all(text=re.compile(r'[\d,]+\s*sq\.?\s*ft', re.IGNORECASE))
        
        if price_elements:
            print(f"Price elements: {price_elements}")
        if sqft_elements:
            print(f"Sqft elements: {sqft_elements}")
        
        # Look for headlines/titles
        headlines = card.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        if headlines:
            print(f"Headlines: {[h.get_text(strip=True) for h in headlines]}")
    
    # Look for any sections that might contain inventory
    print(f"\n--- Looking for inventory sections ---")
    inventory_sections = soup.find_all(text=re.compile(r'inventory|available|now|ready|move-in', re.IGNORECASE))
    print(f"Found {len(inventory_sections)} text elements with inventory keywords")
    
    for section in inventory_sections[:10]:  # Show first 10
        parent = section.parent
        if parent:
            print(f"Section: {section.strip()}")
            print(f"Parent tag: {parent.name}, classes: {parent.get('class', [])}")
    
    # Look for any links that might lead to inventory
    print(f"\n--- Looking for inventory links ---")
    all_links = soup.find_all('a', href=True)
    inventory_links = []
    
    for link in all_links:
        href = link.get('href', '').lower()
        text = link.get_text().lower()
        if any(keyword in href or keyword in text for keyword in ['inventory', 'available', 'now', 'ready']):
            inventory_links.append(link)
    
    print(f"Found {len(inventory_links)} potential inventory links")
    for link in inventory_links[:5]:
        print(f"  - {link.get('href')} (text: {link.get_text(strip=True)})")

if __name__ == "__main__":
    analyze_pacesetter() 