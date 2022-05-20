filename = open("TextFiles/Plurals.txt")
lines = filename.readlines()

for line in lines:
    line = line.strip("\n")
    line = line.split(" ")
    if len(line) > 1:
        value = line[0]
        type = line[1]

        if value == '0':
            value = "no"
        elif value == '1':
            value = "one"

        if value != "one":
            if type[-1] in 'sxz':
                type = type + 'es'
            elif type[-2:] == 'ch' or type[-2:] == 'sh':
                type = type + 'es'
            elif type[-1] == 'o' and type[-2] not in 'aeiou':
                type = type + 'es'
            elif type[-1] == 'y' and type[-2] not in 'aeioux':
                type = type[0:-1] + 'ves'
            elif type[-2:] == 'fe' and type[-3] != 'f':
                type = type[0:-2] + 'ves'
            elif type[-1:] == 'f' and type[-2] != 'f':
                type = type[0:-1] + 'ves'
            else:
                type = type + 's'
        print(value, type)