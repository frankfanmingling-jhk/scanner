from flask import Flask
from playwright.sync_api import sync_playwright

app = Flask(__name__)

URL = "https://ecampus.hmtm.de/campus/all/roomGroupsDay.asp?RWO_BUILDING=Standort+Luisenstra%C3%9Fe&from=publicrooms"

@app.route("/")
def home():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            page = browser.new_page()

            page.goto(URL, timeout=60000)

            html = page.content()

            browser.close()

            return {
                "success": True,
                "length": len(html),
                "preview": html[:2000]
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
