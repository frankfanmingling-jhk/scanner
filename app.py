from flask import Flask
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

URL = "https://ecampus.hmtm.de/campus/all/roomGroupsDay.asp?RWO_BUILDING=Standort+Luisenstra%C3%9Fe&from=publicrooms"

@app.route("/")
def home():

    response = requests.get(
        URL,
        timeout=60
    )

    html = response.text

    soup = BeautifulSoup(html, "html.parser")

    title = soup.title.text if soup.title else "No title"

    links = []

    for a in soup.find_all("a")[:20]:
        text = a.get_text(strip=True)

        if text:
            links.append(text)

    return {
        "success": True,
        "title": title,
        "sample_links": links
    }
