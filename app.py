from flask import Flask
import requests

app = Flask(__name__)

URL = "https://ecampus.hmtm.de/campus/all/roomGroupsDay.asp?RWO_BUILDING=Standort+Luisenstra%C3%9Fe&from=publicrooms"

@app.route("/")
def home():
    try:
        response = requests.get(
            URL,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=30
        )

        return {
            "success": True,
            "status_code": response.status_code,
            "length": len(response.text),
            "preview": response.text[:2000]
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
