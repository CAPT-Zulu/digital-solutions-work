# Write a program which outputs triangle numbers - 1, 3, 6, 10,15, etc.
# We initialise a variable to 0 and then add the loop counter to it during each pass through the loop.
# The value of the number changes thus: 0, 0+1, 1+2, 3+3, 6+4, 10+5, etc

# var, var2 = 0, 0
# for x in range(7):
#     var += var2
#     var2 += 1
#     print(var)

# total = 0
# for i in range(7)
#     total += i
#     print(total)

# Write a program which displays the factors of a number (a factor is a number that divides evenly into a number, leave out 1 because it is a factor of all numbers.

# n = int(input("Enter a number: "))
# factor_count = 0
# for i in range(2, n+1):
#     if n % i == 0:
#         print(i)
#         factor_count += 1
#
# if factor_count > 1:
#     print(n, "is not a prime")
# else:
#     print(n, "is a prime")

# for x in range(1, 6):
#     val = ""
#     for i in range(x-1):
#         val += str(x)
#     print(val + str(x))

# #
# _#
# __#
# ___#
# ____#


# for x in range(1, 6):
#     val = ""
#     for i in range(x-1):
#         val += str("_")
#     print(val + "#")

#A
#B B
#C C C
#D D D D
#E E E E E

# for x in range(7):
#     val = ""
#     if x == 2: val2 = "A "
#     if x == 3: val2 = "B "
#     if x == 4: val2 = "C "
#     if x == 5: val2 = "D "
#     if x == 6: val2 = "E "
#     for i in range(x-1):
#         val += val2
#
#     print(val)
#
# #1
# #22
# #333
# #4444
# #55555
#
# for x in range(7):
#     val = ""
#     if x == 2: val2 = "1"
#     if x == 3: val2 = "2"
#     if x == 4: val2 = "3"
#     if x == 5: val2 = "4"
#     if x == 6: val2 = "5"
#     for i in range(x-1):
#         val += val2
#
#     print(val)
#
# #....1
# #...22
# #..333
# #.4444
# #55555
#
# for x in range(2, 7):
#     val = ""
#     if x == 2: val2 = "1"
#     if x == 3: val2 = "2"
#     if x == 4: val2 = "3"
#     if x == 5: val2 = "4"
#     if x == 6: val2 = "5"
#     for c in range(-x + 6):
#         val += "."
#     for i in range(x-1):
#         val += val2
#
#     print(val)

# Write a program which finds and displays the 'perfect numbers' up to a user-supplied value.
# (A perfect number is one whose factors add up to the number itself, eg 6 = 1+2+3.)
#  N = 2p – 1 (2p – 1)
# for x in range(1, 24):
#     val = 2*x - 1
#     print(val)

val = 2
for x in range(1, 8129):
    val2 = 0
    for i in range (1, val):
        if (val % i) == 0:
            val2 += i
    if val2 == val:
        print(val)
    val += 1