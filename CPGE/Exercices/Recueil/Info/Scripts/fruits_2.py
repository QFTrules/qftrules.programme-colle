def kvoisins(point, parametres, p, distance, k):
    tri = sorted(parametres, key=lambda p: distance(point, p))
    # On prend les k plus proches voisins
    voisins = tri[:k]
    # On compte le nombre de voisins dans chaque classe
    classes_count = {}
    for voisin in voisins:
        classe_voisin = p[voisin]
        if classe_voisin in classes_count:
            classes_count[classe_voisin] += 1
        else:
            classes_count[classe_voisin] = 1
    # On trouve la classe majoritaire
    classe_majoritaire = max(classes_count, key=classes_count.get)
    return classe_majoritaire