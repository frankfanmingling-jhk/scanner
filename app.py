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

    timetable = tables[2]

    rows = timetable.find_all("tr")

    # 第二行是房间名
    header_cells = rows[1].find_all(["td", "th"])

    room_names = []

    for cell in header_cells[1:]:
        room_names.append(
            cell.get_text(strip=True)
        )

    target_row = None

    # 找11点这一行
    for row in rows:

        cols = row.find_all("td")

        if not cols:
            continue

        first = cols[0].get_text(strip=True)

        if first.startswith("11:00"):
            target_row = cols
            break

    if not target_row:
        return {
            "success": False,
            "error": "11:00 row not found"
        }

    free_rooms = []

    for i, cell in enumerate(target_row[1:]):

        text = cell.get_text(strip=True)

        # 空字符串 = 空闲
        if text == "":

            if i < len(room_names):

                room = room_names[i]

                # 只保留L楼琴房
                if room.startswith("L"):

                    free_rooms.append(room)

    return {
        "success": True,
        "time": "11:00",
        "free_rooms_count": len(free_rooms),
        "free_rooms": free_rooms
    }
