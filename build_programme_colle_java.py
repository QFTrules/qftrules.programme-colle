# coding=utf-8
import sys
import sys
with open(sys.argv[1], 'r') as f:
    found  = False
    entete = False
    lookforentete = False
    type   = None
    theme  = '{1}'
#    enviro = False
    secname = []
    with open(sys.argv[2],'a') as g:
        #g.write('\\documentclass[12pt,fancy]{$HOME/Dropbox/.latex/Preambles/progcolle}%$\n\\input{$HOME/Dropbox/.latex/Preambles/programme.tex}%$\n\\Theme{4}\\Chapit{4}{1}\\cover{meca.jpg}\n\\begin{document}\n\\dominitoc\\maketitre{}')
        #g.write('\\input{$HOME/Dropbox/.latex/Preambles/progcolle.sty}%$\n\\input{$HOME/Dropbox/.latex/Preambles/programme.tex}%$\n\\begin{document}\n\\tableofcontents\n')
        linenumber = 0
        for line in f:
            linenumber += 1
            try:
                if 'devoir.sty' in line:
                    type = 'devoir'
                if 'TD.sty' in line or 'TDappli.sty' in line:
                    type = 'td'
                if 'TP.sty' in line:
                    type = 'tp'
                if '\\begin{document}' in line:
                    found = False
                if '\\Chapit{' in line:
                    i = line.index('{')
                    g.write('\\subtitle{\\ChapitName' + line[i:] + '}')
                if '\\Entete' in line or lookforentete:
                    entete = True
                    if type == 'td':
                        try:
                            i = line.index('[')
                            j = line.index(']')
                            k = line[j+1:].index('[')
                            l = line[j+1:].index(']')
                            m = line[l+j+2:].index('[')
                            n = line[l+j+2:].index(']')
                            # print(m,n)
                            #g.write('\\subsection{\\ChapitTD{' + line[i+1:j] + '}{' + line[k+1:l] + '}}\n')
                            # g.write('\\ChapitTD{' + line[i+1:j] + '}{' + line[k+1:l] + '}\n')
                            g.write('\\ChapitTD{' + line[m+l+j+3:n+l+j+2] + '}{' + line[k+j+2:l+j+1]  + '}\n')
                            # print('\\ChapitTD{' + line[k+j+2:l+j+1] + '}{' + line[m+l+j+3:n+l+j+2] + '}\n')
                        except(ValueError):
                            continue
                    if type == 'tp':
                        try:
                            i = line.index('{')
                            j = line.index('}')
                            lookforentete = False
                            # k = line[i+1:].index('{')
                            # l = line[j+1:].index('}')
                            # theme = line[i+1+k:j+1+l+1]
                        except(ValueError):
                            lookforentete = True
                            continue
                    # else:
                    theme = line[i:j+1]
                if found:
                    if entete and not type == 'devoir' and not type == 'td':
                        if type == 'tp':
                            # \TPName
                            # g.write('\\subsection' + theme + '\n')
                            g.write('\\subsection{~\\TPName' + theme + '}\n')
                        else:
                            g.write('\\Theme' + theme + '\n')
                        entete = False
                    #if '\\Chapit' in line:# and type == 'td':
                        #i = line.index('{')
                        #j = line.index('}')
                        #g.write('\\subsubsection' + line[i+1:j] + '\n')
                    if ('\\section' in line or '\\subsection' in line) and not '%' in line and not type == 'tp':
                        k = line.index('\\')
                        i = line.index('{')
                        j = line.index('}')
                        g.write('\\sub' + line[k+1:])
                        # if '\\section' in line:
                        #     g.write('\\subsection{' + line[i+1:j])
                        # if '\\subsection' in line:
                        #     g.write('\\subsubsection{' + line[i+1:j])
                        secname.append(line[i+1:j])
                    if '\\section' in line and not '%' in line and type == 'tp':
                        # if '\\bonus' in line:
                        #     i = line.index('\\bonus')
                        #     line = line[:i] + '}\n'
                        if '\\technique' in line:
                            i = line.index('\\technique')
                            line = line[:i]
                        k = line.index('\\')
                        i = line.index('{')
                        j = line.index('}')
                        g.write('\\subsub' + line[k+1:])
                    if '\\subsection' in line and not '%' in line and type == 'tp':
                            i = line.index('{')
                            j = line.index('}')
                            g.write('\\paragraph' + line[i:j+1] + '\n')
                    if '\\parag' in line and not '%' in line:
                        i = line.index('{')
                        j = line.index('}')
                        if not line[i+1:j] in secname[-1]:
                            g.write('\\paragraph' + line[i:j+1] +'\n')
                        secname.append(line[i+1:j])
                    if '\\begin{theorem}' in line and not '%' in line:
    #                    environ = True
                        i = line.index('[')
                        j = line.index(']')
                        if not line[i+1:j] in secname and not line[i+2:j] in secname[-1] and not "nonc" in secname[-1]:
                            g.write('\\paragraph{\\textit{Formule : ' + line[i+1:j] +'}}\n')
                            secname.append(line[i+1:j])
                    if '\\begin{exemple}' in line and not '%' in line:
                        i = line.index('}')
                        j = -1
                        g.write('\\paragraph{' + '\\textit{Exemple : ' + line[i+2:j] +'}\n')
                        secname.append(line[i+2:j-1])
                    if ('\\Ex{' in line or '\\Ex[' in line) and not '%' in line:
                        i = line.index('{')
                        j = line.index('}')
                        if type == 'devoir':
                            g.write('\\subsection{' + line[i+1:j] +'}\n')
                        else:
                            if 'numérique' in line:
                                g.write('\\subsubsection{' + line[i+1:j] +'~\\faPython}\n')
                            else:
                                g.write('\\subsubsection{' + line[i+1:j] +'}\n')
                    # if '\\docu{' in line:
                    #     i = line.index('{')
                    #     j = line.index('}')
                    #     g.write('\\paragraph{\underline{Analyse Documentaire} : ' + line[i+1:j] + '}\n')
                if ('\\ProgrammeColle' in line and not '\\%' in line) or '\\end{document}' in line:
                    found = not found
            except:
                filename = sys.argv[1].split('/')[-1]
                # print('Error on line ' + str(linenumber) + ' in file ' + filename)
        #g.write('\\end{document}')
    #print(secname)
    g.close()
f.close()
