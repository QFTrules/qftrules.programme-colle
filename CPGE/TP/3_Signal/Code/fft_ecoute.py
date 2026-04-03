""" ÉCOUTE AUDIO """
import sounddevice as sd
sd.play(data, fs)
status = sd.wait()
