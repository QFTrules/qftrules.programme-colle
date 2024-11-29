import sys
#with open('/home/eb/Dropbox/Colles/2021/folder.tmp', 'r') as fold:
#    for line in fold:
#        dossier = line[-11:]
#fold.close()
USB     = 'USB STICK'
fichier = sys.argv[1]
date    = sys.argv[2]
nextdate = sys.argv[3]
Fiche    = sys.argv[4]
Tmp = sys.argv[5]
# count = 1
if 'pc' in fichier:
    classe = 'PC'
if 'pcsi' in fichier:
    classe = 'PCSI'
with open(fichier, 'r') as f:
    section = []
    cours   = []
    for line in f:
        # if '\\Triple' == line[:7]:
            # count = 3
        # if '\\Double' == line[:7]:
            # count = 2
        if '\\begin{cours}' in line:
            i = line.index('[')
            j = line.index(']')
            cours.append(line[i+1:j])
        if '\\Ex' in line:
            k = line.index('{')
            l = line.index('}')
            section.append(line[k+1:l])
        if '\\begin{Exocolle}' in line:
            i = line.index('[')
            j = line.index(']')
            k = line[i:].index('{')
            l = line[i:].index('}')
            cours.append(line[i+1:j])
            section.append(line[i+k+1:i+l])
    if len(cours) > 0:
        with open(Fiche,'r') as g:
            with open(Tmp,'w') as h:
                for line in g:
                    h.write(line)
                    if '\\begin{document}' in line:
                        h.write('\\newcommand{\\thedate}{' + date + '}\n')
                        h.write('\\newcommand{\\classe}{' + classe + '}\n')
                        h.write('\\newcommand{\Coursun}{' + cours[0] + '}\n\\newcommand{\Coursdeux}{' + cours[1] + '}\n\\newcommand{\Courstrois}{' + cours[2] + '}\n\\newcommand{\Exoun}{' + section[0] + '}\n\\newcommand{\Exodeux}{' + section[1] + '}\n\\newcommand{\Exotrois}{' + section[2] + '}\n\n')
            h.close()
        g.close()
f.close()
# print(count)
