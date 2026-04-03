def nim(G,n,j):
    """
    Entrée : G (dict), n (int > 1), j (1 ou 2)
    Sortie : None
    """
    adv = 1+j%2                             # adversaire de j
    if n >= 2:                              # si sommet final non successeur de n
        G[(n,j)] = [(n-2,adv),(n-1,adv)]    # ajouter successeurs de n à G
        nim(G,n-1,adv)                      # appeler nim sur successeur n-1
        nim(G,n-2,adv)                      # appeler nim sur successeur n-2
    elif n == 1:                            # si sommet final successeur de n               
        G[(n,j)] = [(n-1,adv)]              # ajouter successeur de n à G
        nim(G,n-1,adv)                      # appeler nim sur successeur n-1
    else:                                   # si n sommet final (n=0)               
        G[(n,j)] = []                       # liste des successeurs vide