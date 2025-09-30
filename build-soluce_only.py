import sys
import time 
filename = sys.argv[1]
date = sys.argv[2]
# tic = time.perf_counter()
with open(filename, 'r') as f:
    with open(filename[:-4]+'_soluce.tex','w') as g:
        points = []
        quest  = False
        for line in f:
            if '% !TEX root' in line:
                continue
            if '\\begin{document}' in line:
                g.write(line)
                g.write('%--- added by build-soluce_only.py on ' + date + ' ---\n')
                g.write('\\Soluce\n')               # commande qui redéfinit la macro \sol{}, voir préambule symbols.sty 
                g.write('\\SoluceOnly\n') 
                g.write('%----------------------------------------------\n')
                continue
            if '\\ProgrammeColle' in line:
                continue
            if '\\question['  in line :
                quest = True
                i=line.index('[')
                points.append(int(line[i+1:i+2]))
            elif '\\question'  in line and not '%' in line:
                quest = True
                points.append(1)
            if '\\end{document}' in line and quest:
                g.write('\\reversemarginpar\\marginnote{\\raggedleft{\\color{JoliRouge}(%.i~pt.)}}\n'%(sum(points)))
            if '\\begin{Exocolle}' in line:
                i=line.index('[')
                j=line.index(']')
                g.write(line[:j+1] + '[nofig]' + line[j+1:])
                continue
            if '\\Entete' in line:
                g.write('{\\textcolor{gray}Version corrigée du ' + str(date) + '}\n')
            g.write(line)
    g.close()
f.close()
# toc = time.perf_counter()
# print(f"Temps d'exécution de build-soluce.py : {toc - tic:0.4f} secondes")
