def origine(G):
    """
    Entrée : G (dict)
    Sortie : origine de G
    """
    S = [s for i in G]      # Liste des sommets du graphe
    for s in G:             # Parcours des sommets du graphe
        for p in G[s]:      # Si p est un successeur de s
            if p in S:      # Si p est encore dans la liste des sommets
                S.remove(p) # On retire p de la liste des sommets
    return S[0]             # On retourne l'origine de G