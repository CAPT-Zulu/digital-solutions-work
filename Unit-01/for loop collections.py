import random

# msg = "Fuck random shit ahhh"
# vowels = "aeiou"
#
# total = 0
#
# for i in range(len(msg)):
#     if msg[i].lower() in vowels:
#         total += 1
#
# print("Vowel total", total)
# ----------------------------------------------------------------------------------------------------------------------
# Ask the user to enter the number of numbers they will enter.
# Prompt the user for each of the numbers. Display the total, average, maximum and minimum number, the number of odd numbers and the number of even numbers.
# value1 = int(input("input the numbers of numbers your going to input: "))
#
# total = 0
# max = -1
# min = 101
# average = 0
# even = 0
# odd = 0
#
# for x in range(1, value1 + 1):
#     num = int(input("Input value of " + str(x) + ": "))
#     total += num
#     if num > max:
#         max = num
#     if num < min:
#         min = num
#     if num % 2 == 0:
#         even += 1
#     else:
#         odd += 1
# average = total / x
# print("Total:", total)
# print("Average:", average)
# print("Max", max)
# print("Min", min)
# print("Odd", odd)
# print("Even", even)
# ----------------------------------------------------------------------------------------------------------------------
# Simulate the rolling of dice in Yahtzee, by getting 5 random numbers between 1 and 6. Display each number on a line.

# for x in range(5):
#     num = random.randint(1, 6)

# ----------------------------------------------------------------------------------------------------------------------
# Ask the user to enter the number of rolls of dice and then display the frequency of each number.
num = int(input("Input number of roles: "))
roll1, roll2, roll3, roll4, roll5, roll6 = 0, 0, 0, 0, 0, 0
for x in range(num):
    val = int(random.randint(1, 6))
    if val == 1: roll1 += 1
    elif val == 2: roll2 += 1
    elif val == 3: roll3 += 1
    elif val == 4: roll4 += 1
    elif val == 5: roll5 += 1
    elif val == 6: roll6 += 1
print("rolled 1:", "(" + str(roll1) + ")", "rolled 2:", "(" + str(roll2) + ")", "rolled 3:", "(" + str(roll3) + ")", "rolled 4:", "(" + str(roll4) + ")", "rolled 5:", "(" + str(roll5) + ")" ,"rolled 6:", "(" + str(roll6) + ")")
# ----------------------------------------------------------------------------------------------------------------------