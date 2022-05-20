# names = []
#
# setname = input("enter name: ").strip()
# while setname.lower() != "quit":
#     if setname.title() not in names:
#         names.append(setname.title())
#     else: print("no")
#     setname = input("enter name: ").strip()
#
# names.sort()
# for name in names:
#     print(name)
import random

ballcount = []

while len(ballcount) < 6:
    val = int(random.randint(1, 45))
    if val not in ballcount:
        ballcount.append(val)
    else: print("no")

ballcount.sort()
print(ballcount)