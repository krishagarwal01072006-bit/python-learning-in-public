# Day 17: exceptions
# Two functions calling each other. parse_config crashes with a
# ValueError, and the try/except catches it. Delete the try/except
# and rerun: Python prints the full traceback. Read it bottom-up.
# The last line is the error; the lines above show the calls that
# led to it, newest at the bottom.

def parse_config(name):
    return int(name)

def load_model(name):
    return parse_config(name)

try:
    load_model("bert-base")
except ValueError:
    print("Caught a ValueError. The model name was not a number.")
