import requests
import json

# Replace these values with your actual data
base_url = "http://localhost:8080/server/api/core/bitstreamformats"
bitstream_format_id = 6
access_token = "eyJhbGciOiJIUzI1NiJ9.eyJlaWQiOiIzMzU2NDdiNi04YTUyLTRlY2ItYThjMS03ZWJhYmIxOTliZGEiLCJzZyI6W10sImF1dGhlbnRpY2F0aW9uTWV0aG9kIjoicGFzc3dvcmQiLCJleHAiOjE3MDEyOTMyNjh9.aksPpf1dAWZnW7RxUnQ-XyMofI39zpcdw1rupJCk2_U"

# URL for the specific bitstream format
url = "http://localhost:8080/server/api/core/bitstreamformats/6"

# Headers for the request
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}",
}

# JSON payload for the update
payload = {
    "id": bitstream_format_id,
    "shortDescription": "Text",
    "description": "Plain Text H",
    "mimetype": "text/plain",
    "supportLevel": "KNOWN",
    "internal": False,
    "extensions": ["txt", "asc"],
    "type": "bitstreamformat",
}

# Convert the payload to JSON
json_payload = json.dumps(payload)

# Send the PUT request
response = requests.put(url, headers=headers, data=json_payload)

# Check the response
if response.status_code == 200:
    print("Bitstream format updated successfully")
else:
    print(f"Error: {response.status_code}, {response.text}")
