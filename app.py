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

    if len(tables) < 2:
        return {
            "success": False,
            "error": "No timetable found"
        }

    timetable = tables[1]

    rows = timetable.find_all("tr")

    if len(rows) < 3:
        return {
            "success": False,
            "error": "No rows found"
        }

    headers = rows[1].find_all(["td", "th"])

    room_names = []

    for h in headers[1:]:
        room_names.append(h.get_text(strip=True))

    free_rooms = []

    target_row = None

    for row in rows:

        cols = row.find_all("td")

        if not cols:
            continue

        time_text = cols[0].get_text(strip=True)

        if "11:00" in time_text:
            target_row = cols
            break

    if not target_row:
        return {
            "success": False,
            "error": "Time row not found"
        }

    for i, cell in enumerate(target_row[1:]):

        text = cell.get_text(strip=True)

        if text == "":
            free_rooms.append(room_names[i])

    return {
        "success": True,
        "time": "11:00",
        "free_rooms_count": len(free_rooms),
        "free_rooms": free_rooms[:100]
    }            if texts:
                result.append(texts)

    return {
        "success": True,
        "title": title,
        "tables_found": len(tables),
        "preview": result
    }
