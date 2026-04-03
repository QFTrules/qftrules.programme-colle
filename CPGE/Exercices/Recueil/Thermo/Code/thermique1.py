def schema_explicite(T0): 
    """
    Calcule l'évolution temporelle du profil de température dans une barre
    selon le schéma explicite.
    Entrée : 
    - T0 : tableau numpy (nd.array) des températures initiales aux N points de
           discrétisation spatiale.
    Sortie :
    - k : entier, nombre d'itérations effectuées.
    - T_tous_k : tableau numpy (nd.array) de dimensions (N, k+1) contenant les
                  profils de température à chaque itération.
    """
