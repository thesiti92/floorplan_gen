from bs4 import BeautifulSoup
import json
import numpy as np
from PIL import Image
from io import BytesIO
import requests

prefix = "http://www.ultimateplans.com%s"

def get_links():
    soup = BeautifulSoup(open("index.html"), 'html5lib')
    json.dump([link['href'] for link in soup.find_all('a') if "FP-E" in link['href']], open("links.json", "w+"))
def fetch_images():
    links = json.load(open('links.json'))[:5000]
    return {Link.split("/")[-1].split("-")[0].split("_")[-1]: np.asarray(Image.open(BytesIO(requests.get(prefix % links[0]).content)).convert("L").resize((300,300))).tolist() for link in links}
if __name__ == "__main__":
    json.dump(fetch_images(), open("pictures.json", "w+"))
