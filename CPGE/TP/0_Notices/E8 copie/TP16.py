import numpy as np
import matplotlib.pyplot as plt

## non inverseur

t = np.linspace(0,3,100)
ve = 0.5*np.sin(2*np.pi*t)
vs = 11*ve
plt.plot(t,ve)
plt.plot(t,vs)
plt.grid()
plt.xlabel('t(ms)')
plt.ylabel('tensions (V)')
plt.legend(['ve(t)','vs(t)'])
plt.show()

def vs(t):
    vs = np.zeros([len(t)])
    for k in range(len(t)) :
        if 11*3*np.sin(2*np.pi*t[k]) < -15 :
            vs[k] = -15
        elif 11*3*np.sin(2*np.pi*t[k]) > 15 :
            vs[k] = 15
        else :
            vs[k] = 11*3*np.sin(2*np.pi*t[k])
    return vs
    
t = np.linspace(0,3,1000)
ve = 3*np.sin(2*np.pi*t)
vs = vs(t) 
plt.grid()
plt.plot(t,ve)
plt.plot(t,vs)
plt.show()



