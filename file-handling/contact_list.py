# Day 19: JSON
# A tiny phonebook that survives between runs. Contacts are kept
# as a list of dicts in contacts.json. Run it twice: contacts
# from the first run are still there the second time. If the
# file does not exist yet, FileNotFoundError is caught and we
# start with an empty list (Day 17's exceptions, back to help).

import json

try:
    with open("contacts.json") as f:
        contacts = json.load(f)
except FileNotFoundError:
    contacts = []

name = input("Name: ")
phone = input("Phone: ")
contacts.append({"name": name, "phone": phone})

with open("contacts.json", "w") as f:
    json.dump(contacts, f)

print("Saved. All contacts:")
for c in contacts:
    print(c["name"], "-", c["phone"])
