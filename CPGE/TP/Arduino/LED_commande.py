from pyfirmata import Arduino, util
import time
carte = Arduino('/dev/ttyACM0')
acquisition = util.Iterator(carte)
acquisition.start()
sortie = carte.get_pin('d:2:o') # voie 2 en sortie digitale
time.sleep(1.0)
print("Début du test")
# temps d'initialisation de la carte
sortie.write(True) # envoie 5V sur la sortie
time.sleep(4)
# attendre 4 secondes
sortie.write(False) # mettre la sortie à 0V
print("Fin du test")
carte.exit()