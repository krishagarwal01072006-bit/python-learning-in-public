# truthiness_lab.py
# Day 3 project: learn truthiness by poking it.
# Empty things ('', [], {}, 0, None) are falsy. Almost everything else
# is truthy — including [0], which trips up EVERY beginner.

def ask(prompt):
    """Ask a question; return None if stdin runs out (EOF)."""
    try:
        return input(prompt)
    except EOFError:
        print()
        return None

def verdict(thing):
    state = "truthy ✅" if thing else "falsy ❌"
    print(f"  {thing!r:>14} -> {state}")

print("Truthiness lab — guess before you peek!\n")

demo = ["", "hello", [], [0], 0, 1, -3.14, None, False, True, {}]
for thing in demo:
    verdict(thing)

print("\nNow you try. Type one of: 0, '', [], [0], none, false, hello")
print("(or press Enter to quit)")

mapping = {
    "0": 0, "zero": 0,
    "''": "", "empty string": "",
    "[]": [], "empty list": [],
    "{}": {}, "empty dict": {},
    "none": None, "false": False, "true": True,
    "[0]": [0], "hello": "hello",
}

while True:
    raw = ask("Your value > ")
    if raw is None or raw.strip() == "":
        print("Lab closed. Go write some ifs! 👋")
        break
    key = raw.strip().lower()
    if key in mapping:
        verdict(mapping[key])
    else:
        print(f"  {raw!r:>14} -> truthy ✅ (any non-empty text counts)")
