import aiohttp

async def login():
    # Step 1: Get XSRF token from cookie
    url_step1 = "http://localhost:8080/server/api/authn/status"
    headers_step1 = {"Content-Type": "application/x-www-form-urlencoded"}

    async with aiohttp.ClientSession() as session:
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

            # Step 3: Use Bearer token for authentication
            url_step3 = "http://localhost:8080/server/api/authn/status"
            headers_step3 = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": bearer_token,
            }
            print("Bearer token",bearer_token)

        async with session.get(url_step3, headers=headers_step3) as response_step3:
            # Print the response for Step 3
            return await response_step3.text()
        


# import asyncio
# result = asyncio.run(login())
# print(result)
