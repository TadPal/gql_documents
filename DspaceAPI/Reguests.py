import asyncio
from .Authnentication import login
from .UpdateItemTitle import updateItemTitle

login = asyncio.run(login())
updateItemTitle = asyncio.run(updateItemTitle())

