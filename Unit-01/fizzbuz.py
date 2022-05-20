# for every number between 1 - 100 inc
# either print number or if its a multiple of 3 = print "fizz" if multiple of 5 = "fuzz" 3+5 = "fizzbuzz"
for x in range(1, 101):
    if x % 3 == 0:
        if x % 5 == 0:
            print("fizzbuzz")
        else:
            print("fizz")
    elif x % 5 == 0:
        print("buzz")
    else:
        print(x)
# --------------------------------
for x in range(1, 101):
    if x % 3 == 0:
        if x % 5 == 0:
            a = "fizzbuzz"
        else:
            a = "fizz"
    elif x % 5 == 0:
        a = "buzz"
    else:
        a = x
    print(a)