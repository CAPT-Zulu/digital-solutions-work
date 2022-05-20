digits = input("Enter numbers: ").strip()
if digits.isdigit():
    total = 0
    for d in digits:
        total = total + int(d)
    print(total)
else:
    print("Only enter numbers")