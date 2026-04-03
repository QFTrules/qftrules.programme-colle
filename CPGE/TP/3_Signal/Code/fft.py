import numpy as np
from scipy import signal
from numpy.fft import fft
import matplotlib.pyplot as plt

""" ÉCHANTILLONAGE """
f  = 1000 			                # fréquence du signal (Hz)
fe = 3200                           # fréquence d'échantillonnage (Hz)
T  = 10                             # durée d'acquisistion (s)
t  = np.linspace(0,T,int(T*fe))     # instants d'échantillonnage

sinu  = np.cos(2*np.pi*f*t)         # signal sinusoïdal échantillonné
carr  = signal.square(2*np.pi*f*t)  # signal carré échantilloné

""" SIGNAL AUDIO """
import soundfile as sf
import sounddevice as sd
audio = 'sample.wav'
data, fs = sf.read(audio, dtype='float32')
data_e = [data[i,0] for i in np.arange(0,T*fs,int(fs/fe))]
#print(data_e)
#sd.play(data_e, fe)
#status = sd.wait()

""" TRACÉ SIGNAL DANS LE TEMPS """
plt.xlim(0,T)
plt.ylim(-1.5,1.5)
plt.xlabel('t')             # étiquette abscisse
plt.ylabel('s(t)')          # étiquette ordonnées
plt.plot(t,sinu,'b+')       # tracé en croix (+) bleues (b)
plt.plot(t,data_e,'r+')       # tracé en croix (+) bleues (b)
plt.show()                  # affichage figure

""" SPECTRE EN FRÉQUENCE """
TFsinu = np.abs(fft(sinu))
TFsinu = TFsinu/max(TFsinu)
TFcarr = np.abs(fft(data_e))
TFcarr = TFcarr/max(TFcarr)
f      = np.linspace(0,fe,int(fe*T))
plt.plot(f,TFsinu,'b')
plt.plot(f,TFcarr,'r')
plt.show()
