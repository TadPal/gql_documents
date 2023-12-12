import requests

# Replace this token with your actual JWT token
jwt_token = "eyJhbGciOiJIUzI1NiJ9.eyJlaWQiOiIzMzU2NDdiNi04YTUyLTRlY2ItYThjMS03ZWJhYmIxOTliZGEiLCJzZyI6W10sImF1dGhlbnRpY2F0aW9uTWV0aG9kIjoicGFzc3dvcmQiLCJleHAiOjE3MDEyOTMyNjh9.aksPpf1dAWZnW7RxUnQ-XyMofI39zpcdw1rupJCk2_U"

# URL for the status endpoint
url = "http://localhost:8080/server/api/authn/status"

# Headers for the request
headers = {
    "Authorization": f"Bearer {jwt_token}",
}

# Send the GET request
response = requests.get(url, headers=headers)

# Check the response
if response.status_code == 200:
    print("Authentication status:", response.json())
else:
    print(f"Error: {response.status_code}, {response.text}")
