def erreur(M):
    n = len(M)
    N = sum(sum(M))
    TE = 0
    for i in range(N):
        for j in range(N):
            if i != j:
                TE += M[i][j]
    return TE/N
def sensibilite(M):
    return M[0][0]/(M[0][0]+M[1][0])
def specificite(M):
    return M[1][1]/(M[0][1]+M[1][1])
def prevalence(M):
    N = M[0][0] + M[0][1] + M[1][0] + M[1][1]
    return (M[0][0]+M[0][1])/N
