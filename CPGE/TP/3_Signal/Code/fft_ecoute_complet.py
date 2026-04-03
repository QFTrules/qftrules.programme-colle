""" SIGNAL AUDIO ÉCHANTILLONÉ """
import soundfile as sf
import numpy as np
""" ÉCHANTILLONAGE """
fe = 1600                           # fréquence d'échantillonnage (Hz)
T  = 10                             # durée d'acquisistion (s)
t  = np.linspace(0,T,int(T*fe))     # instants d'échantillonnage
audio    = 'sample.wav'
data, fs = sf.read(audio) # fs = fréquence d'échantillonage de l'audio
s        = [data[i,0] for i in np.arange(0,T*fs,int(fs/fe))]

""" ÉCOUTE AUDIO """
import sounddevice as sd
sd.play(s, fe)
status = sd.wait()
