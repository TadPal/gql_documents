import requests

def dspace_login(email, password):
    # DSpace backend login endpoint
    dspace_login_url = 'http://localhost:8080/rest/login'

    # Request parameters for login
    login_params = {'email': email, 'password': password}

    try:
        # Make a POST request to login to the DSpace backend
        response = requests.post(dspace_login_url, data=login_params)

        # Check if the login was successful (status code 200)
        if response.status_code == 200:
            # Extract and return the JSESSIONID cookie from the response
            return response.cookies.get('JSESSIONID')
        else:
            # Print an error message if the login was not successful
            print(f"Login Error: {response.status_code}, {response.text}")
            return "Login Error: {response.status_code}, {response.text}"

    except requests.RequestException as e:
        # Handle request exceptions (e.g., network issues)
        print(f"Request Exception: {e}")
        return (f"Request Exception: {e}")

# Example usage
email = 'test@dspace'
password = 'pass'

jsessionid = dspace_login(email, password)

if jsessionid is not None:
    print(f"Login successful. JSESSIONID: {jsessionid}")
else:
    print("Login failed.")
