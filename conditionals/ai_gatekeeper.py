# ai_gatekeeper.py
# Day 3 project: the gatekeeper only lets the right people in.
# Change age and has_ticket, then rerun to test every branch.

age = 19
has_ticket = True

if age >= 18 and has_ticket:
    print("Welcome in! You may pass.")
elif age >= 18:
    print("Old enough, but you need a ticket.")
else:
    print("Too young — come back later.")

print("and needs EVERY part true. or needs just one.")
