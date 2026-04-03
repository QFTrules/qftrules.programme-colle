norme2 = calc_norme(T_tous_k[:,1]-T_tous_k[:,0])
while (k<ItMax-1 and norme2>0.01):
    T_tous_k[0,k+1] = r*Tint+(1-2*r)*T_tous_k[0,k]+r*T_tous_k[1,k]     # point x1
    for i in range(1,N-1) :     # point x i+1
          T_tous_k[i,k+1] = r*T_tous_k[i-1,k]+(1-2*r)*T_tous_k[i,k]+r*T_tous_k[i+1,k]
    T_tous_k[N-1,k+1] = r*T_tous_k[N-2,k]+(1-2*r)*T_tous_k[N-1,k]+r*Text2     # point xN
    norme2 = calc_norme(T_tous_k[:,k+1]-T_tous_k[:,k])
    k += 1 # itération k+1 terminée
