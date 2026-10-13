# Day 23: classes
# A Student is one object holding a name and a study streak.
# Methods are functions that live inside the class and take
# self as their first argument.

class Student:
    def __init__(self, name):
        self.name = name
        self.streak = 0

    def study(self):
        self.streak = self.streak + 1
        print(self.name, "studied. Streak:", self.streak)

name = input("Your name: ")
s = Student(name)

days = int(input("Days studied this week: "))
for i in range(days):
    s.study()

print("Final streak:", s.streak)
