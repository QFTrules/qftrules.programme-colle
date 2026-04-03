
from pyfirmata import Arduino, util
import time

carte = Arduino('/dev/ttyACM0')
acquisition = util.Iterator(carte)
acquisition.start()

Vpd = carte.get_pin('a:0:i')    # Analog input 0 : photodiode
# E   = carte.get_pin('a:0:i')    # Analog input 0 : alimentation
E  = 5   # Tension d'alimentation
R  = 1e4 # Résistance de mesure
N  = 10  # Nombre de mesures
Te = 1   # Période d'échantillonnage 

sortie = carte.get_pin('d:2:o') # Digital output 2 : Alim 5V

# boucle de mesure
for i in range(N):
    print(Vpd.read())
    Iph = (Vpd.read()-E)/R     # Read photocurrent
    print(Iph)                 # Print the calculated resistance
    time.sleep(Te)             # Wait for 5 seconds
time.sleep(1.0)
print("Début du test")
# temps d'initialisation de la carte
sortie.write(True) # envoie 5V sur la sortie
time.sleep(4)
# attendre 4 secondes
sortie.write(False) # mettre la sortie à 0V
print("Fin du test")
carte.exit()