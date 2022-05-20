filename = "TextFiles/results-1line.txt"
file = open(filename)

context = file.readlines()
for line in context:
    line = line.strip('\n')
    values = line.split(', ')

    name = values[0]
    mark = values[1]
    if int(mark) > 79:
        grade = 'A'
    elif int(mark) > 69:
        grade = 'B'
    elif int(mark) > 49:
        grade = 'C'
    else:
        grade = 'F'
    print(name, grade)

# Home work studentdata.txt
# number of marks recived and average of marks