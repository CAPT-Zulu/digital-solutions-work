final_list = []
final_list_non = []
for x in range(1, 1000, 1):
    final = x
    for f in range(1, 100, 1):
        val2 = 0
        for i in str(x):
            val = 0
            i = int(i)
            val += i * i
            val2 += val
        x = val2
    if x == 1:
        print(x, final)
        final_list.append(final)
    else:
        final_list_non.append(final)
print("Question 1:", final_list[10])
print("Question 2:", final_list_non)
print("Question 3:", final_list[10])
print("Question 4:", final_list[10])
print("Question 5:", final_list[10])
print("Question 6:", final_list[10])