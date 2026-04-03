import numpy as np
import matplotlib.pyplot as plt

""" ÉCHANTILLONAGE """
f0 = 200                            # fréquence du signal (Hz)
fe = 1000                           # fréquence d'échantillonnage (Hz)
T  = 0.01                           # durée d'acquisistion (s)
t  = np.linspace(0,T,int(T*fe))     # instants d'échantillonnage
s  = np.cos(2*np.pi*f0*t)           # signal sinusoïdal échantillonné

""" VARIATION DANS LE TEMPS """
plt.xlim(0,T)               # intervalle des abscisses
plt.ylim(-1.5,1.5)          # intervalle des ordonnées
plt.xlabel('t')             # étiquette abscisse
plt.ylabel('s(t)')          # étiquette ordonnées
plt.plot(t,s,'b+-')         # tracé en croix (+) reliés (-) bleues (b)
plt.show()                  # affichage figure

from numpy.fft import fft

""" SPECTRE EN FRÉQUENCE """
TF = np.abs(fft(s))
f  = np.linspace(0,fe,int(fe*T))
plt.plot(f,TF,'b')
plt.show()


""" ÉCHANTILLONAGE """
fe = 8000                           # fréquence d'échantillonnage (Hz)
T  = 10                             # durée d'acquisistion (s)
t  = np.linspace(0,T,int(T*fe))     # instants d'échantillonnage

""" SIGNAL AUDIO ÉCHANTILLONÉ """
import soundfile as sf
audio    = 'sample.wav'
data, fs = sf.read(audio) # fs = fréquence d'échantillonage de l'audio
s        = [data[i,0] for i in np.arange(0,T*fs,int(fs/fe))]

""" TRACÉ SIGNAL DANS LE TEMPS """
plt.xlim(0,T)               # intervalle des abscisses
plt.ylim(-1.5,1.5)          # intervalle des ordonnées
plt.xlabel('t')             # étiquette abscisse
plt.ylabel('s(t)')          # étiquette ordonnées
plt.plot(t,s,'r+')          # tracé en croix (+) rouges (b)
plt.show()                  # affichage figure

from numpy.fft import fft

""" SPECTRE EN FRÉQUENCE """
TF = np.abs(fft(s))
f  = np.linspace(0,fe,int(fe*T))
plt.plot(f,TF,'r')
plt.show()

""" ÉCOUTE AUDIO """
import sounddevice as sd
sd.play(data, fs)
status = sd.wait()
