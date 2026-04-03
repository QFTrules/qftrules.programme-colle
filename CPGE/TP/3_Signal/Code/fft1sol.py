from numpy.fft import fft

""" SPECTRE EN FRÉQUENCE """
TF = np.abs(fft(s))              # Transformée de Fourier
f  = np.linspace(0,fe,int(fe*T)) # Tableau des fréquences
plt.plot(f,TF,'b')               # Représentation graphique
plt.show()                       # Affichage
