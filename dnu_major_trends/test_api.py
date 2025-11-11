"""Test API endpoints"""
import requests

base_url = "http://127.0.0.1:5000"

# Login first
session = requests.Session()
login_data = {"username": "admin", "password": "admin"}
login_response = session.post(f"{base_url}/login", data=login_data)
print(f"Login status: {login_response.status_code}")

# Test API endpoints
apis = [
    "/api/overview",
    "/api/majors",
    "/api/heatmap",
]

for api in apis:
    try:
        response = session.get(f"{base_url}{api}")
        print(f"\n{'='*60}")
        print(f"API: {api}")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Response: {data}")
    except Exception as e:
        print(f"Error calling {api}: {e}")
