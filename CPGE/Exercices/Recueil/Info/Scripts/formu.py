# max : détermine le maximum parmi les éléments d'une liste
max([0,5,-2,3])
>> 5

# min : détermine le minimum parmi les éléments d'une liste
min([0,5,-2,3])
>> -2

# liste par compréhension
[2*i for i in [1,2,3]]
>> [1,4,6]

# condition d'égalité
1 == 2
>> False
[1,2] == []
>> False
[] == []
>> True

# opérateur ET
False and True
>> False
True and True
>> True

# dictionnaire
dico = {(1,1):[(2,2),(2,3),(2,4)]}
dico[(1,1)]
>> [(2,2),(2,3),(2,4)]
