# Delhi AQI Alert Bot — Day 25 capstone

The flagship project of my Python learning-in-public series. Everything from
Days 1–23 in one program that actually runs against the real world.

## What it does

Checks Delhi's live air quality and pings you on Telegram when the AQI crosses
your threshold. Every reading gets appended to a local log file, so you build
a personal air-quality history over time.

## How it works

- `requests` (Day 21) fetches live AQI from the WAQI API
- `try/except` (Day 17) guards the network calls — if the API is down, it says so instead of crashing
- JSON (Day 19) is parsed from the API response
- A class (Day 23) wraps the whole bot; file logging (Day 19) keeps the history
- Telegram alerts fire when the AQI crosses the threshold you set at startup

## Run it

1. `pip install requests`
2. Free WAQI token at https://aqicn.org/data-platform/token/
3. Make a Telegram bot with @BotFather, then send `/start` to your bot
4. `python3 aqi_alert_bot.py` — tokens are typed at runtime, never saved

Schedule it with cron to check hourly while you sleep:

```
0 * * * * cd ~/python-learning-in-public/capstone && python3 aqi_alert_bot.py
```

October air in Delhi is routinely "Poor" (AQI 150–200+) — on those days this bot
is the one project on my profile that isn't a demo.
