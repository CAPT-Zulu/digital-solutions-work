import random

#Write a loop that will continuously input and print the names of contest participants, until QUIT is entered in place of the name.
# x = True
# name = "Names:"
# while x:
#     nameadd = input("Input name: ")
#     if nameadd == "quit": x = False
#     name = name + ", " + nameadd
#     print(name)

# The factorial of an integer N is the product of all of the integers between 1 and N, inclusive.
# For example if N = 5 then the factorial would be 1*2*3*4*5. Write a while loop that computes the factorial of a given integer N.

# n = int(input("Enter num: "))
# while n != 1:
#     print(n)
#     if n % 2 ==0:
#         n = int(n / 2)
#     else:
#         n = int(n * 3 + 1)
#     print(n)

# x = 26000000
# i = 0
# while x < 50000000:
#     x = x *1.03
#     i += 1
# print("It will take Uganda:", (i), "Years to make it to 50 mill population.")
#
# #
#
# x = int(input("num 1: "))
# i = int(input("num 2: "))
# val=x%i
# while val:
#     x=i
#     i=val
#     val=x%i
# print(i)

# 14. In the game of Lucky Sevens, the player rolls a pair of dice. If the dice add up to 7, the player wins $4; otherwise the player loses $1.
# Suppose that, to entice the gullible, a casino tells players that there are lots of ways to win: (1, 6), (2, 5), (3, 4) etc.
# A little mathematical analysis reveals that there are not enough ways to win to make the game worthwhile;
# however, because many people’s eyes glaze over at the first mention of mathematics, your challenge is to write a program that demonstrates the futility of playing the game.
# Your program should take as input the amount of money that the player wants to put into the pot, and play the game until the pot is empty.
# At that point, the program should print the number of rolls it took to break the player, as well as maximum amount of money in the pot.

x = int(input("Enter the cash amount (without $): "))
val3 = 0
val4 = x
while x > 0:
    val = int(random.randint(1, 6))
    val2 = int(random.randint(1, 6))
    val3 += 1
    print("Rolled a", val, "and a", val2)
    if val + val2 == 7:
        x += 4
        val4 += 4
        print("You won $4 you now have", "$" +str(x))
    else:
        x -= 1
        print("You have lost $1 you now have", "$" + str(x))
print("You are out of money you played", val3, "times the maximum your pot reached was", "$" + str(val4))

# 15. Write a program that prompts the user to enter their user name and password.
# It should check these against values of your choosing. If these values are correct, it should display “welcome back, you are logged in”.
# If they are wrong, it should display “either username or password is incorrect”.
# If they have tried 3 times and got it wrong, your program should display “your account is now locked out for 60 minutes”.

x = True
times = 3
set_user = "admin"
set_pass = "1234"
while x:
    ent_user = input("Input your username: ")
    ent_pass = input("Input your password: ")
    if ent_user == set_user or ent_pass == set_pass:
        x = False
        print("Welcome back, you are logged in")
    else:
        times -= 1
        print("either username or password is incorrect")
        if times <= 0:
            x = False
            print("your account is now locked out for 60 minutes")
