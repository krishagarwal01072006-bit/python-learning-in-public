# config_demo.py
# Day 11 project: the two dict gotchas that got me.
# 1. Indexing a missing key = KeyError crash. .get() with a
#    default keeps the script alive.
# 2. List keys are illegal. Keys must be unchangeable, so the
#    offending line below stays commented out: uncomment it
#    and you get "TypeError: unhashable type: 'list'".
# Change the values at the top and rerun.

config = {"theme": "dark", "volume": 7}

print("theme:", config["theme"])
print("brightness:", config.get("brightness", "not set, using default"))

# config[["a", "b"]] = "nope"   # uncomment me -> TypeError: unhashable type: 'list'
# Keys must be unchangeable: strings, numbers, tuples. Lists never.
