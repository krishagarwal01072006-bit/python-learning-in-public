# Day 21: modules
# The program lives here. The helpers live in string_helpers.py.
# import the module, then call its functions with the module name
# in front. main.py + string_helpers.py is the smallest real project.

import string_helpers

name = input("Your name: ")
print(string_helpers.greet(name))

num = int(input("A number: "))
print("Doubled:", string_helpers.double(num))
