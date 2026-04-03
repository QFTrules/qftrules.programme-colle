from __future__ import division
import numpy as np
import math as math
import matplotlib.pyplot as plt



I = []
J = []

for i in np.linspace(20,60,1000):
	#I += [5*(1+math.cos(3*(2+5*i*i)))]
	J += [1+math.cos(i*i/25+4)]

for i in np.linspace(0,20,1000):
	I += [1+math.cos(i)]

fig = plt.figure(figsize=(3.5*2.75,3.5*1.96))
ax = fig.add_subplot(111)
for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
             ax.get_xticklabels() + ax.get_yticklabels()):
    item.set_fontsize(30)
plt.gca().xaxis.set_major_locator(plt.NullLocator())
plt.gca().yaxis.set_major_locator(plt.NullLocator())
ax.plot(np.linspace(20,60,1000),J,'-k')
ax.plot(np.linspace(0,20,1000),I,'-k')
plt.show()





