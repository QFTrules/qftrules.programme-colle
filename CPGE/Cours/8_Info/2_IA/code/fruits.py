from random import random, randrange
def banane():
    m = 120 + 30*random()
    v = 150 + 100*random()
    return m,v
def kiwi():
    m = 80 + 10*random()
    v = 220 + 30*random()
    return m,v
def tomate():
    m = 100 + 20*random()
    v = 70 + 70*random()
    return m,v

def fruits(N):
    E = []
    for i in range(N):
        fruit = randrange(3)
        if fruit == 0:
            E.append(banane())
        if fruit == 1:
            E.append(kiwi())
        if fruit == 2:
            E.append(tomate())
    return E
