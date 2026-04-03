def bary(points):
    """
    Entrée : points = liste de points de dimension 2
    Action : calcule le barycentre des points
    Sortie : b = barycentre des points
    """
    b = [0,0]               # initialisation du barycentre
    for x in points:        # boucle sur les points
        b[0] = b[0] + x[0]  # addition coordonnée x1
        b[1] = b[1] + x[1]  # addition coordonnée x2
    return b/len(points)    # barycentre = somme divisée par N
