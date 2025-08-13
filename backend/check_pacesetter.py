import requests
from bs4 import BeautifulSoup

def check_pacesetter():
    url = "https://elevontx.com/builder/pacesetter-homes/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    
    print(f"Checking Pacesetter URL: {url}")
    resp = requests.get(url, headers=headers)
    print(f"Status: {resp.status_code}")
    
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    # Look for any "now" or "inventory" related content
    now_content = soup.find_all(text=lambda text: text and ('now' in text.lower() or 'inventory' in text.lower() or 'available' in text.lower()))
    print(f"Found {len(now_content)} references to now/inventory/available content")
    
    # Look for any "ready" or "move-in" content
    ready_content = soup.find_all(text=lambda text: text and ('ready' in text.lower() or 'move-in' in text.lower()))
    print(f"Found {len(ready_content)} references to ready/move-in content")
    
    # Check page title
    title = soup.title.string if soup.title else "No title"
    print(f"Page title: {title}")
    
    # Look for any links that might lead to inventory
    links = soup.find_all('a', href=True)
    inventory_links = [link for link in links if any(word in link.get('href', '').lower() for word in ['inventory', 'available', 'now', 'ready'])]
    print(f"Found {len(inventory_links)} potential inventory links")
    
    for link in inventory_links[:5]:  # Show first 5
        print(f"  - {link.get('href')}")

if __name__ == "__main__":
    check_pacesetter() 