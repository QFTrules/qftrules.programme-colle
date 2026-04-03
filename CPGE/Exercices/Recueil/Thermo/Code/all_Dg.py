t0=0
X0=0
T0=Tp
t_euleri=[t0]
X_euleri=[X0]
T_euleri=[T0]
for i in range(m):
    t_euleri.append(t_euleri[-1]+Deltat)
x_new=[Tp,0]
x_old=[0,0]
for i in range(m):
    while abs(x_new[0]-x_old[0])>1e-5:
        ... # code précédent ici
    X_euleri.append(x_new[0])
    T_euleri.append(x_new[1])