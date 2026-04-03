k = 1 # itération n°1, instant dt
T_tous_k[0,1] = r*Tint+(1-2*r)*T_tous_k[0,0]+r*T_tous_k[1,0]     # ligne 0 = point x1
for i in range(1,N) :     # ligne i = point x i+1
    T_tous_k[i,1] = r*T_tous_k[i-1,0]+(1-2*r)*T_tous_k[i,0]+r*T_tous_k[i+1,0]
T_tous_k[N,1] = r*T_tous_k[N-1,0]+(1-2*r)*T_tous_k[N,0]+r*Text2     # point xN
