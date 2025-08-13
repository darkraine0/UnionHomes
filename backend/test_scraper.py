import requests
from bs4 import BeautifulSoup

def test_historymaker():
    url = "https://elevontx.com/builder/historymaker-homes/"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }
    resp = requests.get(url, headers=headers, timeout=10)
    print(f"Status: {resp.status_code}")
    
    soup = BeautifulSoup(resp.text, "html.parser")
    
    # Try different selectors
    selectors = [
        '.dynamic-list-container .item-listing-wrap',
        '.item-listing-wrap',
        '.ct-div-block.collectable.listing',
        'div[class*="listing"]',
        'div[class*="card"]',
        'a[class*="card"]',
        'div[class*="item"]'
    ]
    
    for selector in selectors:
        elements = soup.select(selector)
        print(f"Selector '{selector}': Found {len(elements)} elements")
        if elements:
            print(f"First element classes: {elements[0].get('class', [])}")
            print(f"First element tag: {elements[0].name}")
            break

if __name__ == "__main__":
    test_historymaker() 