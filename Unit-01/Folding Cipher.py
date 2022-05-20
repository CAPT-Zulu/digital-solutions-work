filename = open("TextFiles/CipherH.txt")
message = filename.read()

key = ((ord(message[0]) - 64) % 3) + 3
rows = len(message) // 3

if len(message) % 3 > 0:
    rows += 1
print(key, rows, len(message))

clean_msg = ""
for j in range(0, rows ):
    print("Number:", j)
    if len(message) > j:
        clean_msg += message[j]
        print(j, rows, 0, 0, j + (rows * 1) - 0, message[j])
        for i in range(1, key):
            x = 0
            if j + (rows * i) - x >= len(message):
                x = len(message)
            print(j, rows, i, x, j + (rows * i) - x, message[j + (rows * i) - x])
            clean_msg += message[j + (rows * i) - x]
    clean_msg = clean_msg.replace("*"," ")
    print(clean_msg)
