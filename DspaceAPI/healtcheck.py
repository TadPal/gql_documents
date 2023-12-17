import requests

def check_dspace_health(dspace_health_url):
    # DSpace backend health endpoint
    #dspace_health_url = 'http://localhost:8080/server/actuator/health'

    try:
        # Make a GET request to check the health of the DSpace backend
        response = requests.get(dspace_health_url)

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

#Example usage
# dspace_health_result = check_dspace_health()

# if dspace_health_result is not None:
#     print("DSpace Health Result:")
#     print(dspace_health_result)
# else:
#     print("Failed to retrieve DSpace health status.")
