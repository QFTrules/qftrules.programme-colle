# graphique
import matplotlib.pyplot as plt
plt.figure(figsize=(10,7))
plt.rc('font', size=16)
plt.xlabel('x')
plt.ylabel('y')
plt.errorbar(X,Y,fmt='+',       
                 xerr=0.3,      
                 yerr=1)
plt.plot(X,a*X+b,'r')
plt.show()
