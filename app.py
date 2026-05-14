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

    tables = soup.find_all("table")

    result = []

    for table in tables[:5]:

        rows = table.find_all("tr")

        for row in rows[:10]:

            cols = row.find_all(["td", "th"])

            texts = [c.get_text(strip=True) for c in cols]

            if texts:
                result.append(texts)

    return {
        "success": True,
        "title": title,
        "tables_found": len(tables),
        "preview": result
    }
