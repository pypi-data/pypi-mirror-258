from aiohttp import ClientSession as Session
from colorpicker_rs import get_dominant_color
from asyncio import run
from time import time
async def r():
    url = "https://cdn.discordapp.com/embed/avatars/0.png"
#    url = "https://cdn.discordapp.com/avatars/1109861649910874274/946588e6d2e8ea2d46ec6e89eb466321.png?size=1024"
#    async with Session() as session:
 #       async with session.get(url) as req:
  #          b = await req.read()
    start = time()
    dom = get_dominant_color(url)
    print(time()-start)
    print(dom)
    return dom

run(r())
