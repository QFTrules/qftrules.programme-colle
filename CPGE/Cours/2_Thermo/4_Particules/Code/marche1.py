""" BIBLIOTHEQUES """
import numpy as np
import random as r

""" PARAMETRES """
l   = 1            # distance des sauts
tau = 1            # durée entre sauts
D   = l**2/2/tau   # coefficient de diffusion

""" SIMULATION """
def marche(Nstep):
    x = 0                          # position initale
    for i in range(Nstep):         # boucle sur les sauts
    	x = x + l*r.randint(-1,1)  # saut
    return x**2                    # position finale au carré
