def classement(E):          # Entrée : liste E
    """
    Entrée : ensemble de mots E de type list (liste)
    Action : classe mots de E selon longueur (inférieure ou supérieure à 3)
    Sortie : classification p de type dict (dictionnaire)
    """
    p = {}                   # initialisation classification
    n = len(E)               # nombre de mots
    for mot in E:            # boucle sur les mots
        if len(E) > 3:       # si long mot
            p[mot] = 'long'  # classe long
        else:                # sinon
            p[mot] = 'court' # classe court
    return p                 # Sortie : dictionnaire p
