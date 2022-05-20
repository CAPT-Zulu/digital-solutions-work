students = []

students.append("Peter")
students.append("Paul")
students.append("Mary")

print(type(students))
print(students)
print(students[1])
print(len(students))
print(students[-1])
print(students.pop)

for student in students:
    print(student)

new_students = ["Simon", "Andrew", "Martha", "Andrea"]
grades = [23, 45, 79, 32]

for i in range(len(new_students)):
    print(new_students[i], "got the grade", grades[i])

nme = 'blood'
let = list(nme)
print(let)

name = 'some thing'
name_parts = name.split()
print(name_parts)
first_name = name_parts[0]
last_name = name_parts[1]
print(last_name.upper(), first_name)