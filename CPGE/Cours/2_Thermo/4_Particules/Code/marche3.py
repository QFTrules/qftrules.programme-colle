""" GRAPHIQUE """
import matplotlib.pyplot as plt
temps = range(100)      # tableau des temps
delta_diff = [np.sqrt(2*D*t*tau) for t in temps]
delta_simu = [dquad(t) for t in temps]

plt.xlabel('t')                     # temps
plt.ylabel('delta')                 # delta
plt.plot(temps,delta_simu,'b+')     # delta issu de la simulation
plt.plot(temps,delta_diff,'r-')     # delta issi de la loi sqrt(D*t)
plt.show()
