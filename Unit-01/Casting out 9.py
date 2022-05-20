Data = \
"""10397802948132245665478667812312
535431322878685168431268321854321
18684132684123843123684431
498643516884746746645687641351684865
213312695472"""
Lines = Data.split()
for x in Lines:
    Line = str(x)
    Num = list(Line)
    end = 0
    for i in Num:
        end += int(i)
        if end >= 9:
            end -= 9
    print(end)

