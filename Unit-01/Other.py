# grade = input("Enter your mark: ").strip()
# if grade.isdigit():
#     grade = int(grade)
#     if grade > 100:
#         print("That is not a valid grade")
#     else:
#         if grade >= 80: endgrade = 'A'
#         elif grade >= 70: endgrade = 'B'
#         elif grade >= 50: endgrade = 'C'
#         elif grade >= 30: endgrade = 'D'
#         else: endgrade = 'E'
#         print("Your grade is", endgrade)
# else:
#     print("Type a number not letters dumb-ass")

# --------------------------------------------------------------

# sold = input("Enter the amount sold: ").strip()
# if sold.isdigit():
#     sold = int(sold)
#     if sold >= 10000: percent = 10
#     elif sold >= 1: percent = 5
#
#     print("You get an", percent,"% commision and your final price is: " + "${:.2f}".format((sold * ((100 + percent)/100))))
# else:
#     print("Type a number not letters dumb-ass")

# --------------------------------------------------------------
# word = input("Enter the word: ").strip()
# wordhalf = len(word) // 2
# if (len(word) % 2) == 0:
#     print("(EVEN)", "First part of the word:", word[:int(wordhalf)], "Second part of the word:", word[int(wordhalf):], "Together is:", word[:int(wordhalf)], word[int(wordhalf):])
# else:
#     print("(ODD)", "The Middle character is:", word[int(wordhalf):int(wordhalf+1)])
# # --------------------------------------------------------------
# word = input("Enter the word: ").strip()
# wordhalf = len(word) // 2
# if (len(word) % 2) == 0: print("(EVEN)", word[:int(wordhalf)], word[int(wordhalf):])
# else: print("(ODD)", word[int(wordhalf):int(wordhalf+1)])
# --------------------------------------------------------------
# word = input("Enter the word: ").strip()
# firstletter = word[:-len(word) + 1]
# print(word[1:] + firstletter + "ay")
# --------------------------------------------------------------
# special_characters = "!@#$%^&*()-+?_=,<>/"
# special_characters2 = "1234567890"
# special_characters3 = "QWERTYUIOPASDFGHJKLZXCVBNM"
# special_characters4 = "qwertyuiopasdfghjklzxcvbnm"
# passed = 0
# passed2 = 0
#
# word = input("Enter the word: ").strip()
#
# if len(word) <= 5:
#     print("To short")
# else:
#     passed2 += 1
#
# if len(word) >= 25:
#     print("To long")
# else:
#     passed2 += 1
#
# if any(c in special_characters for c in word):
#     passed += 1
# else:
#     print("no spec")
#
# if any(c in special_characters2 for c in word):
#     passed += 1
# else: print("no numb")
#
# if any(c in special_characters3 for c in word):
#     passed += 1
# else: print("no upper")
#
# if any(c in special_characters4 for c in word):
#     passed += 1
# else: print("no lower")
#
# if passed >= 3 and passed2 == 2:
#     print("password is valid")
# else:
#     print("password is not valid")
# --------------------------------------------------------------
# Temp converter
# number = input("Enter the number: ").strip()
# if number.isdigit():
#     print("Celcius: ", int(number), "To Farenheit is: ", (int(number)*9/5+32))
# else:
#     print("Type a number not letters dumb-ass")
# --------------------------------------------------------------
# Speed converter
# number = input("Enter the number: ").strip()
# if number.isdigit():
#     print("Miles per hour: ", int(number), "To km/hour is: ", (int(number)*1.609))
# else:
#     print("Type a number not letters dumb-ass")
# --------------------------------------------------------------
# Moon weight converter
# number = input("Enter the number: ").strip()
# if number.isdigit():
#     print("Earth weight: ", int(number), "Moon weight: ", (int(number)*0.165))
# else:
#     print("Type a number not letters dumb-ass")
# --------------------------------------------------------------
# BMI weight
# weight = input("Enter your weight in kg: ").strip()
# height = input("Enter your height in cm: ").strip()
# if weight.isdigit() and height.isdigit():
#     bmi = int(weight) / ((float(height) /100) * (float(height) /100))
#     if bmi >= 18.5 and bmi <= 24.9:
#         print("healthboy")
#     else:
#         print("nonhealthboy")
# else:
#     print("Type a number not letters dumb-ass")
# --------------------------------------------------------------
# The speeding ticket fine policy in Podunksville is $50, plus $5 for each kph over the limit [which is 100 kph] plus a penalty of $200 for any speed over 120 kph.
# Write a program that accepts a speed limit and a clocked speed and either prints a message indicating the speed was legal or prints the amount of the fine.
# speed = input("Enter the speed in kph: ").strip()
# if speed.isdigit():
#     speed = int(speed)
#     if speed <= 100:
#         print("Speed is legal")
#     elif speed > 100:
#         cost = 50
#         cost += (speed - 100) * 5
#         if speed >= 120: cost += 200
#         print("speed is illegal and the fine is:", "$" + str(cost))
# else:
#     print("Type speed limit not letters")
# --------------------------------------------------------------
# A formulae for computing Easter in the years 1982-2048 inclusive, is as follows:
# let a = year mod 19, b = year mod 4, c = year mod 7, d = (19a + 24) mod 30, e = (2b + 4c +6d + 5) mod 7. The date of Easter is March 22 + d + e
# (which could be in April. Write a program that inputs a year, verifies that it is in the proper range, and then prints out the date of Easter that year.
# value = input(("Enter the year (between 1982-2048): ")).strip()
# if value.isdigit():
#     value = int(value)
#     a = value % 19
#     b = value % 4
#     c = value % 7
#     d = (19 * a + 24) % 30
#     e = (2 * b + 4 * c + 6 * d) % 7
#     date = 22 + d + e
#     if date >= 44 or date <= 31:
#         print("Date is invalid")
#     else:
#         print("Date is valid easter is at:", date)
# else:
#     print("Date is invalid")

# Other one

# year = int(input("input a year: "))
#
# if year < 1982 or year > 2048:
# print ("cant calculate a year")
# else:
# a = year % 19
# b = year % 4
# c = year % 7
# d = (19 * a + 24) % 30
# e = (2 * b + 4 * c + 6 * d + 5) % 7
# easter = 22 + d + e
# if easter > 31:
# easter = easter-31
# print("Easter will be on April", easter )
# else:
# print(""
# "Easter will be on March", easter)
# -------------------------------------------------------------
# A year is a leap year if it is divisible by 4, and if it is a century, it must also be divisible by 400. (1800 and 1900 are not leap years while 1600 and 2000 are).
# Write a program that calculates whether a year is a leap year.
# value = int(input(("Enter the year: ")).strip())
#
# if value % 4 == 0:
#     if value % 100 == 0:
#         if value % 400 == 0:
#             leep = True
#         else:
#             leep = False
#     else:
#         leep = True
# else:
#     leep = False
# print(leep, "it is a leep year")
# -------------------------------------------------------------
# The date 10 June 1960 is special because the day times the month equals the year. Create a program
# that asks the user to enter a date in the format dd/mm/yy and output whether it is a magic date or not.
# value = input(("Enter the date in (dd/mm/yy): ")).strip()
# a = int(value[0:2])
# b = int(value[3:5])
# c = int(value[6:])
# if a * b == c:
#     print("is magic")
# else:
#     print("is not magic")
# -------------------------------------------------------------
#    temp          exclusive end
#   counter      start step
# for i in range(1,2,1:
#   print(i)
# -------------------------------------------------------------

# -------------------------------------------------------------
