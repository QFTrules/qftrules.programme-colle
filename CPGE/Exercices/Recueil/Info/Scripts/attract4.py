def attract(G,A,j):
    IG = inverse(G)             # inverse de G
    for s in A:                 # boucle sur sommets gagnants s
        for p in IG[s]:         # boucle sur prédecesseurs de s
            if p[0] != j:       # si prédecesseur non associé au joueur J
                ...             # à compléter
            A.append(p)         # ajout à l'attracteur
    return A                    # renvoie l'attracteur
