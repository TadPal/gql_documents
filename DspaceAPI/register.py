import requests

def create_dspace_account(email, password, additional_info=None):
    # DSpace backend registration endpoint (hypothetical example)
    dspace_register_url = 'http://localhost:8080/rest/register'

    # Request parameters for account creation
    registration_params = {
        'email': email,
        'password': password,
        'additional_info': additional_info
    }

    try:
        # Make a POST request to create a DSpace account
        response = requests.post(dspace_register_url, data=registration_params)

        # Check if the registration was successful (status code 200)
        if response.status_code == 200:
            # Print a success message
            print("Account created successfully.")
        else:
            # Print an error message if the registration was not successful
            print(f"Registration Error: {response.status_code}, {response.text}")

    except requests.RequestException as e:
        # Handle request exceptions (e.g., network issues)
        print(f"Request Exception: {e}")

# Example usage
email = 'newuser@example.com'
password = 'newpassword'
additional_info = {'name': 'John Doe', 'age': 25}

create_dspace_account(email, password, additional_info)
