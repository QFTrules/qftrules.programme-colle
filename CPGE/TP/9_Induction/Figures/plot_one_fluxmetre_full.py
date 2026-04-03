"""
Ce code permet de selectionner le profil de tension induite dans le deuxieme fluxmetre (celui en bas du cyclindre)
en detectant le zero puis translatant les courbes par rapport a cette nouvelle origine des temps pour chaque essai. Enfin
on moyenne le profil sur tous les essais et on traite les donnees (calcul de l'aire = flux maximal, ajustement).

"""

#module de base pour les figures
from doublefigure import *
import sys 
#from scipy.integrate import simps

#dictionnaire pour les couleurs et points
(couleur, mark, size) = defsize()

#creation figure
newfig()
ax = plt.gca()

#parametres de la figure sont enregistres dans sub
sub = plt.subplot(1,1,1)

def crossings(data):
    pos = data > 10**(-1)
    return (pos[:-1] & ~pos[1:]).nonzero()[0]
    
def neg_crossings(data):
    pos = data < 10**(-1)
    return (pos[:-1] & ~pos[1:]).nonzero()[0]
    
def corrected_cross(data):
    zeros1 = crossings(data)
    zeros2 = neg_crossings(data)
    purged = []
    denied = False
    for i in zeros1:
        for j in zeros2:
            if n.abs(i - j) < 20:
                denied = True
                break
        if denied:   
            denied = False
        else:
            purged.append(i)
            
    return purged

# Fit functions
def g(x,f0,tau):
	return -f0*(x*tau**4)/(x**2+tau**2)**(5/2)
def f(x,f0,tau,x0):
	return -f0*tau**3*(1/((x-x0)**2+tau**2)**(3/2)-1/((x+x0)**2+tau**2)**(3/2))

# Number of magnets whose data you want to plot
Index = int(sys.argv[1])

# List of index-related parameters
Indices  = {2:[1,7],5:[7,13],10:[13,18],20:[19,23]}
Duration = {2:1,5:1,10:1,20:0.5}
Ymax     = {2:30,5:80,10:150,20:300}
Nmby     = {2:7,5:9,10:7,20:7}
print('\nThe number of magnets is %.i'%(Index))


#load the first st of data
for i in range(Indices[Index][0],Indices[Index][1]):
	data = n.loadtxt('%.iaimants_%.i.csv'%(Index,i), 	#nom du fichier avec les donnees
                     skiprows = 2)  			#pour sauter la premiere ligne
	print('    File %.iaimants_%.i.csv read'%(Index,i))
	t    = data[:,0]-data[0,0]      			#(s)
	dt   = t[1]
	T    = int(Duration[Index]/dt)

	#change the sign of U if needed
	if (i == 2) or (i == 5) or (i == 7) or (i == 9) or (i == 13) or (i == 20) or (i == 22):
		U = (data[:,1]-data[0,1])*10**3    #(mV) 
	else:
		U = -(data[:,1]-data[0,1])*10**3
	N = n.shape(t)[0]         #taille de la liste   
		         
	#incertitudes
	z_err   = 0.1
	t_err   = n.zeros(N) + 0.01
	U_err   = n.zeros(N) + 0.0001

	#lists of zeros, dt=t[1] is the time step
	cross    = n.array(corrected_cross(U))

	""" FIN NE PAS TOUCHER """

	#axe des abscisses 
	nmbx = 5                 #nombre de traits
	xmin = -Duration[Index]   #valeur minimale de x
	xmax = Duration[Index]    #valeur maximale de x


	plt.xticks([ i for i in n.linspace(xmin,xmax,nmbx)],
		[str('%.1f'%(i)).replace('.',',') for i in n.linspace(xmin,xmax,nmbx)]) #changer .0f en le nombre de chiffres apres la virgule necessaire

	#si jamais vous voulez modifier l'intervalle des axes a la main:
	plt.xlim([xmin, xmax])

	#nom de la variable en abscisse
	plt.xlabel(r'$t$ (s)')

	#petits traits intermediaires
	minorLocator = AutoMinorLocator(2)          #changer le nombre de petits traits
	ax.xaxis.set_minor_locator(minorLocator)    #a enlever si vous ne voulez pas de petits traits

	#axe des ordonnees
	nmby = Nmby[Index]
	ymin = -Ymax[Index]
	ymax = Ymax[Index]

	#si vous voulez l'echelle log:
	#plt.yscale('log')

	plt.yticks([i for i in n.linspace(ymin,ymax,nmby)],
		[r'${}%.0f$'%(i) for i in n.linspace(ymin,ymax,nmby)])
	plt.ylim(ymin, ymax)
	#nom de la variable en ordonnee
	plt.ylabel(r'$U$ (mV)')

	#petits traits intermediaires
	minorLocator = AutoMinorLocator(2)
	ax.yaxis.set_minor_locator(minorLocator)
    
    #si vous avez besoin de mettre les axes origines
    #ax.axhline(y = 0, color = 'k', linewidth = 0.2)
    #ax.axvline(x=0, color='k', linewidth = 0.2)
	if (i == Indices[Index][0]):
		Utot = n.array([U[j]/(Indices[Index][1]-Indices[Index][0]) for j in range(cross[1]-int(Duration[Index]/dt),cross[1]+int(Duration[Index]/dt))])
	else:
		Utot += n.array([U[j]/(Indices[Index][1]-Indices[Index][0]) for j in range(cross[1]-int(Duration[Index]/dt),cross[1]+int(Duration[Index]/dt))])

