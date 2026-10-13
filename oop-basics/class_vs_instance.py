# Day 23: class attributes vs instance attributes
# interest_rate lives on the CLASS, so every Bank account shares it.
# balance lives on each INSTANCE, so each account keeps its own.
# Run it, then change Bank.interest_rate to 0.10 at the top and
# rerun: both balances jump, because the rate is shared.

class Bank:
    interest_rate = 0.05  # shared by all accounts

    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def add_interest(self):
        self.balance = self.balance + self.balance * Bank.interest_rate

a1 = Bank("krish", 1000)
a2 = Bank("zara", 2000)
a1.add_interest()
a2.add_interest()

print("Class rate:", Bank.interest_rate)
print(a1.owner, "balance:", a1.balance)
print(a2.owner, "balance:", a2.balance)
