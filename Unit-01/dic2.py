# student_grades = {
#     "Simon": 45,
#     "Alison": 78,
#     "John": 72,
#     "Tracy": 83,
#     "Zac": 22
# }
#
# print(type(student_grades))
# print(student_grades)
#
# #print the student names and their grades
# for k, v in student_grades.items():
#     print(k, "got: ", v)
#
# #ask for a name and return the grade or 'not found'
# # name = input("Enter a name: ")
# # if name in student_grades:
# #     print(student_grades[name])
# # else:
# #     print("Name not found")
#
#
# #print a list of all the student names -> ie the keys
# student_names = list(student_grades.keys())
# print(student_names)
#
#
# #print a list of all the grades -> ie the values
# print(student_grades.values())
#
#
# #sort the dictionary according to student names -> ie the keys
# print(sorted(student_grades.keys()))
#
# #sort the dictionary according to the grades -> ie the values
# print(sorted(student_grades.values()))
#
# #sort the dictionary in reverse order of student names
# print(list(reversed(sorted(student_grades.values()))))
fun = {}
sentence = input("Enter sentence: ")
sentence_split = sentence.split()

for word in sentence_split:
    if word in fun:
        fun[word] += 1
    else:
        fun[word] = 1
for k, v in fun.items():
    print(k, "for", v, "times")