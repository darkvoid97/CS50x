from cs50 import get_int
import re

# String used to print what type of card after doing the checks
type = ""

# Ask for the credit card number and keep asking until we get a valid input
card = -1
while card < 0:
    card = get_int("I'm once again asking for your credit card information: ")

# Any valid credit card number has either 13, 15, or 16 digits
# Also, any valid credit card number starts with one of the following cases: '4'; '51'-'55' range; either '34' or '37';
if any(digits == len(str(card)) for digits in [13, 15, 16]):
    if bool(re.match("^4|^5[1-5]|^(34|37)", str(card))):
        # If the number passes these two checks, then it's worth to start computing the Luhn algorithm
        sum = 0
        # card[::-1] reverses the string, making it easier to code the algorithm
        # The enumerate function allows me to access both the index and the char related to it
        for index, digit in enumerate(str(card)[::-1]):
            number = int(digit)
            # Take any second digit from the left and do the Luhn thingy
            if index % 2 == 1:
                number *= 2
                if number > 9:
                    # This is basically the same as summing the single digits of the eventual double-digits number, in this case
                    number -= 9

            sum += number

        # Card is invalid if the sum's last digit isn't 0, aka, sum modulo 10 isn't 0
        if sum % 10 != 0:
            type = "INVALID"
        # Check for VISA card requirements (card number has either 13 or 16 digits, and starts with '4')
        elif any(digits == len(str(card)) for digits in [13, 16]) and str(card).startswith("4"):
            type = "VISA"
        # Check for MASTERCARD card requirements (card number has 16 digits, and starts with '51'-'55' range)
        elif len(str(card)) == 16 and bool(re.match("^5[1-5]", str(card))):
            type = "MASTERCARD"
        # Check for AMEX card requirements (card number has 15 digits, and starts with either '34' or '37')
        elif len(str(card)) == 15 and str(card).startswith(("34", "37")):
            type = "AMEX"
        # Just in case the sum's last digit is 0 but none of the checks passes
        else:
            type = "INVALID"

    else:
        type = "INVALID"

else:
    type = "INVALID"

print(type)
