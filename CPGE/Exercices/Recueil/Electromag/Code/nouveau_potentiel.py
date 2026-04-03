def nouveau_potentiel(V, rhos, frontiere, i, j):
    if frontiere[i, j]: # on ne modifie pas le potentiel d'un point de la frontiere
        return V[i, j] # car il est imposé et donc fixé dès le début
    else: # sinon on utilise la relation (5)
        return (V[i, j+1]+V[i, j-1]+V[i+1, j]+V[i-1, j]+rhos[i, j])/4