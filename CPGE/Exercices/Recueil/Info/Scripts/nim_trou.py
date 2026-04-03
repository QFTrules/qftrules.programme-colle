def nim(G,n,j):
    """
    Entrée : G (dict), n (int > 1), j (1 ou 2)
    Sortie : None
    """
    adv = 1+j%2
    if n >= 2:
        G[(n,j)] = 
        nim(G,n-1,adv)
        nim(G,n-2,adv)
    elif n == 1:
        G[(n,j)] = 
        nim(G,n-1,adv)
    else: 
        G[(n,j)] = 
