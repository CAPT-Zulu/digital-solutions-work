# english = input("Enter the english: ").strip()
# latin = ""
# words = english.split(" ")
# for word in words:
#     if len(word) > 1:
#         firstletter = word[:-len(word) + 1]
#         latin += (word[1:] + firstletter + "ay" + " ")
#     else:
#         latin += (word + "ay" + " ")
# print(latin)
#
val = input("Enter the words: ").strip()
clean_msg = " "
words = val.split(" ")