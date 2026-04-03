""" NE PAS TOUCHER """

#module de base pour les figures
from doublefigure import *
from scipy.signal import argrelextrema
#import scipy.optimize as spo

#load the first set of data
data = n.loadtxt('m0/scope_1.txt',skiprows=2)
# definitions
i=1
scope = str(int(i))
temps = data[:,0]
resol = 1
dt = (data[1,0]-data[0,0])*resol
print('dt=', dt)
V = data[:,1]


# importation des bornes d'ajustement
folder = 'm0'
bornes = n.loadtxt(folder+'/bornes_'+folder+'.txt',skiprows=1)
pe     = n.loadtxt(folder+'/ajust_'+folder+'.txt',skiprows=1)[:,8]
bornemin = bornes[:,0]
bornemax = bornes[:,1]

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
		'Pression equilibre      pe = %.2f'%popt[4], '+- %.2f'%uopt[4], 'hPa', '\n' +
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
xmax = 8        #valeur maximale de x

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
nmby = 5	
ymin = 0 #n.min(O)*0.99
ymax = 2 #n.max(O)*1.01

#si vous voulez l'echelle log
#plt.yscale('log')

""" NE PAS TOUCHER """

plt.yticks([i for i in n.linspace(ymin,ymax,nmby)],
		[str('{}%.1f'%(i)).replace('.',',') for i in n.linspace(ymin,ymax,nmby)])
plt.ylim(ymin, ymax)
#plt.yscale('log')


""" FIN NE PAS TOUCHER """

#nom de la variable en ordonnee
plt.ylabel(r'$\ln(\vert y_{\rm extr}\vert)$')

#petits traits intermediaires
minorLocator = AutoMinorLocator(2)
ax.yaxis.set_minor_locator(minorLocator)
               
# bornes
i=1

bmin = int(bornemin[int(i)])
bmax = int(bornemax[int(i)])

# donnees experimentales
y = P[bmin:bmax:resol]
x = temps[bmin:bmax:resol]

#averaging
pas = 10
Y = n.linspace(0,1,(bmax-bmin-2*pas)//resol)
sigma = n.linspace(0,1,(bmax-bmin-2*pas)//resol)
for j in range(0,(bmax-bmin-2*pas)//resol):
	Y[j] = sum(y[j-pas:j+pas])/(2*pas)
	sigma[j] =  n.sqrt(sum([(y[a]-y[j])**2 for a in range(j-pas,j+pas)])/(2*pas))

#	pas = 5
#	extr = [[-1000,0]]
#	for j in range(0,int((bmax-bmin)/pas)) :
#		if (n.abs(y[pas*j]-y[pas*(j-1)]) < 0.25) and (x[pas*j]-extr[-1][0] > 0.3) :
#			extr.append([x[pas*j],y[pas*j]])

#	print(extr
result_max = argrelextrema(Y, np.greater)[0]
result_min = argrelextrema(Y, np.less)[0]
Xmax = result_max
Ymax = P[result_max]
Xmin = result_min
Ymin = P[result_min]
Xmax = list(Xmax[Ymax>pe[i]])
#	Ymax = list(Ymax[Ymax>pe[i]])
Xmin = list(Xmin[Ymin<pe[i]])
#	Ymin = list(Ymin[Ymin<pe[i]])

Xextr = n.array(Xmax+Xmin)
Xextr.sort()
#	Yextr = n.array(Ymax+Ymin)
Yextr = P[Xextr]
Yextr_err = sigma[Xextr]/2
print(Yextr_err)

#pe moyen

PE = sum(P[bmax-100:bmax])/100
dPE = n.sqrt(sum((P[bmax-100:bmax]-PE)**2)/99)
print('pe = ', PE, 'dpe = ', dPE)

# ecriture des resultats
#	output.write('\n{0:.3e}	{1:.3e}	{2:.3e}	{3:.3e}	{4:.3e}	{5:.3e}	{6:.3e}	{7:.3e}	{8:.3e}	{9:.3e}'.format(popt[0],uopt[0],popt[1],uopt[1],popt[2],uopt[2],popt[3],uopt[3],popt[4],uopt[4]))


#print(Xextr,Yextr,pe[i])

(a0, a_err, b0,b_err,chi2) = fit_affine(Xextr[1:15]*dt,     #abscisse
                                      n.log(n.abs(Yextr-PE))[1:15],     #ordonnee
                                      Xextr[1:15]*0.0000001*dt, #incertitude abscisse
                                      n.array([Yextr_err[a]/(Yextr[a]-PE) for a in range(1,15)])) #incertitude ordonnee
                                      
#print the results of the fit
print('Decrement log\n' +   '   pente    = %.3e +/- %.1e\n' %(a0, a_err)
  + '   ordonnee = %.3e +/- %.1e\n' %(b0, b_err)
  + '   chi2     = %.3f\n' % chi2)

#plt.plot(n.array([0,12]),              #abscisse
#	     n.exp(a0*n.array([0,12])+b0)
#		     color      = couleur[1],   #couleur de la courbe, mettre le numero voulu
#         label      = r'$\chi^2=%.2f$ '%(chi2)
#	     )
plotcurve(size, mark, couleur,    #NE PAS TOUCHER
        n.array([0,12]),                                      #abscisse
        a0*(n.array([0,12])+Xextr[0]*dt)+b0,                                 #ordonnee
        ID   = 1                               #numero du type de points
        )

#points experimentaux
ploterr(size, mark, couleur,    #NE PAS TOUCHER
	  			 (Xextr-Xextr[0])*dt,
	             n.log(n.abs(Yextr-PE)),
				 Xextr*0,
				 n.abs(Yextr-PE)/Yextr_err/240,
	             ID = 1
	             )


#save the figure
figsave('Ruchardt_decrement')   #changer le nom de la figure

#plt.show()
