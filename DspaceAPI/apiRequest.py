import requests

def request(url):
    try:
        # Make a GET request to check the health of the DSpace backend
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse and return the JSON response
            return str(response.json())
        else:
            # Print an error message if the request was not successful
            print(f"Error: {response.status_code}, {response.text}")
            return None

    except requests.RequestException as e:
        # Handle request exceptions (e.g., network issues)
        print(f"Request Exception: {e}")
        return None
