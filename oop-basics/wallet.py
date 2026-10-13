# Day 23: methods + attributes
# A Wallet keeps its balance inside the object. deposit() and
# spend() are methods, so every operation goes through them.
# The spend method refuses to let you go below zero.

class Wallet:
    def __init__(self, balance):
        self.balance = balance

    def deposit(self, amount):
        self.balance = self.balance + amount
        print("Deposited", amount, "- balance:", self.balance)

    def spend(self, amount):
        if amount > self.balance:
            print("Not enough money. Balance:", self.balance)
            return
        self.balance = self.balance - amount
        print("Spent", amount, "- balance:", self.balance)

w = Wallet(500)
w.deposit(200)
w.spend(int(input("How much to spend? ")))
w.spend(int(input("Spend again? ")))
