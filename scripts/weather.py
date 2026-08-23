#!/usr/bin/env python
import json
import os
import sys

import requests

CACHE = os.path.expanduser("~/.config/waybar/cache/weather.json")
URL = (
    "http://api.weatherapi.com/v1/current.json"
    "?key=d8d8aa1927c941a0834142846250904&q=kolkata&aqi=yes"
)

RAIN = {
    1063, 1072, 1087, 1150, 1153, 1168, 1171,
    1180, 1183, 1186, 1189, 1192, 1195, 1198, 1201,
    1240, 1243, 1246, 1273, 1276, 1279, 1282,
}
SNOW = {1210, 1213, 1216, 1219, 1222, 1225, 1237, 1255, 1258}


def load_cache():
    try:
        with open(CACHE) as f:
            return json.load(f)
    except Exception:
        return None


def fetch():
    try:
        resp = requests.get(URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        with open(CACHE, "w") as f:
            json.dump(data, f)
        return data
    except Exception:
        return None


def pick_icon(code, is_day):
    if code == 1000:
        return "" if is_day else ""
    if code in (1003, 1006):
        return ""
    if code in (1009, 1030, 1135, 1147):
        return ""
    if code in RAIN:
        return "🌧 "
    if code in SNOW:
        return "❄ "
    return "" if is_day else ""


data = fetch() or load_cache()
if not data:
    print(json.dumps({"text": " weather unavailable", "class": "error"}))
    sys.exit(0)

cur = data["current"]
loc = data["location"]
is_day = cur.get("is_day", 1) == 1
code = cur["condition"]["code"]
precip = cur.get("precip_mm", 0) or 0

text = f"{pick_icon(code, is_day)} {round(cur['temp_c'])}°C  {loc['name']}"
tooltip = "\n".join([
    f"{loc['name']}, {loc['region']}",
    "",
    f"{cur['condition']['text']}",
    f"feels like : {round(cur['feelslike_c'])}°C",
    f"humidity   : {cur['humidity']}%",
    f"rain       : {precip} mm",
    f"cloud      : {cur['cloud']}%",
    "",
    f"updated : {cur['last_updated']}",
])

rainy = precip > 0 or code in RAIN
cls = "rainy" if rainy else ("day" if is_day else "night")
print(json.dumps({"text": text, "tooltip": tooltip, "class": cls}))
