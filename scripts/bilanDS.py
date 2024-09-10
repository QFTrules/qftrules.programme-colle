"""
Import section
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

"""
Get table of marks
"""
file = sys.argv[1]
tmp_folder = sys.argv[2]
sty_file = sys.argv[3]
# get basename of file
basename = file.split('/')[-1]
# get first three characters of file basename
DSnumber = (basename.split('.')[0])[:3]
# import csv file as dataframe in python usign utf8 encoding for names
df = pd.read_excel(file)

"""
Extract information from table
"""
#  create a dictionary for correspondence between name and line number 
ID = {}
for i in range(len(df)):
    nom = df['NOMS'][i]
    if not 'Moyenne' in str(nom) and not 'nan' in str(nom):
        ID[df['NOMS'][i]] = i

# number of students
numstudent = len(ID)

# create a dictionary for correspondence between question and coefficient
coeff = {}
i=1
while True:
    try:
        quest = df['Q%i'%i]
        # print(quest)
        coeff['Q%i'%i] = float(quest[0])
        i+=1
    except(KeyError):
        break
    
# define sum of coefficients
sumcoeff = sum(list(coeff.values()))
sumquest = len(coeff)

def efficacite(eleve):
    # rapport du nombre de points gagnés sur le nombre de points abordés
    eff = 0
    sumaborde = 0
    for q in coeff:
        qvalue = df[q][ID[eleve]]
        if not 'nan' in str(qvalue):
            sumaborde += coeff[q]
            eff += qvalue/coeff[q]
    return eff/sumaborde

def productivite(eleve):
    prod = 0
    for q in coeff:
        qvalue = df[q][ID[eleve]]
        if not 'nan' in str(qvalue):
            prod += 1
    return prod/sumquest

def notebrute(eleve):
    note = 0
    for q in coeff:
        qvalue = df[q][ID[eleve]]
        if not 'nan' in str(qvalue):
            note += qvalue
    return round(note, 1)

def notefinale(eleve):
    note_eleve = df['Note'][ID[eleve]]
    # if note_eleve < 20:
    return note_eleve
    # else:
        # return 19.4

# produce a list of notes
notes = []
for eleve in ID:
    notes.append(notefinale(eleve))
    
#  moyenne et écart-type
moyenne = np.round(np.mean(notes),1)
stdnotes = np.round(np.std(notes),1)
    
"""
Generate histogram and latex
"""
# get the number of students in bin range where notefinale(eleve) is
def bineleve(note_eleve):
    binlisteleve = []
    i = round(note_eleve)
    j = round(note_eleve) + 1
    for note in notes:
        if i <= note < j:
            binlisteleve.append(note_eleve)
    return binlisteleve

# function to plot histogram
def figsize(scale):                                 # Define default ratio
    fig_width_pt =  341.43307                       # Get this from LaTeX using \the\textwidth
    inches_per_pt = 1.0/72.27                       # Convert pt to inch
    golden_mean = (np.sqrt(5.0)-1.0)/2.0             # The golden number is an aesthetic ratio
    fig_width = fig_width_pt*inches_per_pt*scale    # width in inches
    fig_height = fig_width*golden_mean              # height in inches
    fig_size = [fig_width,fig_height]
    return fig_size

# def histnote(eleve,binres):
#     # use latex rendering
#     plt.rc('text', usetex=True)
#     # use serif font
#     plt.rc('font', family='serif')
#     # set font size to 11
#     plt.rc('font', size=11)
#     # set figure size to 
#     plt.figure(figsize = figsize(0.75), dpi = 200)
#     binrange = np.arange(0,21,binres)
#     plt.hist(notes, bins=binrange, edgecolor='black', color='lightgray')
#     # highlight the bin where the student mark is in darkgray
#     plt.hist(bineleve(eleve), bins=binrange, edgecolor='black', color='black')
#     # plt.xlabel(r'Notes')
#     plt.xlabel(r'Notes finales')
#     # plt.ylabel(r"Nombre d'étudiants")
#     plt.ylabel(r"Effectifs")
#     plt.xticks(np.arange(0,21,2), labels=[r'$0$',r'$2$',r'$4$',r'$6$',r'$8$',r'$10$',r'$12$',r'$14$',r'$16$',r'$18$',r'$20$'])
#     plt.yticks(np.arange(0,1.2*numstudent/np.sqrt(2*np.pi*stdnotes),1))
#     # plt.title(r'Histogramme des notes')
#     plt.savefig(tmp_folder + DSnumber + '_' + str(eleve) + '_histo.pdf', dpi=300, bbox_inches='tight')
#     plt.close()

def histnote(eleve,binres=1):
    # use latex rendering
    plt.rc('text', usetex=True)
    # use serif font
    plt.rc('font', family='serif')
    # set font size to 11
    plt.rc('font', size=11)
    # set figure size to 
    plt.figure(figsize = figsize(0.75), dpi = 200)
    binrange = np.arange(0,21,binres)
    plt.hist(notes, bins=binrange, edgecolor='black', color='lightgray')
    # highlight the bin where the student mark is in darkgray
    plt.hist(bineleve(notefinale(eleve)), bins=binrange, edgecolor='black', color='black')
    # plt.xlabel(r'Notes')
    plt.xlabel(r'Notes finales')
    # plt.ylabel(r"Nombre d'étudiants")
    plt.ylabel(r"Effectifs")
    plt.xticks(np.arange(0,21,2), labels=[r'$0$',r'$2$',r'$4$',r'$6$',r'$8$',r'$10$',r'$12$',r'$14$',r'$16$',r'$18$',r'$20$'])
    plt.yticks(np.arange(0,1.2*numstudent/np.sqrt(2*np.pi*stdnotes),1))
    # plt.title(r'Histogramme des notes')
    plt.savefig(tmp_folder + '/' + DSnumber + '_' + str(eleve) + '_histo.pdf', dpi=300, bbox_inches='tight')
    plt.close()
    
# write the latex file for the bilan for eleve
# def bilan_latex(eleve):
#     with open(tmp_folder + DSnumber + '_' + str(eleve) + '_bilan.tex','w') as f:
#         f.write('\\input{' + sty_file + '}\n')
#         f.write('\\begin{document}\n')
#         f.write('\\EnteteBilan{' + str(eleve) + '}{' + str(notebrute(eleve)) + '/' + str(sumcoeff) + '}{' + str(notefinale(eleve)) + '/' + str(20) + '}{' + str(int(round(efficacite(eleve)*100,0))) + '\\%}{' + str(int(round(productivite(eleve)*100,0))) + '\\%}{' + DSnumber + '_' + str(eleve) + '_histo.pdf}\n')
        
#         # end of document
#         f.write('\\end{document}')
#         f.close()

# write the latex file for all students
tex_bilan = tmp_folder + '/' + DSnumber + '_bilan.tex'
def init_latex_all():
    with open(tex_bilan,'w') as f:
        f.write('\\input{' + sty_file + '}\n')
        f.write('\\begin{document}\n')

def end_latex_all():
    with open(tex_bilan,'a') as f:
        f.write('\\end{document}')
        f.close()       

def bilan_latex_all(eleve):
    with open(tex_bilan,'a') as f:
        f.write('\\EnteteBilan{' + str(eleve) + '}{' + str(notebrute(eleve)).replace('.',',') + '/' + str(int(sumcoeff)) + '}{' + str(notefinale(eleve)).replace('.',',') + '/' + str(20) + '}{' + str(int(round(efficacite(eleve)*100,0))) + '\\%}{' + str(int(round(productivite(eleve)*100,0))) + '\\%}{' + DSnumber + '_' + str(eleve) + '_histo.pdf}' + '{' + str(moyenne).replace('.',',') + '/' + str(20) + '}{' + str(stdnotes).replace('.',',') + '/' + str(20) + '}\n')
        f.write('\\newpage\n')
        
# generate the histogram and bilan for each student
init_latex_all()
for eleve in ID:
    try:
        histnote(eleve)
        bilan_latex_all(eleve)
    except:
        pass
end_latex_all()