import aiohttp
import asyncio
import json
from .config import DSPACE_PORT, DSPACE_DOMAIN
import os

async def addBitstreamsItem(bundleId, file_path="files", filename="file.pdf",contentType ="pdf"):
    
    script_dir = os.path.dirname(os.path.abspath(__file__))

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
        async with session.patch(url_step1) as response_step3:
            # Print the response for Step 3
            xsrf_cookie_step3 = response_step3.cookies.get("DSPACE-XSRF-COOKIE").value

         # Step 4: Upload a file to a specific bundle
        url_step4 = f"{DSPACE_DOMAIN}:{DSPACE_PORT}/server/api/core/bundles/{bundleId}/bitstreams"

        headers_step4 = {
            "Authorization": bearer_token,
            "X-XSRF-TOKEN": xsrf_cookie_step3,
        }

        # Construct the full path to 'file.pdf'
        file_path = os.path.join(script_dir, f"{filename}")

        # Create multipart form data
        form_data = aiohttp.FormData()

        # Add file field with correct filename
        form_data.add_field('file', open(file_path, 'rb'), filename=f"{filename}", content_type=f"application/{contentType}")

        # Add properties as a JSON field
        properties = {
            "name": f"{filename}",
            "metadata": {
                "dc.description": [
                    {
                        "value": "example file",
                        "language": None,
                        "authority": None,
                        "confidence": -1,
                        "place": 0
                    }
                ]
            },
            "bundleName": "ORIGINAL"
        }

        form_data.add_field('properties', json.dumps(properties), content_type='application/json')

        # Make the POST request with multipart/form-data
        async with session.post(url_step4, headers=headers_step4, data=form_data) as response_step4:
            # Print the response for Step 4
            return await response_step4.text()

# Run the asynchronous event loop
# result = asyncio.run(updateItemTitle())
# print(result)
