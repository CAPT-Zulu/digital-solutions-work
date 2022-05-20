import random
filename = "TextFiles/quotes.txt"

file = open(filename)
# print(type(file))

contents = file.readlines()
print(type(contents))
print(len(contents))

quote = random.choice(contents).strip("\n")
print(quote)