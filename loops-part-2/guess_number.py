# guess_number.py
# Day 7 project: the classic guessing game.
# A while loop keeps asking until you get it right, and break ends the game.
# Type a number and press Enter each time. The secret is 7 - go on, try!

secret = 7
tries = 0

print("I am thinking of a number between 1 and 10.")

while True:
    guess = int(input("Your guess: "))
    tries = tries + 1
    if guess == secret:
        print("Got it! That took you", tries, "tries.")
        break
    if guess < secret:
        print("Too low. Aim higher.")
    else:
        print("Too high. Aim lower.")
