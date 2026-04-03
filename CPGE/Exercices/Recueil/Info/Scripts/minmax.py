def minmax(A,s):
    """
    Entrée : arbre A (dict), nœud s = (j,n) avec j le joueur (int) et n le numéro (int)
    Sortie : heuristique h(s) (int)
    """
    if A[s] == []:
        if s[0] == 1:
            return ...
        else:
            return ...
    else:
        h = [minmax(A,n) for n in A[s]]
        if s[0] == 1:
             return ...
        else:
            return ...
