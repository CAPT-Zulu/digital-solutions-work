filename = open("TextFiles/Pangrams.txt")
lines = filename.readlines()
abc = 'abcdefghijklmnopqrstuvwxyz'
for line in lines:
    pangram = 0
    line = line.strip("\n").strip(" ").lower()
    letters = set(line)
    for let in letters:
        if let in line:
            pangram += 1
    if pangram >= 26:
        print("Is pangram")
    else:
        print("Not pangram missing:", *sorted(set(abc) - set(line)), sep = ", ")