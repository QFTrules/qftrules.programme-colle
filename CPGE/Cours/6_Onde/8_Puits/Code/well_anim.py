from cmath import exp, pi
from numpy import sqrt
from vpython import color, gcurve, graph, rate, sin


g1 = graph(
  title="Probability Density",
  xtitle="x (m)",   # LaTeX math mode for x
  ytitle="rho",       # LaTeX math mode for P
  width=1000,
  height=500,
  ymax=2,
  ymin=0
)

f1 = gcurve(color=color.blue, graph=g1)



a = 1       # largeur du puits
m = 1       # masse de la particule
hbar = 1    # constante de Planck réduite

def omega(n):
  return (n*pi/a)**2*hbar/2/m

def phi(n,x):
  return sqrt(2/a)*sin(n*pi*x/a)


def psi(x,t):
  psi = 0
  for n in range(2):
    psi += phi(n,x) * exp(-1j*omega(n)*t)
  return psi


x = 0
dx = 0.01
t =0
dt = 0.001

while t < 5:
  rate(100)
  data = []
  x = 0 
  while x<a:
    data = data + [[x,psi(x,t)]]
    x = x + dx
  # Draw vertical lines at x=0 and x=a by plotting multiple points along y
  for y in [i * 0.05 for i in range(41)]:  # y from 0 to 2 in steps of 0.05
    f1.plot(pos=(0, y))
    f1.plot(pos=(a, y))
  f1.plot(pos=data)
  t = t + dt