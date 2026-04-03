from collections import deque
def cycleimp(G,d):
    """
    Entrée : graphe G, de type dict ; sommet de départ d, de type int.
    Action : détermine si G possède un cycle impair au départ de s.
    Sortie : True ou False, de type bool.
    """
    rang = {s:0 for s in G}
    succ = deque([d])
    while succ:
        s = succ.popleft()
        for x in G[s]:
            if not rang[x]:
                rang[x] = rang[s] + 1
                succ.append(x)
            elif rang[x] == rang[s]:
                return True
    return False
