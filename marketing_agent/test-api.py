import requests
import json

# Test the API
base_url = "http://localhost:8000"

print("=" * 60)
print("Testing Marketing Planning Assistant API")
print("=" * 60)

# Test 1: Health Check
print("\n[1] Health Check:")
response = requests.get(f"{base_url}/health")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

# Test 2: Generate Plan
print("\n[2] Generate Marketing Plan:")
payload = {
    "goal": "Increase brand awareness for a tech startup",
    "use_ai": True,
    "duration_days": 14,
    "custom_instructions": ""
}

response = requests.post(
    f"{base_url}/plan",
    json=payload
)

print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Success! Generated plan with {len(data.get('tasks', []))} tasks")
    print(f"Interpretation: {data.get('interpretation', {}).get('primary_objective', 'N/A')}")
else:
    print(f"Error: {response.text[:500]}")

print("\n" + "=" * 60)
