# truthiness_lab.py
# Day 3 project: truthiness in action.
# Empty things are falsy. Almost everything else is truthy.

name = "krish"
if name:
    print("name is truthy")

empty_text = ""
if empty_text:
    print("this never prints")
else:
    print("empty string is falsy")

scores = []
if scores:
    print("this never prints")
else:
    print("empty list is falsy")

weird = [0]
if weird:
    print("[0] is truthy — the list is not empty!")
