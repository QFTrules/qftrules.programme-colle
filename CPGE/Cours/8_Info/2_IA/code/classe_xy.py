def classemaj(E, x, d, k, p):
    v = voisins(E, x, d, k)
    cvoisins = {p[y]:0 for y in v}
    for y in v:
        cvoisins[p[y]] += 1
    maxi = 0
    for classe in cvoisins:
        if cvoisins[classe] > maxi:
            maxi, cmaj = cvoisins[classe], classe
    return cmaj
