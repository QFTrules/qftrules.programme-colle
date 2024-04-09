# coding=utf-8
import sys
with open(sys.argv[1], 'r') as f:
    with open('Interro.tex','a') as g:
        prop    = False
        eq      = False
        eqprev  = False
        defini  = False
        formula = False
        quest   = 0
        for line in f:
            if line[0] == '%':
                continue
            if '\\begin{theorem}' in line or '\\end{theorem}' in line:
                if '[' in line:
                    i = line.index('[')
                    j = line.index(']')
                    g.write('\\item ' + line[i+1:j] + '\\ansbox\n')
                    quest += 2
                else:
                    formula = not formula
                    quest += 1
                    continue
            if formula:
                if '\\begin{equation*}' in line or '\\end{equation*}' in line or '$$' in line:
                    eqrev = eq
                    eq = not eq
                    continue
                if eq:
                    i = line.index('=')
                    g.write('\\ansbox[$\displaystyle' + line[:i+1] + '$\qquad]\n')
                else:
                    if not eqprev:
                        g.write('\\item ' + line)
                    else:
                        eqprev = False
            if '\\begin{definition}' in line or '\\end{definition}' in line:
                defini = not defini
                quest += 1
                continue
            if '\\begin{prop}[' in line or (prop and'\\end{prop}' in line):
                i = line.index('[')
                j = line.index(']')
                g.write('\\item ' + line[i+1:j] + '\\ansbox\n')
                quest += 2
            # if prop:
            #     if '\\begin{equation*}' in line or '\\end{equation*}' in line or '$$' in line:
            #         eq = not eq
            #         continue
            #     if not eq:
            #         g.write('\\item ' + line + '\\ansbox\n')
            if defini:
                if '\\begin{equation*}' in line or '\\end{equation*}' in line or '$$' in line:
                    eqrev = eq
                    eq = not eq
                    continue
                if eq:
                    i = line.index('=')
                    g.write('\\ansbox[$\displaystyle' + line[:i+1] + '$\qquad]\n')
                else:
                    if not eqprev:
                        g.write('\\item ' + line)
                    else:
                        eqprev = False
            if quest == 10:
                break
    g.close()
f.close()
