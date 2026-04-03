"""
Pyplot animation example.

The method shown here is only for very simple, low-performance
use.  For more demanding applications, look at the animation
module and the examples that use it.
"""

import matplotlib.pyplot as plt
import numpy as np
import random
 
# defining the number of steps
n = 2000
 
#creating two array for containing x and y coordinate
#of size equals to the number of size and filled up with 0's
x = np.zeros(n)
y = np.zeros(n)
t = 0
dt = 0.01


# filling the coordinates with random variables
for i in range(1, n):
	t = t + dt
	val = random.randint(1, 4)
	p = plt.imshow(x,y)
	if val == 1:
		x[i] = x[i - 1] + 1
		y[i] = y[i - 1]
	elif val == 2:
		x[i] = x[i - 1] - 1
		y[i] = y[i - 1]
	elif val == 3:
		x[i] = x[i - 1]
		y[i] = y[i - 1] + 1
	else:
		x[i] = x[i - 1]
		y[i] = y[i - 1] - 1
	p.set_data(x,y)
	
	if i%int(np.log10(n)*2) == 0:
		fig = plt.gcf()
		plt.clim()
		plt.title("Boring slide show")
		plt.pause(0.1)
