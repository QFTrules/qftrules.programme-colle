def minmax(A,s):
    """
    Entrée : arbre A (dict), nœud s = (j,n) avec j le joueur (int) et n le numéro (int)
    Sortie : heuristique h(s) (int)
    """
    if A[s] == []:                      # si s feuille
        if s[0] == 1:                   # si s appartient à J1
            return -1                   # h(s) = -1 car gagnant pour J2
        else:                           # si s appartient à J2
            return +1                   # h(s) = +1 car gagnant pour J1
    else:                               # si s pas feuille
        h = [minmax(A,n) for n in A[s]] # calcule h successeurs
        if s[0] == 1:                   # si s appartient à J1
             return max(h)              # h(s) = max des h successeurs
        else:                           # si s appartient à J2
            return min(h)               # h(s) = min des h successeurs
