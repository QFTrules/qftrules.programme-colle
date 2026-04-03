v0 = 2  # vitesse initiale                              
t  = np.linspace(0,tmax,N)  # tableau comprenant N instants régulièrement espacés de 0 à tmax
y  = -v0*t*np.sin(Omega*t)  # ordonnée
