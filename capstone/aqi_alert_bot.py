# Day 25 capstone: Delhi AQI Alert Bot
# The flagship project. Everything so far in one program:
# requests (Day 21) fetches live AQI, try/except (Day 17) guards the
# network calls, JSON (Day 19) gets parsed from the API, the whole
# thing is a class (Day 23), and every check is appended to a log
# file (Day 19). Telegram pings you when the air crosses your threshold.
#
# Needs: pip install requests
# Get a free WAQI token at https://aqicn.org/data-platform/token/
# Make a Telegram bot with @BotFather, then send /start to your bot.
# Your tokens are typed in when you run this. They are never saved.
#
# Scheduling: run it by hand each morning, or give it a cron job on
# your own machine so it checks every hour while you sleep.
#   0 * * * * cd ~/python-learning-in-public/capstone && python3 aqi_alert_bot.py

import requests
from datetime import datetime

WAQI_URL = "https://api.waqi.info/feed/delhi/?token="
TELEGRAM_URL = "https://api.telegram.org/bot"


class AQIAlertBot:
    def __init__(self, waqi_token, bot_token, chat_id, threshold):
        self.waqi_token = waqi_token
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.threshold = threshold

    def fetch_aqi(self):
        # Returns (aqi number, main pollutant) or (None, None) if anything breaks.
        try:
            response = requests.get(WAQI_URL + self.waqi_token, timeout=10)
            data = response.json()
        except Exception as error:
            print("Network problem, could not reach the AQI API:", error)
            return None, None
        if data.get("status") != "ok":
            print("AQI API said no. Check your token.")
            return None, None
        aqi = data["data"]["aqi"]
        pollutant = data["data"]["dominentpol"]
        return aqi, pollutant

    def label(self, aqi):
        if aqi <= 50:
            return "Good"
        if aqi <= 100:
            return "Moderate"
        if aqi <= 200:
            return "Poor"
        if aqi <= 300:
            return "Very Poor"
        return "Severe"

    def log(self, aqi, pollutant):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        line = now + " | AQI " + str(aqi) + " (" + self.label(aqi) + ") | " + pollutant
        with open("aqi_log.txt", "a") as f:
            f.write(line + "\n")
        print("Logged:", line)

    def send_telegram(self, message):
        url = TELEGRAM_URL + self.bot_token + "/sendMessage"
        try:
            r = requests.get(url, params={"chat_id": self.chat_id, "text": message}, timeout=10)
            if r.status_code == 200:
                print("Telegram alert sent.")
            else:
                print("Telegram said no. Check your bot token and chat id.")
        except Exception as error:
            print("Could not reach Telegram:", error)

    def check(self):
        aqi, pollutant = self.fetch_aqi()
        if aqi is None:
            return
        print("Delhi AQI right now:", aqi, "(" + self.label(aqi) + "), main pollutant:", pollutant)
        self.log(aqi, pollutant)
        if aqi > self.threshold:
            message = "Air alert: Delhi AQI is " + str(aqi) + " (" + self.label(aqi) + "). Stay inside."
            print(message)
            self.send_telegram(message)
        else:
            print("Under your threshold. No alert needed.")


waqi_token = input("WAQI API token: ")
bot_token = input("Telegram bot token: ")
chat_id = input("Telegram chat id: ")
threshold = int(input("Alert me when AQI is above: "))

bot = AQIAlertBot(waqi_token, bot_token, chat_id, threshold)
bot.check()
