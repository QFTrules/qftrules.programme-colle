def init_centres(E,k,d):
    c = [sample(E,1)]
    for i in range(k-1):
        c.append(eloigne(c,E,d))
    return c