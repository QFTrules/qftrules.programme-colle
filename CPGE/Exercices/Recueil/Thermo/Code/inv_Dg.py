invDg=inv_mat(mat_Dg(x_old))
T_new=x_old[0] - invDg[0,0]*g1(x_old[0],x_old[1]) - invDg[0,1]*g2(x_old[0],x_old[1])
X_new=x_old[1] - invDg[1,0]*g1(x_old[0],x_old[1]) - invDg[1,1]*g2(x_old[0],x_old[1])
x_new=[T_new,X_new]