from numpy.fft import fft

""" SPECTRE EN FRÉQUENCE """
TF = np.abs(fft(s))
f  = np.linspace(0,fe,int(fe*T))
plt.plot(f,TF,'r')
plt.show()
