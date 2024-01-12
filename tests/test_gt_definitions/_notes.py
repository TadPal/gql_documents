

# @pytest.fixture
# def RSAKeys():
#     from cryptography.hazmat.primitives.asymmetric import rsa
#     from cryptography.hazmat.primitives import serialization

#     key = rsa.generate_private_key(
#         public_exponent=65537,
#         key_size=2048
#     )

#     pem_private_key = encrypted_pem_private_key = key.private_bytes(
#         encoding=serialization.Encoding.PEM,
#         format=serialization.PrivateFormat.TraditionalOpenSSL,
#         encryption_algorithm=serialization.NoEncryption()
#     )

#     pem_public_key = key.public_key().public_bytes(
#     encoding=serialization.Encoding.PEM,
#     format=serialization.PublicFormat.SubjectPublicKeyInfo
#     )
#     return (pem_private_key, pem_public_key)

# @pytest.fixture
# def JWTSigner(RSAKeys):
#     (pem_private_key, _) = RSAKeys
#     import jwt
#     def asJWT(data={}):
#         result = jwt.encode(data, pem_private_key, algorithm="RS256")
#         return result
#     return asJWT

# @pytest.fixture
# def OAuthport():
#     port = 8125
#     return port

# @pytest.fixture
# def Set_JWTRESOLVEUSERPATH(monkeypatch):
#     port = 8125
#     monkeypatch.setenv("JWTRESOLVEUSERPATH", f"http://localhost:{port}/publickey")
#     return port


# @pytest.fixture
# def Set_JWTPUBLICKEY(monkeypatch, RSAKeys):
#     port = 8126
#     monkeypatch.setenv("JWTRESOLVEUSERPATH", f"http://localhost:{port}/publickey")
#     return port

# @pytest.fixture
# def FastApiApp():
#     import fastapi
#     app = fastapi.FastAPI()


# def createFastApiApp(path, method="get", executor=None):
#     import fastapi
#     app = fastapi.FastAPI()

#     decoratorFunc = getattr(app, method, None)
#     assert decoratorFunc is not None, f"method {method} not found on fastapi app"
#     decorated = decoratorFunc(path)(executor)

# def runU(app, port):
#     uvicorn.run(app, port=port)

# def runFastApi(app, port):
#     from multiprocessing import Process
    
#     _api_process = Process(target=runU, daemon=True, kwargs={"app": app, "port": port})
#     _api_process.start()
#     print(f"Server started at {port}")
#     logging.info(f"Server started at {port}")
#     yield _api_process
#     _api_process.terminate()
#     _api_process.join()
#     print(f"Server stopped at {port}")
#     logging.info(f"Server stopped at {port}")

# @pytest.fixture
# def OAuthServer(OAuthport, RSAKeys):
#     from mockoauthserver import server as OAuthServer
#     app = OAuthServer.createServer()    
#     runFastApi(app, OAuthport)


# @pytest_asyncio.fixture
# async def AccessToken(OAuthport, OAuthServer, LoggedUser):
#     import aiohttp 
#     userDict = LoggedUser
#     # keyurl = f"http://localhost:{OAuthport}/publickey"
#     loginurl = f"http://localhost:{OAuthport}/login3"
#     async with aiohttp.ClientSession() as session:
#         async with session.get(loginurl) as resp:
#             assert resp.status == 200
#             accessjson = await resp.json()
#         payload = {
#             "username": userDict["email"],
#             "password": "IDontCare"
#         }
#         async with session.post(loginurl, json=payload) as resp:
#             assert resp.status == 200
#             tokendict = await resp.json()
            
#     return tokendict["token"]

