# I only need the get_int() function from the library, it saves me from having to type the library name before the function
from cs50 import get_int

# Ask for the height, and keep asking until it receives a number between 1 and 8
height = 0
while height < 1 or height > 8:
    height = get_int("Input a number between 1 and 8, inclusive, to build the Mario pyramid: ")

# Loop through the rows and columns to print the pyramid
for i in range(1, height + 1):
    for j in range(1, height + 1):
        # Aura farming section: because I love using less lines of code. If you can't read this line properly, skill issue bro
        print("#" if j > (height - i) else " ", end="")
    # At the end of the row, print to go to a new line
    print()
