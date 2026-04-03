def partition(E, centres, d):
    """
    Entrée : ensemble d’apprentissage E (list), centres de classe centres (list), 
             distance d (function)
    Action : partitionne E autour des centres selon la distance d
    Sortie : partition p (dict)
    """
    p = {}                   # initialisation partition = dictionnaire vide
    for x in E:              # pour chaque donnée d'apprentissage x
        c    = min(centres, key = lambda y:d(x,y))  # centre le plus proche de x
        p[x] = centres.index(c)                     # classe attribuée à x
    return p
