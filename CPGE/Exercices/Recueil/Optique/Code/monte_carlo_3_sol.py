fmoy    = np.mean(fp)       # valeur moyenne de f'
Deltaf  = np.std(fp,ddof=1) # écart-type de la distribution de f'
print("f' = (%.1f \pm %.1f) cm"%(fmoy,Deltaf))
