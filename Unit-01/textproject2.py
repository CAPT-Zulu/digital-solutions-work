file = open("TextFiles/studentdata.txt")
content = file.readlines()
name = ""
grd_1 = 0
grd_2 = 0
for line in content:
    line = line.strip('\n')
    line = line.split()
    name = line.pop(0)
    grd_1 = len(line)
    grd_2 = sum(list(map(int, line))) // len(line)
    print(name, "had", grd_1, "grades and their average for grades are", grd_2)