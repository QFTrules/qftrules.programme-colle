def nim(n,j,G):
    jbis = 1+j%2                            # adversaire de j
    if n > 1:                               # si plus de 2 objets
        G[(j,n)] = [(jbis,n-2),(jbis,n-1)]  # tirage d'1 ou 2 objets
        nim(n-1,jbis,G)
        nim(n-2,jbis,G)
    elif n == 1:                            # si plus qu'1 objet
        G[(j,n)] = [(jbis,n-1)]             # tirage d'1 objet
        nim(n-1,jbis,G)
    else:                                   # si plus d'objets
        G[(j,n)] = []                       # fin du jeu et j perd
