from flask import Flask, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def home():

    room = request.args.get("room", "L018")

    url = f"https://ecampus.hmtm.de/campus/all/roomGroupsDay.asp?room={room}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=30
        )

        soup = BeautifulSoup(response.text, "html.parser")

        tables = soup.find_all("table")

        if len(tables) < 3:
            return {
                "success": False,
                "error": "No timetable found"
            }

        timetable = tables[2]

        rows = timetable.find_all("tr")

        if len(rows) < 2:
            return {
                "success": False,
                "error": "No rows found"
            }

        schedule = []

        for row in rows[1:]:

            cells = row.find_all("td")

            if len(cells) < 2:
                continue

            time_text = cells[0].get_text(" ", strip=True)

            room_cell = cells[1]

            room_text = room_cell.get_text(" ", strip=True)

            room_text = room_text.replace("\n", " ").strip()

            if room_text == "":
                status = "FREE"
            else:
                status = "BUSY"

            schedule.append({
                "time": time_text,
                "status": status,
                "detail": room_text
            })

        return {
            "success": True,
            "room": room,
            "schedule": schedule
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
