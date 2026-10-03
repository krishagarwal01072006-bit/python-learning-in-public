# greet_machine.py
# Day 13 project: default arguments.
# greeting has a default value ("hello"), so it can be
# left out of the call. Defaults always go last in the
# def line, after the plain parameters.
# Type your name when asked, then run it a second time
# with your favourite greeting.

def greet(name, greeting="hello"):
    print(greeting + ",", name)

my_name = input("Your name: ")
greet(my_name)
greet(my_name, "namaste")
