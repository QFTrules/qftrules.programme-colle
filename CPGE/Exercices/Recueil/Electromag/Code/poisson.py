def poisson(f_iter, V, rhos, frontiere, eps):
    err = 2*eps # on donne une valeur a priori plus grande que la valeur d'arrêt
            # afin que la boucle s'exécute au moins une fois
    while err >= eps:
        err = f_iter(V, rhos, frontiere)
    # la fonction n'a pas de return car elle modifie le tableau V "en place"