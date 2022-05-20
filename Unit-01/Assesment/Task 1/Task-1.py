values = 1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1
roman = "M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"
numerals = ""
number = int(input("Enter a number between 1 and 3999: "))
if number in range(1,4000):
    for i in range(0,13):
        while number >= values[i]:
            number = number - values[i]
            numerals += roman[i]
else:
    print("Please choose a valid number between 1 and 3999")
print("numerals: " + numerals)