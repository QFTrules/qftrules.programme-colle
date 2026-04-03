N  = 10000   # nombre de tirages
fp = []      # liste des valeurs de f'

for i in range(N):
    objet = np.random.uniform(OA-Delta,OA+Delta)    # tirage de OA
    image = np.random.uniform(OAp-Delta,OAp+Delta)  # tirage de OAp
    fp.append(focale(objet,image))                  # calcul de f'
