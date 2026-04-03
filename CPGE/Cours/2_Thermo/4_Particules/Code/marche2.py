""" DISTANCE MOYENNE QUADRATIQUE """
def dquad(Nstep):
    xcarre = []                         # initialisation tableau
    for i in range(1000):               # 1000 simulutions
        xcarre.append(marche(Nstep))    # simultion d’une marche
    return np.sqrt(np.mean(xcarre))     # moyenne quadratique
