def origine(G):
    """
    Entrée : G, un dictionnaire représentant un graphe orienté
    Sortie : s0, l'origine de G
    """
    S = G.keys()        # Liste des sommets du graphe
    for s in S:         # Parcours des sommets du graphe
        for p in G[s]:  # Si p est un successeur de s
            S.remove(p) # On retire p de la liste des sommets
    return S[0]         # On retourne l'origine de G