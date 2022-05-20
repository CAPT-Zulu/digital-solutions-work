

def getcharacter(hv):
    hv = str
    hexvalue = dict{"0":0-7 "f":15}
    if hv == str: hv = hv.lower()
    total = hexvalue(hv(0)) * 16 + hexvalue(hv(1))
    ascii_character = chr(total)
    return ascii_character