import sys
#with open('/home/eb/Dropbox/Colles/2021/folder.tmp', 'r') as fold:
#    for line in fold:
#        dossier = line[-11:]
#fold.close()
USB     = 'USB STICK'
fichier = sys.argv[1]
date    = sys.argv[2]
nextdate = sys.argv[3]
fiche_latex    = sys.argv[4]
tmp = sys.argv[5]
double  = False
triple  = False
datefound = False
if 'pc' in fichier:
    classe = 'PC'
if 'pcsi' in fichier:
    classe = 'PCSI'
with open(fichier, 'r') as f:
    section = []
    cours   = []
    for line in f:
        if '\\Triple' == line[:7]:
            triple = True
        if '\\Double' == line[:7]:
            double = True
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
    # cours = cours[::-1]
    # section = section[::-1]
    # # print(section)
    # if double:
    #     with open(path + '/Dropbox/texmf/tex/latex/Preambles/Fiche_double.tex','r') as g:
    #         with open('Fiche_tmp_double.tex','w') as h:
    #             # h.write('\\renewcommand{\\classe}{' + classe + '}\n')
    #             # h.write('\\lhead{\\small \\classe}\n')
    #             for line in g:
    #                 if '\\flushright{Date : \\hspace{2cm}}' in line:
    #                    # h.write('\\flushright{Date : ' + date + '}')
    #                     h.write('\\flushright{Date : ' + date + '}')
    #                 else:
    #                     h.write(line)
    #                     if '\\input{' in line:
    #                         h.write('\\renewcommand{\\classe}{' + classe + '}\n')
    #                     if '\\begin{document}' in line:
    #                         # h.write('\n\n\\newcommand{\Coursun}{' + cours[0] + '}\n\\newcommand{\Coursdeux}{' + cours[1] + '}\n\\newcommand{\Courstrois}{' + cours[2] + '}\n\\newcommand{\Exoun}{' + section[0] + '}\n\\newcommand{\Exodeux}{' + section[1] + '}\n\\newcommand{\Exotrois}{' + section[2] + '}\n\n')
    #                         h.write('\n\n\\newcommand{\Coursun}{' + cours.pop() + '}\n\\newcommand{\Coursdeux}{' + cours.pop() + '}\n\\newcommand{\Courstrois}{' + cours.pop() + '}\n\\newcommand{\Exoun}{' + section.pop() + '}\n\\newcommand{\Exodeux}{' + section.pop() + '}\n\\newcommand{\Exotrois}{' + section.pop() + '}\n\n')
    #         h.close()
    #     g.close()
    #     double = False
    # elif triple:
    #     with open(path + '/Dropbox/texmf/tex/latex/Preambles/Fiche_triple.tex','r') as g:
    #         with open('Fiche_tmp_triple.tex','w') as h:
    #             # h.write('\\renewcommand{\\classe}{' + classe + '}\n')
    #             # h.write('\\lhead{\\small \\classe}\n')
    #             for line in g:
    #                 if '\\flushright{Date : \\hspace{2cm}}' in line:
    #                     # h.write('\\flushright{Date : ' + date + '}')
    #                     h.write('\\flushright{Date : ' + date + '}')
    #                 else:
    #                     h.write(line)
    #                     if '\\input{' in line:
    #                         h.write('\\renewcommand{\\classe}{' + classe + '}\n')
    #                     if '\\begin{document}' in line:
    #                         h.write('\n\n\\newcommand{\Coursun}{' + cours[0] + '}\n\\newcommand{\Coursdeux}{' + cours[1] + '}\n\\newcommand{\Courstrois}{' + cours[2] + '}\n\\newcommand{\Exoun}{' + section[0] + '}\n\\newcommand{\Exodeux}{' + section[1] + '}\n\\newcommand{\Exotrois}{' + section[2] + '}\n\n')
    #         h.close()
    #     g.close()
    #     triple = False
    # cours = cours[::-1]
    # section = section[::-1]
    # if len(cours) > 0:
    with open(fiche_latex,'r') as g:
        with open(tmp + 'Fiche_tmp_simple.tex','w') as h:
            # h.write('\\renewcommand{\\classe}{' + classe + '}\n')
            # h.write('\\lhead{\\small \\classe}\n')
            for line in g:
                if '\\flushright{Date : \\hspace{2cm}}' in line:
                    if datefound:
                        h.write('\\flushright{Date : ' + nextdate + '}')
                    else:
                        h.write('\\flushright{Date : ' + date + '}')
                        datefound = True
                else:
                    h.write(line)
                    if '\\input{' in line:
                        h.write('\\renewcommand{\\classe}{' + classe + '}\n')
                    if '\\begin{document}' in line:
                        h.write('\n\n\\newcommand{\Coursun}{' + cours[0] + '}\n\\newcommand{\Coursdeux}{' + cours[1] + '}\n\\newcommand{\Courstrois}{' + cours[2] + '}\n\\newcommand{\Exoun}{' + section[0] + '}\n\\newcommand{\Exodeux}{' + section[1] + '}\n\\newcommand{\Exotrois}{' + section[2] + '}\n\n')
        h.close()
    g.close()
f.close()
