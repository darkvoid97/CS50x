from cs50 import get_string
import re

text = get_string("Text: ")

# Count every alphabetic character (letter) in the string
letters = sum(1 for char in text if char.isalpha())

# Count every word contained in the string, meaning we'll count the whitespaces between the words
words = len(text.split())

# Count every sentence contained in the string, meaning we'll check for how many punctuations in the text
sentences = len(re.findall("[^.!?]+[.!?]", text))

# Compute the Coleman-Liau index
index = int(round(0.0588 * (letters / words * 100) - 0.296 * (sentences / words * 100) - 15.8))

# Assign the grade by evaluating the index and print it
print("Before Grade 1" if index < 1 else f"Grade {index}" if index <= 16 else "Grade 16+")

# Man, I love Python so much, so many fewer lines than the C version
