def attract(G,F):
    """
    Entrée : graphe du jeu G (dict), sommets finaux F (list), joueur J (int)
    Sortie : attracteur A (list)
    """
    E = existe(G,F,1)   # de type list
    P = pourtout(G,F,2) # de type list
    A = F + E + P
    if E == [] and P == []:
        return A
    else:
        return attract(G,A)
