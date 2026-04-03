def nim(n,j,G):
    adv = 1+j%2                            # adversaire de j
    if n > 2:                               # si plus de 2 objets
        G[(j,n)] = [(adv,n-2),(adv,n-1)]  # tirage d'1 ou 2 objets
        nim(n-1,adv,G)
        nim(n-2,adv,G)
    else:                                   # si plus d'objets
        G[(j,n)] = []                       # fin du jeu et j perd
