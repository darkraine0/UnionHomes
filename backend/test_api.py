import requests
import json

def test_api():
    try:
        # Test the API endpoint
        response = requests.get('http://localhost:8080/api/plans')
        if response.status_code == 200:
            data = response.json()
            
            # Filter for K.Hovnanian homes
            khovnanian_homes = [home for home in data if home.get('company') == 'K. Hovnanian Homes']
            
            print(f"Total homes in API: {len(data)}")
            print(f"K.Hovnanian homes: {len(khovnanian_homes)}")
            
            if khovnanian_homes:
                print("\nK.Hovnanian Homes found:")
                for i, home in enumerate(khovnanian_homes[:3], 1):
                    print(f"{i}. {home.get('plan_name')} - ${home.get('price'):,} - {home.get('sqft')} sqft")
            else:
                print("No K.Hovnanian homes found in API response")
                
        else:
            print(f"API request failed with status code: {response.status_code}")
            
    except Exception as e:
        print(f"Error testing API: {e}")

if __name__ == "__main__":
    test_api() 