# contact_book.py
# Day 11 project: a tiny phone book.
# Dict keys are names, values are numbers. .get() with a
# default gives a friendly message for missing names
# instead of a KeyError crash.

contacts = {
    "ria": "98100-12345",
    "dev": "98200-54321",
    "ana": "98300-98765",
}

name = input("Whose number do you want? ").lower()
print(name, "->", contacts.get(name, "not in my contacts, sorry!"))
