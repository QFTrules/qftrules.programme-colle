"""
This script converts a PDF document into a markdown file using the markitdown library.
It takes the path to the PDF document as a command-line argument and outputs a markdown file
with the same name but with a .md extension.
"""

import sys
from markitdown import MarkItDown

# input pdf document
programme_colle = sys.argv[1]
input_path = sys.argv[2]

# markdown_content of the pdf document
markdown_content = MarkItDown().convert(programme_colle).text_content



"""
Read markdown file to extract the « questions de cours » 
"""

def extract_questions_from_markdown(md_content_true: str):
    """
    Input : md_content (str) : content of the markdown file
        Output : list of questions (list of str)
    """
    # identify lines in large string
    md_content = md_content_true
    questions = dict()
    # questions = []
    
    while len(md_content) > 0:
        
        # get cours section
        try:
            cours_start_index = md_content.index("Cours")
            cours_end_index = md_content.index("Exercices")
        except ValueError:
            try:
                cours_start_index = md_content.index("Cours")
                cours_end_index = md_content.index("Colleurs")
            except ValueError:
                break
        
        # GET THEME
        # print(md_content)
        md_search_theme = md_content[cours_start_index:cours_start_index-min(50, cours_start_index):-1]
        # print("COURSS INDEX:", cours_start_index)
        # print("***************")
        # print(md_search_theme)
        # print("***************")
        start_theme = md_search_theme.find("\n")
        end_theme = md_search_theme.find("\n", start_theme+2)
        theme = md_content[cours_start_index - end_theme -1 : cours_start_index - start_theme -1].strip()
        # print("THEME:", theme)
        # initialize list of questions with theme
        # questions.append(theme)
        questions[theme] = []
        
        # isolate cours section
        md_section = md_content[cours_start_index:cours_end_index]
        # print(md_section)
        # print("----------------")
        # loop over bullets
        while len(md_section) > 0:
            try:
                md_section = md_section[md_section.index("•")+1:]
            except ValueError:
                break
            question = md_section[0:md_section.find("•")].strip()
            # remove new lines in question
            question = question.replace("\n", " ")
            # append question to list
            questions[theme].append(question)
            
        # update md_content by removing the cours section
        md_content = md_content[cours_end_index+1:]
        # print("Remaining md_content length:", len(md_content))
    # output list of questions 
    return questions

questions = extract_questions_from_markdown(markdown_content)

# replace lone accents by accented letters in questions
accented_replacements = {"´a": "á", "´e": "é", "´i": "í", "´o": "ó", "´u": "ú",
                         "`a": "à", "`e": "è", "`i": "ì", "`o": "ò", "`u": "ù",
                         '¨a': "ä", "¨e": "ë", "¨ı": "ï", "¨o": "ö", "¨u": "ü", 
                         "~n": "ñ", "ˆa": "â", "ˆe": "ê", "ˆi": "î", "ˆo": "ô", "ˆu": "û"}

questions_copy = dict() 

for theme in questions:
    question_list = questions[theme]
    # correct theme accents
    theme_corrected = theme
    for key in accented_replacements:
        theme_corrected = theme_corrected.replace(key, accented_replacements[key])
    questions_copy[theme_corrected] = []
    # correct question accents
    for i in range(len(question_list)):
        for key in accented_replacements:
            question_list[i] = question_list[i].replace(key, accented_replacements[key])
        questions_copy[theme_corrected].append(question_list[i])


"""
Add questions to the template of colle PCSI
"""

# # string with the latex template
# template_colle = "\\input{colle.sty}\n\\Classe[PCSI]\n\\begin{document}\n\\Count{2}{\n%%%% EXERCICE 1 %%%\n\\Source{electrocin.tex}\n\\begin{Exocolle}[\\THEME]{}\n\\item\\QUESTION1\n\\item\\QUESTION2\n\\end{Exocolle}\n\n%%%% EXERCICE 2 %%%\n\\begin{Exocolle}[\\THEME]{}\n\\item\\QUESTION1\n\\item\\QUESTION2\n\\end{Exocolle}\n\n%%%% EXERCICE 3 %%%\n\\begin{Exocolle}[\\THEME]{}\n\\item\\QUESTION1\n\\item\\QUESTION2\n\\end{Exocolle}\n}\n\\end{document}"

