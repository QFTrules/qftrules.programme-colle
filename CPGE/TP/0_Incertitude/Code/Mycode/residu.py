# residus
import matplotlib.pyplot as plt
plt.figure(figsize=(10,7))
plt.rc('font', size=16)
plt.xlabel('x')
plt.ylabel('Residu')
plt.errorbar(X,residu(p[0],X,Y),
                fmt='+',
                xerr=0.3,
                yerr=1)
plt.show()
