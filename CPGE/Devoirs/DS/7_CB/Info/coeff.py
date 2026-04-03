def coeff_normalise(data):
    L = []
    for i in range(len(data[0])):
        colonne = [data[j][i] for j in range(len(data))] # si data n'est pas un tableau numpy ; sinon colonne=data[:, i]
        mini,maxi = min_max(colonne)
        a = 1/(maxi-mini)
        b = -mini/(maxi-mini)
        L.append([a,b])
    return L

def distance(z, data):
    coef = coeff_normalise(data)
    distances = []
