def final(G):
"""
Entrée : G, un dictionnaire représentant un graphe orienté
Sortie : F, une liste des sommets finaux
"""
F = []            # Initialisation de la liste des sommets finaux
for s in G:       # Parcours des sommets du graphe
    if G[s] == []:  # Si le sommet s n'a pas de successeur
        F.append(s)   # On ajoute s à la liste des sommets finaux
return F          # On retourne la liste des sommets finaux