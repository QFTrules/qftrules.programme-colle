import sys
import time 
import re

filename = sys.argv[1]
date = sys.argv[2]

def count_braces(text):
    """Count unmatched opening braces in text"""
    count = 0
    i = 0
    while i < len(text):
        if i > 0 and text[i-1] == '\\':
            i += 1
            continue
        if text[i] == '{':
            count += 1
        elif text[i] == '}':
            count -= 1
        i += 1
    return count

with open(filename, 'r') as f:
    with open(filename[:-4]+'_soluce_only.tex','w') as g:
        entete = False
        in_todo = False
        in_sol = False
        in_enonce = False
        in_qr_question = False
        in_qr_answer = False
        in_quest = False
        todo_depth = 0
        sol_depth = 0
        enonce_depth = 0
        qr_depth = 0
        
        for line in f:
            # Handle Entete block
            if '\\Entete' in line or entete:
                g.write(line)
                entete = True
                if '\\end{entete}' in line or '% \\end \\entete' in line:
                    entete = False
                continue
            
            # Skip LaTeX root comment
            if '% !TEX root' in line:
                continue
            
            # Handle input commands
            if '\\input{' in line:
                if 'devoir.sty' in line:
                    g.write('\\input{devoir_soluce.sty}\n')
                else:
                    g.write(line)
                g.write('\\Soluce\n')
                g.write('\\SoluceOnly\n')
                if '\\input{TP.sty}' in line:
                    g.write("\\renewcommand{\\todo}[1]{\\stepcounter{protocolei}\\item[\\icontodo\\theprotocolei]}\n")
                continue
            
            # Handle begin document
            if '\\begin{document}' in line:
                g.write(line)
                g.write('{\\textcolor{gray}Version corrigée du ' + str(date) + '}\n')
                g.write('%--- added by build-soluce_only.py on ' + date + ' ---\n')
                g.write('%----------------------------------------------\n')
                continue
            
            # Skip ProgrammeColle
            if '\\ProgrammeColle' in line:
                continue
            
            # Handle Exocolle
            if '\\begin{Exocolle}' in line:
                i = line.index('[')
                j = line.index(']')
                g.write(line[:j+1] + '[nofig]' + line[j+1:])
                continue
            
            # Skip Enonce blocks entirely
            if '\\Enonce{' in line:
                in_enonce = True
                enonce_depth = 1 + count_braces(line.split('\\Enonce{')[1] if '\\Enonce{' in line else '')
                continue
            elif in_enonce:
                enonce_depth += count_braces(line)
                if enonce_depth <= 0:
                    in_enonce = False
                continue
            
            if in_enonce:
                continue
            
            # Track quest blocks
            if '\\begin{quest}' in line:
                in_quest = True
                g.write(line)
                continue
            elif '\\end{quest}' in line:
                in_quest = False
                g.write(line)
                continue
            
            # Handle multi-line QR answer
            if in_qr_answer:
                qr_depth += count_braces(line)
                if qr_depth <= 0:
                    # End of answer
                    content = line.rstrip()
                    if content.endswith('}'):
                        content = content[:-1]
                    if content.strip():
                        g.write(content + '\n')
                    in_qr_answer = False
                else:
                    g.write(line)
                continue
            
            # Handle question part of QR
            if in_qr_question:
                # Check if answer starts with { on this line
                if '{' in line and not '\\' in line[:line.index('{')]:
                    # Found answer opening {
                    in_qr_question = False
                    in_qr_answer = True
                    idx = line.index('{')
                    answer_content = line[idx+1:]
                    qr_depth = 1 + count_braces(answer_content)
                    
                    if qr_depth <= 0:
                        # Empty or single-line answer
                        content = answer_content.rstrip()
                        if content.endswith('}'):
                            content = content[:-1]
                        if content.strip():
                            g.write('\\item ' + content.rstrip() + '\n')
                        in_qr_answer = False
                    else:
                        # Multi-line answer
                        g.write('\\item ' + answer_content)
                    continue
                
                # Still in question, count braces
                qr_depth += count_braces(line)
                if qr_depth <= 0:
                    # Question ended without finding answer opening {
                    in_qr_question = False
                    # This shouldn't happen in well-formed input
                continue
            
            # Detect QR start
            if '\\QR' in line and '{' in line:
                in_qr_question = True
                match = re.search(r'\\QR\s*\{', line)
                if match:
                    after_qr = line[match.end():]
                    qr_depth = 1 + count_braces(after_qr)
                    
                    # Check if question closes and answer starts on same line
                    if '}' in after_qr:
                        idx_close = after_qr.rfind('}')
                        after_close = after_qr[idx_close+1:]
                        if '{' in after_close:
                            # Answer starts on same line
                            idx_open = after_close.index('{')
                            answer_content = after_close[idx_open+1:]
                            in_qr_question = False
                            in_qr_answer = True
                            qr_depth = 1 + count_braces(answer_content)
                            
                            if qr_depth <= 0:
                                # Single-line answer
                                content = answer_content.rstrip()
                                if content.endswith('}'):
                                    content = content[:-1]
                                if content.strip():
                                    g.write('\\item ' + content.rstrip() + '\n')
                                in_qr_answer = False
                            else:
                                # Multi-line answer
                                g.write('\\item ' + answer_content)
                            continue
                        else:
                            # Answer on next line
                            in_qr_question = False
                            continue
                continue
            
            # Handle todo blocks
            if '\\todo' in line and '{' in line and not in_sol:
                in_todo = True
                todo_depth = 1 + count_braces(line.split('\\todo{')[1] if '\\todo{' in line else '')
                continue
            elif in_todo:
                todo_depth += count_braces(line)
                if todo_depth <= 0:
                    in_todo = False
                continue
            
            # Handle sol blocks
            if '\\sol{' in line:
                in_sol = True
                sol_depth = 0
                match = re.search(r'\\sol\{', line)
                if match:
                    prefix = line[:match.start()]
                    rest = line[match.end():]
                    sol_depth = 1 + count_braces(rest)
                    
                    if in_quest and prefix.strip() == '':
                        prefix = '\\item '
                    
                    if sol_depth <= 0:
                        content = rest.rstrip()
                        if content.endswith('}'):
                            content = content[:-1]
                        g.write(prefix + content.rstrip() + '\n')
                        in_sol = False
                    else:
                        g.write(prefix + rest)
                continue
            elif in_sol:
                sol_depth += count_braces(line)
                if sol_depth <= 0:
                    content = line.rstrip()
                    if content.endswith('}'):
                        content = content[:-1]
                    if content.strip():
                        g.write(content + '\n')
                    in_sol = False
                else:
                    g.write(line)
                continue
            
            # End of document
            if '\\end{document}' in line:
                g.write(line)
                continue
            
            # Write other content
            g.write(line)

g.close()
f.close()
