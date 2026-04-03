import numpy as np
from matplotlib import rc
import matplotlib.pyplot as plt


# Use LaTeX for text rendering
rc('text', usetex=True)
rc('font', family='serif')

""" ÉCHANTILLONNAGE """
fe = 1600                           # fréquence d'échantillonnage (Hz)
T  = 10                             # durée d'acquisistion (s)
N  = int(T*fe)                      # nombre de points
t  = np.linspace(0,T,N)             # instants d'échantillonnage

""" SIGNAL AUDIO ÉCHANTILLONNÉ """
import soundfile as sf
audio    = 'sample.wav'
data, fs = sf.read(audio) # fs = fréquence d'échantillonage intrinsèque
s        = [data[i,0] for i in np.arange(0,T*fs,int(fs/fe))] # signal

""" TRACÉ SIGNAL DANS LE TEMPS """
plt.xlim(0,T)               # intervalle des abscisses
plt.ylim(-1.5,1.5)          # intervalle des ordonnées
plt.xlabel(r'$t$ (s)')             # étiquette abscisse
plt.ylabel(r'$s(t)$ (V)')          # étiquette ordonnées
plt.plot(t,s,'r+')          # tracé en croix (+) rouges (b)
plt.savefig('audio_fe={}.pdf'.format(fe))
plt.show()                  # affichage figure

from numpy.fft import fft

""" SPECTRE EN FRÉQUENCE """
TF = np.abs(fft(s))
f  = np.linspace(0,fe,int(fe*T))
plt.xlabel(r'$f$ (Hz)')             # étiquette abscisse
plt.ylabel(r'amplitude')          # étiquette ordonnées
plt.plot(f,TF,'r')
plt.savefig('spectre_audio_fe={}.pdf'.format(fe))
plt.show()
