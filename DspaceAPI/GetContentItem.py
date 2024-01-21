import aiohttp
import asyncio
import json
import os
from .config import DSPACE_PORT, DSPACE_DOMAIN

async def downloadItemContent(bitstreamId, bitstreamName, filePath=""):
    # JWT token
    async with aiohttp.ClientSession() as session:
        # Step 1: Get XSRF token from cookie
        url_step1 = f"{DSPACE_DOMAIN}:{DSPACE_PORT}/server/api/authn/status"
        headers_step1 = {"Content-Type": "application/x-www-form-urlencoded"}

        async with session.get(url_step1, headers=headers_step1) as response_step1:
            xsrf_cookie = response_step1.cookies.get("DSPACE-XSRF-COOKIE").value

            # Step 2: Login and obtain Bearer token
            url_step2 = f"{DSPACE_DOMAIN}:{DSPACE_PORT}/server/api/authn/login"
            headers_step2 = {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-XSRF-TOKEN": xsrf_cookie,
            }
            params_step2 = {"user": "test@test.edu", "password": "admin"}

        async with session.post(
            url_step2, headers=headers_step2, data=params_step2
        ) as response_step2:
            bearer_token = response_step2.headers.get("Authorization")
            xsrf_cookie = response_step2.cookies.get("DSPACE-XSRF-COOKIE").value

            # Step 3: Access a new API endpoint to get specific XSRF token
            url_step3 = f"{DSPACE_DOMAIN}:{DSPACE_PORT}/server/api/core/items"
            headers_step3 = {}
            data_step3 = {}

        async with session.patch(
            url_step3, headers=headers_step3, data=json.dumps(data_step3)
        ) as response_step3:
            # Print the response for Step 3
            xsrf_cookie_step3 = response_step3.cookies.get("DSPACE-XSRF-COOKIE").value

            # Step 4: Another API endpoint using XSRF cookie from Step 3
            url_step4 = f"{DSPACE_DOMAIN}:{DSPACE_PORT}/server/api/core/bitstreams/{bitstreamId}/content"
            headers_step4 = {
                "Content-Type": "application/json",
                "Authorization": bearer_token,
                "X-XSRF-TOKEN": xsrf_cookie_step3,  # Use XSRF cookie from Step 3
            }

            async with session.get(url_step4, headers=headers_step4) as response_step4:
                # You can access the content and headers as needed
                if response_step4.status == 200:
                    # Read the binary content
                    content = await response_step4.read()
                    
                    # Check if the file already exists
                    counter = 0
                    while os.path.exists(bitstreamName):
                        bitstreamName = bitstreamName.split('(')[0]
                        counter += 1
                        bitstreamName = f"{bitstreamName.split('.')[0]}({counter}).pdf"
                        
                    # Save the content to a PDF file
                    with open(f"{filePath}{bitstreamName}", "wb") as file:
                        file.write(content)
                        
                        result = {}
        
                        result["msg"] = response_step4.status
                        result["response"] = ""
                    
                return result
# Run the asynchronous event loop
# result = asyncio.run(downloadItemContent())
# print(result)
