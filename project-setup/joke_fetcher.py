# Day 21: requests + venv
# Fetches a random joke from a free JSON API and prints it.
# Before running: python3 -m venv myenv, activate it, then
# pip install requests inside the venv. Installing requests
# in the venv instead of globally is the whole point of this day.

import requests

try:
    response = requests.get(
        "https://official-joke-api.appspot.com/random_joke", timeout=10
    )
    joke = response.json()
    print(joke["setup"])
    print(joke["punchline"])
except Exception as e:
    print("Something went wrong:", e)
