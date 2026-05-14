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

    timetable = tables[2]

    rows = timetable.find_all("tr")

    result = []

    for row in rows:

        cols = row.find_all("td")

        if len(cols) < 2:
            continue

        time_text = cols[0].get_text(strip=True)

        status_text = cols[1].get_text(strip=True)

        if status_text == "":
            status = "FREE"
        else:
            status = "BUSY"

        result.append({
            "time": time_text,
            "status": status,
            "detail": status_text
        })

    return {
        "success": True,
        "room": "L018",
        "schedule": result
    }
