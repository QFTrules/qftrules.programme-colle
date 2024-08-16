# coding=utf-8
import sys
# from collections import deque
cours = sys.argv[1]
template = sys.argv[2]
from numpy import random

def get_left_side(line):
    try:
        i = line.index('$')
    except:
        i = -1
    try:
        k = line.index('=')
        try:
            k = line.index('$',k)
        except:
            pass
    except:
        k = len(line)
    try:
        k = line.index('\simeq') - 1
    except:
        pass
    return clear_output(line[i+1:k].strip())

def get_right_side(line):
    try:
        k = line.index('=')
    except:
        k = len(line)
    try:
        k = line.index('\simeq') - 1
    except:
        pass
    try:
        j = line.index('$',k)
    except:
        j = len(line)
    left_side = line[k+1:j].strip().replace(',','')
    return clear_output(left_side)
    
def clear_output(output):
    if '.' in output:
        output = output.replace('.','')
    if '\quad' in output:
        m = output.index('\quad')
        output = output[:m]
    if '\qquad' in output:
        m = output.index('\qquad')
        output = output[:m]
    if '&' in output:
        m = output.index('&')
        output = output[:m]
    if '\\end{array}' in output:
        m = output.index('\\end{array}')
        output = output[:m]
    # if '\SI' in output:
        # output = ''
    if '\\begin{cases}' in output:
        # i = output.index('\\begin{cases}')
        # j = output.index('&')
        output = ''
    if '\\begin{split}' in output:
        # i = output.index('\\begin{split}')
        # j = output.index('&')
        output = ''
    if output:
        if output[0] == '\simeq':
            output = output[1:]
    return output

def get_to_write(line):
    try:
        i = line.index('$')
        j = line.index('$',i+1)
        output = line[i+1:j].replace('\centering','').strip()
    except:
        output = line.replace('\centering','').strip()
    return clear_output(output)
    
def get_text(line):
    try:
        i = line.index('$')
    except:
        i = len(line)
    return line[:i] + '\n'

def get_theorem(line):
    try:
        i = line.index('[')
        j = line.index(']')
        return line[i+1:j]
    except:
        return ''

def get_random_answer(ANSWERS,line):
    right_side = get_right_side(line)
    # if '\dive' in right_side:
    #     return right_side.replace('\dive','\Delta')
    # if '\Delta' in right_side:
    #     return right_side.replace('\Delta','\dive')
    # if '\Rot' in right_side:
    #     return right_side.replace('\Rot','\Grad')
    # if '\Grad' in right_side:
    #     return right_side.replace('\Grad','\Rot')
    if ANSWERS:
        answer = random.choice(ANSWERS)
        # # answer = ANSWERS.pop().strip()
        # if answer[0] == '-':
        #     ANSWERS.append(answer)
        #     return answer.replace('-','')
        # else:
            # ANSWERS.append('-' + answer)
        return answer
    else:
        if '-' in right_side:
            return right_side.replace('-','')
        else:
            return right_side
    
def build_propositions(ANSWERS,line,answer=''):
    left_side = get_left_side(line)
    right_side = get_right_side(line)
    towrite = get_to_write(line)
    if towrite == '':
        return []
    propositions = ['\\bonne{$' + towrite + '$}\n']
    for i in range(2):
        while answer == '' or answer == left_side:
            answer = get_random_answer(ANSWERS,line)
        choix = left_side + '=' + answer
        if not choix in CHOIX and choix != towrite:
            CHOIX.append(choix)
            propositions += ['\\mauvaise{$' + choix + '$}\n']
    for i in range(2):
        while answer == '' or answer == right_side:
            answer = get_random_answer(ANSWERS,line)
        choix = answer + '=' + right_side
        if not choix in CHOIX and choix != towrite: 
            CHOIX.append(choix)
            choix = choix.replace('=\simeq','\simeq')
            propositions += ['\\mauvaise{$' + choix + '$}\n']
    random.shuffle(propositions)
    return propositions

def build_ANSWERS(cours):
    with open(cours, 'r') as f:
        ANSWERS = []
        formula = False
        for line in f:
            if '\\begin{theorem}' in line or '\\end{theorem}' in line:
                formula = not formula
                continue
            if formula and '=' in line and not '\includegraphics' in line and not '\\begin{array}' in line and not '\\end{array}' in line:
                right_side = get_right_side(line)
                if '\dive' in right_side:
                    ANSWERS.append(right_side.replace('\dive','\Delta'))
                if '\Delta' in right_side:
                    ANSWERS.append(right_side.replace('\Delta','\dive'))
                if '\Rot' in right_side:
                    ANSWERS.append(right_side.replace('\Rot','\Grad'))
                if '\Grad' in right_side:
                    ANSWERS.append(right_side.replace('\Grad','\Rot'))
                if right_side:
                    if right_side[0] == '-':
                        ANSWERS.append(right_side.replace('-',''))
                ANSWERS.append(right_side)
        return ANSWERS

ANSWERS = build_ANSWERS(cours)

with open(cours, 'r') as f:
    with open(template,'a') as g:
        prop    = False
        eq      = False
        eqinline = False
        eqprev  = False
        defini  = False
        formula = False
        quest   = 0
        CHOIX = []
        prevline = ''
        g.write('\n\n')
        for line in f:
            if line[0] == '%':
                continue
            if '\\begin{theorem}' in line:
                # or '\\begin{prop}' in line:
                g.write('\\begin{question}{' + str(int(quest)) + '}\!\!\!:~' + get_theorem(line) + '\n')
                formula = True
                quest += 0.5
                continue
            if '\\end{theorem}' in line:
                # or '\\end{prop}' in line:
                g.write('\\end{question}\n')
                formula = False
                quest += 0.5
                eq = False
                continue
            if formula:
                if '\\begin{equation*}' in line or '\\begin{equation}' in line or '\\end{equation*}' in line or '\\end{equation}' in line or '$$' in line:
                    eqprev = eq
                    eq = not eq
                    # formula = not formula
                    continue
                # elif '=' in line:
                    # eq = not eq
                    # g.write(line)
                    # g.write(get_text(line))
                    # continue
                if eq and not '\label{' in line and not '\\end{reponses}' in prevline:
                    propositions  = build_propositions(ANSWERS,line)
                    if propositions:
                        g.write('\\begin{reponses}\n')
                        for choix in propositions:
                            g.write(choix)
                        g.write('\end{reponses}\n')
                        ANSWERS.append(get_right_side(line))
                        prevline = line
                    # eq = False
                    continue
                if '=' in line:
                    propositions  = build_propositions(ANSWERS,line)
                    if propositions:
                        g.write('\\begin{reponses}\n')
                        for choix in propositions:
                            g.write(choix)
                        g.write('\end{reponses}\n')
                        ANSWERS.append(get_right_side(line))
                        prevline = line
                    # eq = False
                    continue
                # if '$' in line:
                #     towrite = line
                #     towrite = towrite.replace('\centering','')
                #     g.write('\\begin{reponses}\n')
                #     g.write('\mauvaise{' + towrite + '}')
                #     g.write('\\bonne{' + towrite + '}')
                #     g.write('\end{reponses}\n')
                #     continue
                # else:
                #     if not '\label{' in line:
                #        g.write(line + '\n')
                #     continue
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
                # quest += 1
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
            if quest == 5:
                break
        # g.write('\\AMCaddpagesto{1}\n\\end{document}')
    g.close()
f.close()
