def nim(n,j):
    """
    Entrée : G (dict), n (int > 1), j (1 ou 2)
    Sortie : None
    """
    G = {}
    for i in range(2,n+1):
        G[(i,j)] = [(i-2,1+j%2),(i-1,1+j%2)]

G={}
nim(G,5,1)
G