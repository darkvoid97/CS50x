from cs50 import get_float

# Ask for the change, and keep asking until it receives a valid input
change = -1
while change < 0:
    change = get_float("Change: ")
# Floating numbers are always a problem to calculate with (because of base 2 computer approximations), so I'm better off translating the dollars value
# to number of cents
change = int(round(change * 100))

# Variable to start counting the number of coins needed to the change owed
coins = 0

# Check for bigger coins first, until the cents reach 0
while change > 0:
    if change >= 25:
        coins += 1
        change -= 25
    elif change >= 10:
        coins += 1
        change -= 10
    elif change >= 5:
        coins += 1
        change -= 5
    elif change >= 1:
        coins += 1
        change -= 1

print(coins)
