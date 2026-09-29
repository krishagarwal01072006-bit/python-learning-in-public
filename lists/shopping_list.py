# shopping_list.py
# Day 9 project: build a shopping list, then pop off what you bought.
# Type items one at a time. Type "done" when you stop adding.
# Then type one thing you bought and pop() takes it off the list.

items = []

while True:
    item = input("Add an item (or 'done'): ")
    if item == "done":
        break
    items.append(item)

print("Your list:", items)

bought = input("What did you buy first? ")
index = 0
for thing in items:
    if thing == bought:
        items.pop(index)
        break
    index = index + 1

print("Still to buy:", items)
