a = set('abccddefgedaqr')
print(type(a),a)
sentance = "Fuck english sucks ass"
words = sentance.split()
set_words = set(words)
print(set_words)

#set_words = set(sentance.split())
if "Fuck" in set_words:
    print("Found")
else:
    print("Not Found")

student_names = {()}
print(type(student_names))