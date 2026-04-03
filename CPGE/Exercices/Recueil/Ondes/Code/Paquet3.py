def omega(k):
    omegap = 5
    c = 1
    return (k**2*c**2+omegap**2)**0.5

def s_temps(k, X, A, t):
    s = np.zeros(len(X), dtype=np.complex_)
    for i in range(len(k)):
        s += ...
    return np.real(s)
