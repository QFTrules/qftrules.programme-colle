def d(x, y):
    return (y[0]-x[0])**2 + (y[1]-x[1])**2

def tri(E, x, d):
  return sorted(E, key = lambda y:d(x,y))  # tri selon la distance de y à x

def voisins(E, x, d, k):
    liste = tri(E, x, d)                # liste triée (y,distance)
    return liste[:k]                    # k points y les plus proches

def classe(E, x, d, k, p):
    v = voisins(E, x, d, k)             # k plus proches voisins de x
    c = {p[y]:0 for y in v}             # liste des classes des voisins
    for y in v:                         # boule sur voisins
        c[p[y]] += 1                    # comptage des classes
    maxi = 0                            # initialisation maximum
    for i in c:                         # boucle sur classes des voisins
        if c[i] > maxi:                 # si classe i plus nombreuse
            maxi, classmaj = c[i], i    # mise à jour classe majoritaire
    return classmaj                     # retourne classe majoritaire

x = (0.5,0)
print(classe(E, x, d, 1, p))
plt.plot(x,'b')
plt.show()
