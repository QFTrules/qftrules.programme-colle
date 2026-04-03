G = 6.67e-11
N = ['Me', 'Ve', 'Te', 'Ma']
M = [3e23, 5e24, 6e24, 6e23]
R = [58e6, 110e6, 150e6, 230e6]
MS = 2e30
V = [(G * MS / (R[i]*1000))**0.5/1000 for i in range(len(M))]
V = [50, 35, 30, 24]
L = [M[i] * R[i] * V[i] for i in range(len(M))]

for i in range(len(M)):
    print(N[i], M[i], 'kg', R[i], 'km', V[i], 'km/s',L[i], 'kg.km^2/s')
