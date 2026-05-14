from flask import Flask
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

URL = "https://ecampus.hmtm.de/campus/all/roomGroupsDay.asp?room=L%20018&oid=341&gguid=0xCD7890D53F0B4C4BAF813E12FB1A8DA6&mode=all&from=&tguid=0xAF6933CCA3E6504089248488B6F1AC0D"

@app.route("/")
def home():

    response = requests.get(
        URL,
        timeout=60
    )

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    tables = soup.find_all("table")

    result = []

    for i, table in enumerate(tables):

        rows = table.find_all("tr")

        result.append({
            "table": i,
            "rows": len(rows),
            "preview": table.get_text(strip=True)[:500]
        })

    return {
        "success": True,
        "tables": result
    }
