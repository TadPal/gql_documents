import aiohttp
import asyncio
import json

async def getItem(itemsId):
   
    language = "English_US"
    
    #JWT token
    async with aiohttp.ClientSession() as session:
        # Step 1: Get XSRF token from cookie
        url_step1 = "http://localhost:8080/server/api/authn/status"
        headers_step1 = {"Content-Type": "application/x-www-form-urlencoded"}

        async with session.get(url_step1, headers=headers_step1) as response_step1:
            xsrf_cookie = response_step1.cookies.get("DSPACE-XSRF-COOKIE").value

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

            # Step 3: Access a new API endpoint to get specific XSRF token
            url_step3 = "http://localhost:8080/server/api/core/items/"+f"{itemsId}"
            headers_step3 = {
                "Content-Type": "application/json",
                "Authorization": bearer_token,
                "X-XSRF-TOKEN": xsrf_cookie,  # Use XSRF cookie from Step 3
            }

        async with session.get(url_step3, headers=headers_step3) as response_step3:
            
            return await response_step3.json()
        
# Run the asynchronous event loop

# result = asyncio.run(addItemTitle())
# print(result)
