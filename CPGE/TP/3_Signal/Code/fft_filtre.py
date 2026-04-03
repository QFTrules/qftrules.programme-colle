import numpy.fft as ft
import numpy as np

""" SIGNAL AUDIO ÉCHANTILLONNÉ """
import soundfile as sf
audio    = 'sample.wav'
data, fs = sf.read(audio) # fs = fréquence d'échantillonage intrinsèque
s        = data[:,0]      # signal audio
TF       = ft.fft(s)      # spectre complet du signal audio

""" FILTRE ANTI-REPLIEMENT """
f         = np.linspace(0,fs,len(data)) # liste fréquences
fe        = 1600                        # fréquence échantillonnage (Hz)
filtre    = ...                         # filtre par une porte
TF_filtre = TF*filtre                   # spectre filtré
s_filtre  = np.real(ft.ifft(TF*filtre)) # signal filtré

""" ÉCOUTE AUDIO """
import sounddevice as sd
sd.play(s, fs)              # écoute signal original
# sd.play(s_filtre, fs)     # écoute signal filtré
status = sd.wait()
