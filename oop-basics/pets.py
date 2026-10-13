# Day 23: inheritance
# class Dog(Pet) means: a Dog IS a Pet, plus its own tricks.
# Dog gets name, legs and describe() for free from Pet.
# Try it: add class Cat(Pet) with a meow() method.

class Pet:
    def __init__(self, name):
        self.name = name
        self.legs = 4

    def describe(self):
        print(self.name, "has", self.legs, "legs")

class Dog(Pet):
    def bark(self):
        print(self.name, "says woof")

d = Dog("Tommy")
d.describe()
d.bark()
