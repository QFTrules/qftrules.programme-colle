from collections import deque
def cycleimp(G,d):
    """
    Entrée : graphe G, de type dict ; sommet de départ d, de type int.
    Action : détermine si G possède un cycle impair au départ de s.
    Sortie : True ou False, de type bool.
    """
    rang = {s:0 for s in G}             # Initialiser le rang des sommets.
    succ = deque([d])                   # Initialiser la file des successeurs.
    while succ:                         # Tant qu’il y a des successeurs :
        s = succ.popleft()              # retirer le premier entré s ;
        for x in G[s]:                  # pour chaque successeur x de s,
            if not rang[x]:             # si le rang de x n’est pas encore déterminé :
                rang[x] = rang[s] + 1   # le rang de x vaut 1 + celui de s,
                succ.append(x)          # ajouter x à la file des successeurs ;
            elif rang[x] == rang[s]:    # sinon, si sommet et successeur ont même rang :
                return True             # il existe un sommet impair.
    return False                        # Sinon, il n’existe pas de sommet impair.
