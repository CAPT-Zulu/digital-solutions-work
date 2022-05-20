happy_list = []
unhappy_list = []
for n in range(1, 1000, 1):
    checked = []
    nums = str(n)
    while nums != '1' and not (nums in checked):
        checked.append(nums)
        result = 0
        for num in nums:
            result += int(num)**2
        nums = str(result)
        if result == 1:
            happy_list.append(n)
        elif nums in checked:
            unhappy_list.append(n)
    if nums == '1':
        print("True")
    else:
        print("False")