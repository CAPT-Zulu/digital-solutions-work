student_ages = {} #empty dic

student_ages["Elliot"] = 16
student_ages["Ronan"] = 17
student_ages["Matthew"] = 17
student_ages["Louis"] = 18
print(len(student_ages))

if "Ronan" in student_ages:
    print(student_ages['Ronan'])

x = True
while x:
    name = input("Enter name: ")
    if name == "quit":
        x = False
    else:
        if name not in student_ages:
            age = int(input("Enter age: "))
            student_ages[name] = age
        else:
            print("No")
        print(student_ages)