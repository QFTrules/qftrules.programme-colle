""" TRACÉ """
x = +x0*np.cos(a*t)*np.cos(omega*t) + a*x0/omega*np.sin(a*t)*np.sin(omega*t)
y = -x0*np.sin(a*t)*np.cos(omega*t) + a*x0/omega*np.cos(a*t)*np.sin(omega*t)
plt.xlim(-1.5*x0,1.5*x0) # intervalle des x
plt.xlim(-1.5*x0,1.5*x0) # intervalle des y
plt.xlabel('x')          # étiquette de l’axe x
plt.ylabel('y')          # étiquette de l’axe y
plt.plot(x,y)            # tracé des points
plt.show()               # affichage du graphe
