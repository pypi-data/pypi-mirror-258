from PIL import Image
import requests, colorgram
from datetime import datetime
from xxhash import xxh3_64_hexdigest as hash
from io import BytesIO
from discord import Color

def req():
	start = datetime.now().timestamp()
	r = requests.get("https://cdn.discordapp.com/embed/avatars/0.png")
	resp = r.content
	image_hash = hash(resp)
#	start = datetime.now().timestamp()
	img = Image.open(BytesIO(resp))
	img.thumbnail((100, 100))
	colors = colorgram.extract(img, 1)
	color = Color.from_rgb(*colors[0].rgb).value
	return (datetime.now().timestamp()-start,hex(color))

print(req())
