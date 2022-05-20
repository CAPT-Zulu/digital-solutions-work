filename = open("textdocs/task3_test_data.txt")
lines = filename.readlines()

def MainFunction (val1):
    value = []
    for x in range(len(val1)):
        value.append("0")
        level = 0
        for i in val1[x+1:]:
            level += 1
            if i == val1[x]:
                value[x] = ("+" + str(level))
                break
    return value

for line in lines:
    word1, word2 = line.split(" ")
    word1, word2 = word1.strip(), word2.strip()
    if len(word1) == len(word2):
        letters1, letters2 = list(word1), list(word2)
        value_1, value_2 = MainFunction(letters1), MainFunction(letters2)

        if value_1 == value_2:
            print(word1 + ',', word2, "are isomorphs with repetition pattern", *value_1)
        else:
            print(word1 + ',', word2, "are not isomorphs")
    else:
        print(word1 + ',', word2, "have different lengths")