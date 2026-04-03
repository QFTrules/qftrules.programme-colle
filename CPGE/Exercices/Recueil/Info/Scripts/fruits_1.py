def classification(fruits, parametres):
    """
    Entrée : fruits (list) : liste de chaînes de caractères
            parametres (list) : liste de tuples  (masse, couleur)
    Sortie : p (dict) : classification, de type (masse, couleur) : fruit
    """
    p = {}
    for i in range(len(fruits)):
        p[parametres[i]] = fruits[i]
    return p