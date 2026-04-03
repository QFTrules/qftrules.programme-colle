def couleur(y, d):
    if d(y,(0,0)) < 0.5:
        return 'rouge'
    else:
        return 'bleu'

p  = {y:couleur(y,d) for y in E}

xr = [y[0] if p[y]=='rouge' for y in E]
yr = [y[1] if p[y]=='rouge' for y in E]
xb = [y[0] if p[y]=='bleu' for y in E]
yb = [y[1] if p[y]=='bleu' for y in E]
plt.plot(xr,yr,'rd')
plt.plot(xb,yb,'bd')
plt.show()
