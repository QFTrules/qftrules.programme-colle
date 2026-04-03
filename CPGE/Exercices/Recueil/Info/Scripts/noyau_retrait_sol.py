def retrait(G,L):
    for s in L:                 # Pour tout sommet s à retirer
        G.remove(s)             # Retirer s de la liste des sommets  
        for p in G:             # Pour tout sommet p du graphe
            if s in G[p]:       # Si s successeur de p
                G[p].remove(s)  # Retirer s de la liste des successeurs de p