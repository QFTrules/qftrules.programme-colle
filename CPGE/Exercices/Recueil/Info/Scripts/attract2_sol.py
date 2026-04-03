def final(G,j):
    F = []
    for s in G:
        if G[s] == [] and s[0] == j:
            F.append(s)
    return F
