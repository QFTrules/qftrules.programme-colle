def attract(G,A,j):
    IG = inverse(G)
    for s in A:                 # boucle sur sommets gagnants s
        for p in IG[s]:         # boucle sur prédecesseurs de s
            if p[0] != j:       # si prédecesseur non associé au joueur J
                if False in [(succ in A) for succ in G[p]]:
                    continue    # saut au prédecesseur suivant
            A.append(p)         # ajout à l'attracteur
    return A                    # renvoie l'attracteur