# fetch week number en programme_colle string
# print("programme_colle:", programme_colle)
# if "programme-" in programme_colle:
    # Scolle_start_index = programme_colle.index("-")
    # Scolle_start_index = len("programme-")
    # Scolle_end_index = programme_colle.index("-S", Scolle_start_index)
    # Scolle_number = programme_colle[Scolle_start_index:Scolle_end_index]
    # write the tex file
    # folder_absolute_path = "/".join(programme_colle.split("/")[:-1]) + "/"
    # input_path = folder_absolute_path + "Colle" + Scolle_number + "_pcsi.tex"
# else:
    # return error message to user
    # raise ValueError("Error: programme_colle does not contain 'programme-'. String received: " + programme_colle)
    # print("Error: programme_colle does not contain 'programme-'.")
    # sys.exit(1)
# output_path = folder_absolute_path + "Colle_" + Scolle_number + "_pcsi.tex"

# print(questions_copy)

# read content of colle_pcsi.tex file
with open(input_path, "r") as f:
    text = f.readlines() 
f.close()
with open(input_path, "w") as g:
    theme_counter = 0 
    question_counter = 0
    found = False
    Exocolle = False
    for line in text:
        
        # cases to handle 
        if '\\begin{document}' in line:
            found = True
            g.write("\\input{colle.sty}\n\\Classe[PCSI]\n\\begin{document}\n\\Count{1}{\n")
            continue
        if "\\Count{" in line or line[0] == "}":
            # print("skip count")
            continue
        if '\\end{document}' in line:
            # print("end document")
            g.write("}\n\\end{document}\n")
            break
        # if ("EXERCICE" in line or "\\begin{Exocolle}" in line or line[0] == "}") and Exocolle:
            # Exocolle = False
            # g.write("\\end{Exocolle}\n")
            # continue
        if "\\end{Exocolle}" in line:
            continue
            # Exocolle = False
        if '\\begin{Exocolle}[' in line:
            # Exocolle = True
            # remove trailing indent
            # replace everting between [ and ] by [\\THEME]
            start_index = line.index('[')
            end_index = line.index(']', start_index+1)
            try:
                theme = list(questions_copy.keys())[theme_counter]
                question_counter = 0
            except IndexError:
                theme = list(questions_copy.keys())[-1]
                question_counter = 2
            theme_counter += 1
            line = line[:start_index+1] + theme + line[end_index:]
            
            # write the exocolle environment line with updated theme
            g.write(line)
            
            # generate two questions that start with \item
            Nquest = len(questions_copy[theme])
            for i in range(2):
                try:
                    question = questions_copy[theme][question_counter]
                except IndexError:
                    question = questions_copy[theme][2*Nquest-2-question_counter]
                question_counter += 1
                g.write("\t\\item " + question + "\n")
            g.write("\\end{Exocolle}\n")
                
            # skip to next line
            continue
        
        if '\\item' in line:
            continue
        #     # replace everything after \item by \QUESTIONX
        #     start_index = line.index('\\item') + len('\\item')
        #     try:
        #         question = questions_copy[theme][question_counter]
        #     except IndexError:
        #         question = questions_copy[theme][-1]
        #     question_counter += 1
        #     line = line[:start_index] +  " " + question + "\n"
        if not found:
            continue
        
        # if '\\end{Exocolle}' in line:
            # remove trailing indent
            # line = line.lstrip()
        # default case: write line as is
        g.write(line)
g.close()



# # replace themes and questions in the template
# for i in range(3):
#     # retrieve theme
#     try:
#         theme = list(questions_copy.keys())[i]
#     except IndexError:
#         theme = list(questions_copy.keys())[-1]
#     template_colle = template_colle.replace("\\THEME", theme, 1)
    
#     # retrieve questions
#     for i in range(2):
#         try:
#             question = questions_copy[theme][i]
#         except IndexError:
#             question = questions_copy[theme][-1]
#         template_colle = template_colle.replace(f"\\QUESTION{i+1}", " " + question, 1)
        


# # write the tex file
# folder_absolute_path = "/".join(programme_colle.split("/")[:-1]) + "/"
# latex_file_path = folder_absolute_path + "_colle_" + Scolle_number + "_pcsi.tex"
# with open(output_path, "w") as f:
    # f.write(template_colle)
# print(f"LaTeX file {output_path} has been created.")
f.close()

    