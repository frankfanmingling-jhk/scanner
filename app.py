from flask import Flask
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

URL = "https://ecampus.hmtm.de/campus/all/roomGroupsDay.asp?RWO_BUILDING=Standort+Luisenstra%C3%9Fe&from=publicrooms"

@app.route("/")
def home():

    response = requests.get(URL, timeout=60)

    html = response.text

    soup = BeautifulSoup(html, "html.parser")

    tables = soup.find_all("table")

    result = []

    for i, table in enumerate(tables):

        rows = table.find_all("tr")

        result.append({
            "table_index": i,
            "rows": len(rows),
            "preview": table.get_text(strip=True)[:300]
        })

    return {
        "success": True,
        "tables": result
    }
