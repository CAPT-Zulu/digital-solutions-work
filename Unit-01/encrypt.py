msg = (input("Enter your plain text: ") + " ")
encrypted_msg = ("")

val = 0
val2 = -len(msg) + 1

letters = len(msg)

for letters in msg:

    letter = msg[val:val2]

    print(letter)

    if letter != "":
        order = ord(letter) + 123
    encrypted_msg = (encrypted_msg + str(order))

    val = val + 1
    val2 = val2 + 1

print(encrypted_msg)
# --------------------------------------------------------------
continuescrypt = (input("Press enter to continue"))

uncrpt_msg = ""
val = 0
val2 = -len(encrypted_msg) + 3

for x in range(0, len(encrypted_msg)//3 - 1):

    letter = encrypted_msg[val:val2]

    print(letter)

    if letter != "":
        order = int(letter) - 123
    uncrpt_msg = (uncrpt_msg + chr(order))

    val = val + 3
    val2 = val2 + 3

print(uncrpt_msg)