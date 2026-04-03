def moy(E, k, d, ni):
    c = sample(E, k)                    # centres aléatoires
    for j in range(ni):                 # itération du partionnement
        p = partition(E, c, d)          # partionnement autour des centres
        for i in p.values():                     # boucle sur classe i
            classe = [x for x in p if p[x] == i] # ensemble correspondant
            c[i]   = bary(classe)                # ré-évaluation centres
    return p, c                         # retourne partition et centres