#	plt.plot(n.linspace(-0.5,0.5,int(1/dt)),
#		 n.array([U[i] for i in range(cross[1]-int(0.5/dt),cross[1]+int(0.5/dt))]),
#		 color = couleur[i-23]
#		 )

# axe U=0
plt.plot([xmin,xmax],
             [0,0],
             color = 'black',
             linewidth = 0.2)

# correction to the position of the zero
corr = Utot[T]/(Utot[T]-Utot[T+2])*dt


plt.plot(n.linspace(-Duration[Index]-corr,Duration[Index]-corr, 2*T),
		 Utot,
		 color = couleur[0],
		 marker = mark[0],
		 markersize = size[0],
		 linestyle = ''
		 )

#plt.plot([], [], linestyle =  '', label = r'$f(t,t_0)=\frac{1}{((t-t_0)^2+\tau^2)^{3/2}}$')

# ajustement
if (Index == 2):

	# ajustement
	popt, pcov = opt.curve_fit(g, n.linspace(-Duration[Index]-corr,Duration[Index]-corr, 2*T), Utot)
	
	plt.plot(n.linspace(-Duration[Index],Duration[Index],2000),
		g(n.linspace(-Duration[Index],Duration[Index],2000), popt[0], popt[1]),
		color = couleur[1],
		linestyle = '-',
		markersize = 0,
		label = r'$U(t) = U_0 g(t,\tau)$'
		)
else:

	# ajustement
	popt, pcov = opt.curve_fit(f, n.linspace(-Duration[Index]-corr,Duration[Index]-corr, 2*T), Utot)
	
	plt.plot(n.linspace(-Duration[Index],Duration[Index],2000),
		f(n.linspace(-Duration[Index],Duration[Index],2000), popt[0], popt[1], popt[2]),
		color = couleur[1],
		linestyle = '-',
		markersize = 0,
		label = r'$U(t) = U_0 f(t,\tau,t_0)$'
		)

plt.text(0.1,ymax*2/3,r'$U_0 = %.0f~$V'%(popt[0]))
plt.text(0.1,ymax*(2/3-0.2),r'$\tau = %.3f~$s'%(abs(popt[1])))
if (Index == 2):
	print('\n    U_0 = %.3f\n    tau = %.3f'%(popt[0], abs(popt[1])))
else:
	print('\n    U_0 = %.3f\n    tau = %.3f\n    t_0 = %.3f'%(popt[0], abs(popt[1]), popt[2]))
	plt.text(0.1,ymax*(2/3-0.4),r'$t_0 = %.3f~$s'%(popt[2]))

# representation de l aire sous la courbe
Integr = sum(Utot[:T])*dt
print('\n    Flux = %.3f Wb'%(Integr))
plt.fill_between(n.linspace(-Duration[Index],0,T), 
				 Utot[:T], 
				 color     ="skyblue", 
				 alpha     = 0.4, 
				 label     = r'$\Phi_{\rm max} = %.3f~$Wb'%(Integr), 
				 linewidth = 0)

#legende
leg(sub,                #NE PAS TOUCHER
	'lower left')       #position de la legende sur le qraphe


	#save the figure
figsave('%.iaimants'%(Index))   #changer le nom de la figure
