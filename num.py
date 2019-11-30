import random

def random_num():
    a = []
    i = 0
    base = []
    while i<1000:
        base = [0,0]
        v1 = random.randrange(0,4)
        base[0] = v1
        v2 = random.randrange(0,10)
        base[1] = v2
        a.append(base)
        i += 1
    return a

lista = [1, 2, 3, 4]


