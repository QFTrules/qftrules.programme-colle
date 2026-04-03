# Python code for 2D random walk.
import numpy
import pylab
import random
# from figure import *
import matplotlib as mpl 

Fsize   = int(20)     # Big size, which corresponds to the size of the legend in latex (/small)
fsize   = int(20)
pgf_with_latex = {                       # Setup matplotlib to use latex for output
        "pgf.texsystem":   "pdflatex",       # Change this if using xetex or lautex
        "text.usetex":     True,             # Use LaTeX to write all text
        "font.family":     "serif",
        "font.serif":      [],               # Blank entries should cause plots to inherit fonts from the document
        "font.sans-serif": [],
        "font.monospace":  [],
        "axes.labelsize":  Fsize,            # Here is the default font size (10pt, 11pt or 12pt typically)
        "font.size":       Fsize,
        "legend.fontsize": Fsize,            # Make the legend/label fonts a little smaller
        "xtick.labelsize": Fsize,
        "ytick.labelsize": Fsize,
        "pgf.preamble": [
            r"\usepackage[utf8x]{inputenc}", # Use utf8 fonts because your computer can handle it :)
            r"\usepackage[T1]{fontenc}",     # Plots will be generated using this preamble
        ]
    }

    # Set the new params to default
mpl.rcParams.update(pgf_with_latex)
    
# defining the number of steps
n = 5000

#creating two array for containing x and y coordinate
#of size equals to the number of size and filled up with 0's
x = numpy.zeros(n)
y = numpy.zeros(n)
t = 0
dt = 0.01
line, = pylab.plot(x, y)

lim = 1*numpy.sqrt(n)
pylab.xlim(-lim,lim)
pylab.ylim(-lim,lim)

pylab.ion() # mode interaction on

# filling the coordinates with random variables
for i in range(1, n):
	t = t + dt
	val = random.randint(1, 4)
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
	# update only the filled portion so the line isn't closed to remaining (zero) points
	line.set_xdata(x[:i+1])
	line.set_ydata(y[:i+1])
	#pylab.draw()
	if i%int(numpy.log10(n)*2) == 0:
		#pylab.show()
		pylab.pause(1/3/n)
xf,yf = x[-2],y[-1]

pylab.ioff()
# plotting stuff:

pylab.xlabel(r'$x$')
pylab.ylabel(r'$y$')
pylab.title(r"Marche aléatoire ($N = " + str(n) + r"$ sauts)")
pylab.plot(x, y)
pylab.plot(xf, yf, 'r')
pylab.savefig("rand_walk"+str(n)+".pdf",bbox_inches="tight",dpi=500)
pylab.show()
