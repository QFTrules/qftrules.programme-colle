""" NE PAS TOUCHER """

#module de base pour les figures
from doublefigure import *
#import scipy.optimize as spo

#load the first set of data
data = n.loadtxt('m0/scope_1.txt',skiprows=2)

temps = data[:,0]
V = data[:,1]

print ('\nPas de temps            dt = %.4f'%(temps[1]-temps[0]), 's')

uV = 0.00000001 # a modifier

# Calibrage du manometre
a = 390
b = 955
ua = 7
ub = 7

P = a*V+b # en hPa
uP = n.sqrt(n.square(ua*V)+n.square(a*uV))

# donnees experimentales
O = P[82:833]
t = temps[82:833]+18.70
N = n.shape(t)[0]            #taille de la liste

pe = 998.83

#incertitudes
t_err   = 0      #mettre t/100 si 1% d'incertitude par ex.
O_err   = uP[82:833]

# fonction f decrivant la courbe a ajuster aux donnees
def funct(p,x):
	a,b,c,d,e =  p
	return a*np.sin(b*x+c)*np.exp(-d*x)+e
	
# residuals
def residuals(p, x, y):
    return (funct(p,x) -y)/O_err

# ajustement
guess = n.array([-32, 5.27, -13, 0.151, 994])
result = opt.leastsq(residuals, guess, args=(t, O), full_output=1)

popt = result[0]
uopt = n.sqrt(np.abs(np.diagonal(result[1])))
print ('\n' +   'Amplitude                A = %.1f'%popt[0], '+- %.1f'%uopt[0], 'hPa', '\n' +
		'Pression équilibre      pe = %.2f'%popt[4], '+- %.2f'%uopt[4], 'hPa', '\n' +
      		'Pseudo-pulsation     omega = %.3f'%popt[1], '+- %.3f'%uopt[1], 's-1', '\n' +
		'Phase                  phi = %.2f'%popt[2], '+- %.2f'%uopt[2], 'rad', '\n' +
		'Coeff amortissement Lambda = %.3f'%popt[3], '+- %.3f'%uopt[3], 's-1', '\n')
      
### FIGURE ###

#dictionnaire pour les couleurs et points
(couleur, mark, size) = defsize()

#creation figure
newfig()
ax = plt.gca()

#parametres de la figure sont enregistres dans sub
sub = plt.subplot(1,1,1)

#axe des abscisses 
nmbx = 9           #nombre de traits
xmin = 0       #valeur minimale de x
xmax = 8         #valeur maximale de x

""" NE PAS TOUCHER """

plt.xticks([ i for i in n.linspace(xmin,xmax,nmbx)],
    [r'${}%.0f$'%(i) for i in n.linspace(xmin,xmax,nmbx)]) 
plt.xlim([xmin, xmax])

""" FIN NE PAS TOUCHER """

#nom de la variable en abscisse
plt.xlabel(r'$x$')

#petits traits intermediaires
minorLocator = AutoMinorLocator(2)          #changer le nombre de petits traits
ax.xaxis.set_minor_locator(minorLocator)    #a enlever si vous ne voulez pas de petits traits

#axe des ordonnees
nmby = 7	
ymin = -6 #n.min(O)*0.99
ymax = 6 #n.max(O)*1.01

#si vous voulez l'echelle log
#plt.yscale('log')

""" NE PAS TOUCHER """

plt.yticks([i for i in n.linspace(ymin,ymax,nmby)],
	[r'%.0f'%(i) for i in n.linspace(ymin,ymax,nmby)])
plt.ylim(ymin, ymax)

""" FIN NE PAS TOUCHER """

#nom de la variable en ordonnee
plt.ylabel(r'$y(x)$')

#petits traits intermediaires
minorLocator = AutoMinorLocator(2)
ax.yaxis.set_minor_locator(minorLocator)
               
#points experimentaux
m = 3
plt.plot(t[::m], 
                 O[::m]-pe,
                 markersize = size[0],
                 marker     = mark[0],
                 color      = couleur[0], 
                 linestyle  = '',
                 )

plt.plot(np.linspace(min(t),max(t),1000),              #abscisse
         funct([popt[0],0,n.pi/2,popt[3],popt[4]],np.linspace(min(t),max(t),1000))-pe,  #ordonnee
         color      = couleur[1],   #couleur de la courbe, mettre le numero voulu
#         label      = r'$\chi^2=%.2f$ '%(chi2)
         )

plt.plot(np.linspace(min(t),max(t),1000),              #abscisse
         funct([popt[0],0,3*n.pi/2,popt[3],popt[4]],np.linspace(min(t),max(t),1000))-pe,  #ordonnee
         color      = couleur[1],   #couleur de la courbe, mettre le numero voulu
#         label      = r'$\chi^2=%.2f$ '%(chi2)
         )

X = np.linspace(min(t),7.73,14)
plt.plot(X,              #abscisse
         funct(popt,X)-pe,  #ordonnee
         color      = couleur[1],
		 linestyle = '',
		 markersize   = size[1],
		 marker 	= mark[1]   #couleur de la courbe, mettre le numero voulu
#         label      = r'$\chi^2=%.2f$ '%(chi2)
         )

#save the figure
figsave('Ajustement_ruchard_m0_scope_1')   #changer le nom de la figure

#plt.show()
