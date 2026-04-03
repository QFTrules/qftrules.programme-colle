import numpy as np
import matplotlib.pyplot as plt

""" ÉCHANTILLONNAGE """
fe = 8000                           # fréquence d'échantillonnage (Hz)
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
plt.xlabel('t')             # étiquette abscisse
plt.ylabel('s(t)')          # étiquette ordonnées
plt.plot(t,s,'r+')          # tracé en croix (+) rouges (b)
plt.show()                  # affichage figure
