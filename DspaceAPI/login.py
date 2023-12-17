import requests

# Your login data
login_data = {
    "user": "dspacedemo+admin@gmail.com",
    "password": "dspace",
    

}

# CSRF token and cookie
csrf_token = "a354740d-80b3-4cc8-af26-674ca5da76e2; klaro-57d0a99d-d0f0-44b2-937c-43291b8a8b1d"
cookie = {"DSPACE-XSRF-COOKIE": "d5389e72-ea8f-4699-a0f7-0751b0d6e9b7"}

# Your login endpoint (corrected)
login_url = "http://localhost:8080/server/api/authn/login"

# Make the login request
response = requests.post(
    login_url,
    data=login_data,
    headers={"X-XSRF-TOKEN": csrf_token},
    cookies=cookie,
)

# Check if login was successful
if response.status_code == 200:
    # Extract the bearer token from the response
    bearer_token = response.headers.get("Authorization").replace("Bearer ", "")

    # Use the bearer token in subsequent requests
    headers = {"Authorization": f"Bearer {bearer_token}", "X-XSRF-TOKEN": csrf_token}

    # Now you can make authenticated requests using the headers
    # For example, let's check the status endpoint
    status_url = "http://localhost:8080/rest/status"
    status_response = requests.get(status_url, headers=headers)

    print(f"Status response: {status_response.status_code}")
    print(f"Status text: {status_response.text}")
else:
    print(f"Login Error: {response.status_code}, {response.text}")
