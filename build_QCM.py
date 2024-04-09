# coding=utf-8
import sys
cours = sys.argv[1]
template = sys.argv[2]
with open(cours, 'r') as f:
    with open(template,'a') as g:
        prop    = False
        eq      = False
        eqprev  = False
        defini  = False
        formula = False
        quest   = 0
        g.write('\n\n')
        for line in f:
            if line[0] == '%':
                continue
            if '\\begin{theorem}' in line:
                # or '\\begin{prop}' in line:
                g.write('\\begin{question}{' + str(quest) + '}')
                formula = not formula
                quest += 1
                continue
            if '\\end{theorem}' in line:
                # or '\\end{prop}' in line:
                g.write('\\end{question}\n')
                formula = not formula
                quest += 1
                continue
            if formula:
                if '\\begin{equation*}' in line or '\\begin{equation}' in line or '\\end{equation*}' in line or '\\end{equation}' in line or '$$' in line:
                    eqrev = eq
                    eq = not eq
                    continue
                if eq:
                    towrite = line
                    towrite = towrite.replace('\centering','')
                    g.write('\\begin{reponses}\n')
                    g.write('\mauvaise{$' + towrite + '$}')
                    g.write('\\bonne{$' + towrite + '$}')
                    g.write('\end{reponses}\n')
                    continue
                # if '$' in line:
                #     towrite = line
                #     towrite = towrite.replace('\centering','')
                #     g.write('\\begin{reponses}\n')
                #     g.write('\mauvaise{' + towrite + '}')
                #     g.write('\\bonne{' + towrite + '}')
                #     g.write('\end{reponses}\n')
                #     continue
                else:
                    g.write(line + '\n')
                    continue
                    # g.write('\\ansbox[$\displaystyle' + line[:i+1] + '$\qquad]\n')
                # else:
                    # if not eqprev:
                    #     # g.write('\\item ' + line)
                    #     g.write('\\begin{question}{' + str(quest) + '}')
                    #     g.write(line + '\n')
                    #     g.write('\\begin{reponses}\n')
                    #     g.write('\mauvaise{Faux}\n')
                    #     g.write('\\bonne{Vrai}\n')
                    #     g.write('\end{reponses}\n')
                    #     g.write('\end{question}\n')
                    # else:
                    #     eqprev = False
            if '\\begin{definition}' in line or '\\end{definition}' in line:
                defini = not defini
                quest += 1
                continue
            # if '\\begin{prop}[' in line or (prop and'\\end{prop}' in line):
            #     i = line.index('[')
            #     j = line.index(']')
            #     g.write('\\begin{question}{' + str(quest) + '}')
            #     g.write(line[i+1:j] + '\n')
            #     g.write('\\begin{reponses}\n')
            #     g.write('\mauvaise{Faux}\n')
            #     g.write('\\bonne{Vrai}\n')
            #     g.write('\end{reponses}\n')
            #     g.write('\end{question}\n')
            #     # g.write('\\item ' + line[i+1:j] + '\\ansbox\n')
            #     quest += 2
            # # if prop:
            # #     if '\\begin{equation*}' in line or '\\end{equation*}' in line or '$$' in line:
            # #         eq = not eq
            # #         continue
            # #     if not eq:
            # #         g.write('\\item ' + line + '\\ansbox\n')
            # if defini:
            #     if '\\begin{equation*}' in line or '\\end{equation*}' in line or '$$' in line:
            #         eqrev = eq
            #         eq = not eq
            #         continue
            #     if eq:
            #         i = line.index('=')
            #         g.write('\\begin{question}{' + str(quest) + '}')
            #         g.write(line[:i+1] + '\n')
            #         g.write('\\begin{reponses}\n')
            #         g.write('\mauvaise{Faux}\n')
            #         g.write('\\bonne{Vrai}\n')
            #         g.write('\end{reponses}\n')
            #         g.write('\end{question}\n')
            #         # g.write('\\ansbox[$\displaystyle' + line[:i+1] + '$\qquad]\n')
            #     else:
            #         if not eqprev:
            #             g.write('\\begin{question}{' + str(quest) + '}')
            #             g.write(line + '\n')
            #             g.write('\\begin{reponses}\n')
            #             g.write('\mauvaise{Faux}\n')
            #             g.write('\\bonne{Vrai}\n')
            #             g.write('\end{reponses}\n')
            #             g.write('\end{question}\n')
            #             # g.write('\\item ' + line)
            #         else:
            #             eqprev = False
            if quest == 10:
                break
        # g.write('\\AMCaddpagesto{1}\n\\end{document}')
    g.close()
f.close()
