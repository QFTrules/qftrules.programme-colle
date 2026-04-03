def mat_Dg(x):
    Dg=np.zeros((2,2)) 
    Dg[0,0]=g_1 T(x[0], x[1]) 
    Dg[0,1]=g_1 x(x[0], x[1]) 
    Dg[1,0]=g_2 T(x[0], x[1]) 
    Dg[1,1]=g_2 x(x[0], x[1])
    return Dg