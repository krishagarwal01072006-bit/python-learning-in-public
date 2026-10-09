# Day 19: JSON
# Saves a tiny model config dict to config.json, then loads it
# back and prints each setting. This is how real AI configs are
# stored: Hugging Face checkpoints ship with a config.json.

import json

config = {"model": "bert", "epochs": 5, "learning_rate": 0.01}

with open("config.json", "w") as f:
    json.dump(config, f)

with open("config.json") as f:
    loaded = json.load(f)

print("model:", loaded["model"])
print("epochs:", loaded["epochs"])
print("learning_rate:", loaded["learning_rate"])
