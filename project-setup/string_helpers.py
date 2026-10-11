# Day 21: modules
# A tiny helper module. The functions here get imported and used
# in main.py. Real Python projects are organized exactly like this:
# helpers live in one file, the program in another.

def greet(name):
    return "Hello " + name

def double(n):
    return n * 2
