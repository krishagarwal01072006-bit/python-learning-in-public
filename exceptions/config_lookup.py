# Day 17: exceptions
# Look up a setting in a model config. Ask for a key that is not
# there (try batch_size) and the KeyError path runs instead of
# a crash.

config = {"model": "bert", "epochs": 5}

key = input("Which setting? (model / epochs / batch_size): ")

try:
    print(key, "=", config[key])
except KeyError:
    print(key, "is not in the config. Known settings: model, epochs")
