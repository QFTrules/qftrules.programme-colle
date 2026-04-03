def tri(E, x, d):
    """
    Entrée : E (list), x (tuple), d (func)
    Action : tri l’ensemble E selon la distance des points à x
    Sortie : E_tri (list)
    """
    n = len(E)
    E_tri = E
    for i in range(n):
        for j in range(n-i-1):
            if d(x,E_tri[j]) > d(x,E_tri[j+1]):
                E_tri[j], E_tri[j+1] = E_tri[j+1], E_tri[j]
    return E_tri