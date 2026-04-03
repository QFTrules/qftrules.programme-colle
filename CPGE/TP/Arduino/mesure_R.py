from pyfirmata import Arduino, util
import time

carte = Arduino('/dev/ttyACM0')  # Connect to Arduino board
acquisition = util.Iterator(carte)  # Create an iterator for reading analog inputs
acquisition.start()

tension_A0 = carte.get_pin('a:0:i')  # Set up analog input pin A0
time.sleep(1.0)

Rref = 1000  # Reference resistance in Ohms

for i in range(0,30):
    tensionCTN = tension_A0.read()  # Read analog input voltage
    Rctn = tensionCTN
    # Rctn = Rref * tensionCTN / (1 - tensionCTN)  # Calculate resistance using voltage divider formula
    print(Rctn)  # Print the calculated resistance
    time.sleep(2)  # Wait for 5 seconds

carte.exit()  # Stop the measurements and disconnect from Arduino
