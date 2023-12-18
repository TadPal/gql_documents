import aiohttp
import asyncio
import json

async def createWorkspaceItem():

    async with aiohttp.ClientSession() as session:
        # Step 1: Get XSRF token from cookie
        url_step1 = "http://localhost:8080/server/api/authn/status"
        headers_step1 = {"Content-Type": "application/x-www-form-urlencoded"}

        async with session.get(url_step1, headers=headers_step1) as response_step1:
            xsrf_cookie = response_step1.cookies.get("DSPACE-XSRF-COOKIE").value
            print(f"XSRF Cookie: {xsrf_cookie}")

            # Step 2: Login and obtain Bearer token
            url_step2 = "http://localhost:8080/server/api/authn/login"
            headers_step2 = {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-XSRF-TOKEN": xsrf_cookie,
            }
            params_step2 = {"user": "test@test.edu", "password": "admin"}

            async with session.post(url_step2, headers=headers_step2, data=params_step2) as response_step2:
                bearer_token = response_step2.headers.get("Authorization")
                xsrf_cookie = response_step2.cookies.get("DSPACE-XSRF-COOKIE").value

                # Step 3: Access a new API endpoint
                url_step3 = "http://localhost:8080/server/api/submission/workspaceitems"
                headers_step3 = {
                }
                data_step3 = {} 

                async with session.post(url_step3, headers=headers_step3, data=json.dumps(data_step3)) as response_step3:
                        # Print the response for Step 3
                    xsrf_cookie_step3 = response_step3.cookies.get("DSPACE-XSRF-COOKIE").value

                    # Step 4: Another API endpoint using XSRF cookie from Step 3
                    url_step4 = "http://localhost:8080/server/api/submission/workspaceitems"  
                    headers_step4 = {
                        "Content-Type": "application/json",
                        "Authorization": bearer_token,
                        "X-XSRF-TOKEN": xsrf_cookie_step3,  # Use XSRF cookie from Step 3
                    }
                    data_step4 = {}  # Your JSON request body here

                    async with session.post(url_step4, headers=headers_step4, data=json.dumps(data_step4)) as response_step4:
                        # Print the response for Step 4
                        return await response_step4.json()

# Run the asynchronous event loop
result = asyncio.run(createWorkspaceItem())

# Print the entire result dictionary
item = result.get('_embedded').get('item').get('uuid')
print(item)

# Assuming 'result' is the dictionary you provided

