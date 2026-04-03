def nim(G,n,j,p):
    """
    Entrée : G (dict), n (int > 1), j (1 ou 2), p (int < n)
    Sortie : None
    """
    G[(n,j)] = []
    adv = 1+j%2
    i   = 1
    while n >= i and i <= p:
        G[(n,j)].append((n-i,adv))
        nim(G,n-i,adv,p)
        i += 1