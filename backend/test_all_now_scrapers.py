#!/usr/bin/env python3
"""
Test script to run all "now" scrapers and show total inventory
"""

from app.scrapers.now.elevon.drhorton import DRHortonElevonNowScraper
from app.scrapers.now.elevon.unionmain import UnionMainElevonNowScraper
from app.scrapers.now.elevon.historymaker import HistoryMakerElevonNowScraper
from app.scrapers.now.elevon.mihomes import MIHomesElevonNowScraper
from app.scrapers.now.elevon.trophysignature import TrophySignatureElevonNowScraper
from app.scrapers.now.elevon.pacesetter import PacesetterElevonNowScraper
from app.scrapers.now.elevon.khovnanian import KHovnanianElevonNowScraper

def test_all_now_scrapers():
    scrapers = [
        ("DR Horton", DRHortonElevonNowScraper()),
        ("Union Main", UnionMainElevonNowScraper()),
        ("HistoryMaker", HistoryMakerElevonNowScraper()),
        ("MI Homes", MIHomesElevonNowScraper()),
        ("Trophy Signature", TrophySignatureElevonNowScraper()),
        ("Pacesetter", PacesetterElevonNowScraper()),
        ("K.Hovnanian", KHovnanianElevonNowScraper()),
    ]
    
    total_inventory = 0
    all_homes = []
    
    print("=" * 60)
    print("TESTING ALL ELEVON INVENTORY SCRAPERS")
    print("=" * 60)
    
    for name, scraper in scrapers:
        print(f"\n--- Testing {name} ---")
        try:
            results = scraper.fetch_plans()
            print(f"✅ {name}: Found {len(results)} inventory homes")
            total_inventory += len(results)
            all_homes.extend(results)
            
            # Show some details for the first few homes
            for i, home in enumerate(results[:3]):
                print(f"  {i+1}. {home.get('plan_name', 'Unknown')} - ${home.get('price', 0):,} - {home.get('sqft', 0)} sqft")
                
        except Exception as e:
            print(f"❌ {name}: Error - {e}")
    
    print("\n" + "=" * 60)
    print(f"TOTAL INVENTORY: {total_inventory} homes across all builders")
    print("=" * 60)
    
    # Show summary by company
    company_counts = {}
    for home in all_homes:
        company = home.get('company', 'Unknown')
        company_counts[company] = company_counts.get(company, 0) + 1
    
    print("\nBreakdown by company:")
    for company, count in sorted(company_counts.items()):
        print(f"  {company}: {count} homes")
    
    # Show price ranges
    if all_homes:
        prices = [home.get('price', 0) for home in all_homes if home.get('price')]
        if prices:
            min_price = min(prices)
            max_price = max(prices)
            avg_price = sum(prices) / len(prices)
            print(f"\nPrice range: ${min_price:,} - ${max_price:,}")
            print(f"Average price: ${avg_price:,.0f}")

if __name__ == "__main__":
    test_all_now_scrapers() 