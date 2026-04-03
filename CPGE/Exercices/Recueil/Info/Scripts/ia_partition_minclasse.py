def partition(E, centres, d):
    p = {}                                
    for x in E:                           
        c    = minclasse(x, centres, d)   
        p[x] = centres.index(c)           
    return p 