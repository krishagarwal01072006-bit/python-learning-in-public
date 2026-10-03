# scope_demo.py
# Day 13 project: variables have a home.
# `secret` is created inside the function, so it exists
# only while the function runs. `name` outside the
# function is a different variable from the parameter
# named `name` inside it -- the call does not change it.
# Uncomment the last print to meet the NameError yourself.

def spell(name):
    secret = "xyz"
    return name + " spelled: " + secret

name = "krish"
print(spell(name))
print("outside, name is still:", name)

# print(secret)   # uncomment me -> NameError: name 'secret' is not defined
