def minclasse(x, centres, d):
    c    = centres[0]
    dist = d(x,c)
    for y in centres[1:]:
        if d(x,y) < dist:
            c    = y
            dist = d(x,y)
    return c