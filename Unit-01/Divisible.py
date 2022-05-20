filename = open("TextFiles/divs.txt")
contents = filename.readlines()
for line in contents:
    values = line.split()
    count = 0
    start = int(values[0])
    end = int(values[1])
    for number in range(start,end+1,1):
        valid = True
        for i in range(len(str(number))):
            number = str(number)
            val1 = number[0:i+1]
            val2 = number[i]
            if int(val1) == 0 or int(val2) == 0:
                valid = False
            elif int(val1) % int(val2) != 0:
                valid = False
        if valid == True:
            count += 1
    print(count)