def noyau(G,N):
    if G == {}:             # si graphe vide
        return N            # retourner le noyau
    f = final(G)[0]         # choix d'UN sommet final
    L = [f]                 # initialisation des sommets à supprimer
    for s in G:             # boucle sur les sommets du graphe
        if f in G[s]:       # si s est un prédécesseur de f
            L.append(s)     # ajouter s à la liste des sommets à supprimer
    retrait(G,L)            # supprimer les sommets de L du graphe G
    noyau(G,N + [f])        # ajouter f au noyau et recommencer