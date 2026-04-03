def distance(z, data) :
    distances=[]
    for i in range(len(data)):
        d=0
        for j in range(len(z)):
            d+=((z[j]-data[i][j]))**2
        distances.append(sqrt(d))
return distances
