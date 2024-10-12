#!/bin/bash

# colors
# RED="\033[1;31m"
# END='\e[0m'

collepath=$1
stypath=$2
pythoncommand=$3
pythonpath=$4

# change directory
# cd ~/Dropbox/.latex/Commands/
cd ./tmp/
ProgColle="ProgrammeColle.tex"
# create list of files to parse
find ~/Dropbox/CPGE/Physique/Cours/ \( -name "*.tex" ! -name "*TD*" ! -name "*Fig*" ! -name "*Doc*" \) | sort > list_cours.txt
# find ~/Dropbox/PCAME/Cours/ \( -name "*.tex" ! -name "*TD*" ! -name "*Fig*" ! -name "*Doc*" \) | sort > list_cours.txt
# echo "List of Cours files printed in list_cours.txt"
find ~/Dropbox/CPGE/Physique/TD/ -name "*TD*.tex" | sort > list_TD.txt
# echo "List of TD files printed in list_TD.txt"
find ~/Dropbox/CPGE/Physique/Devoirs/DM -name "*.tex" | sort > list_DM.txt
# echo "List of DM files printed in list_DM.txt"
find ~/Dropbox/CPGE/Physique/Devoirs/DS/ -name "*.tex" | sort > list_DS.txt
# echo "List of DS files printed in list_DS.txt"
find ~/Dropbox/CPGE/Physique/TP/ -name "*.tex" | sort > list_TP.txt
# echo "List of TP files printed in list_TP.txt"

# create tex file with programme de colle
# echo "\input{${stypath}progcolle.sty}%$
#       \input{${stypath}programme.tex}%$
#       \begin{document}
#       \tableofcontents
#       " > $ProgColle
echo "\input{/home/eb/Dropbox/texmf/tex/latex/Preambles/progcolle.sty}%$
      \input{/home/eb/Dropbox/texmf/tex/latex/Preambles/programme.tex}%$
      \begin{document}
      \tableofcontents
      " > $ProgColle

# echo "Warning : "
# fetch program in all lecture files
for fichier in $(cat list_cours.txt)
do
  if grep -q "\ProgrammeColle" $fichier
  then
    # simple_fichier=$(basename "$fichier")
    # echo -e "${RED}Cours${END} $simple_fichier added to programme de colle"
    python $pythonpath/build_programme_colle_java.py $fichier $ProgColle
  else
      continue
  fi
done

# fetch program in all TD files
echo "\TD" >> $ProgColle
for fichier in $(cat list_TD.txt)
do
  if grep -q "\ProgrammeColle" $fichier
  then
    # simple_fichier=$(basename "$fichier")
    # echo -e "${RED}TD${END} $simple_fichier added to programme de colle"
    python $pythonpath/build_programme_colle_java.py $fichier $ProgColle
  else
      continue
  fi
done

# fetch program in all DM files
echo "\DM" >> $ProgColle
for fichier in $(cat list_DM.txt)
do
  if grep -q "\ProgrammeColle" $fichier
  then
    # simple_fichier=$(basename "$fichier")
    # echo -e "${RED}DM${END} $simple_fichier added to programme de colle"
    python $pythonpath/build_programme_colle_java.py $fichier $ProgColle
  else
      continue
  fi
done

# fetch program in all DS files
echo "\DS" >> $ProgColle
for fichier in $(cat list_DS.txt)
do
  if grep -q "\ProgrammeColle" $fichier
  then
    # simple_fichier=$(basename "$fichier")
    # echo -e "${RED}DS${END} $simple_fichier added to programme de colle"
    python $pythonpath/build_programme_colle_java.py $fichier $ProgColle
  else
      continue
  fi
done

# fetch program in all TP files
echo "\TP" >> $ProgColle
for fichier in $(cat list_TP.txt)
do
  if grep -q "\ProgrammeColle" $fichier
  then
    # simple_fichier=$(basename "$fichier")
    # echo -e "${RED}TP${END} $simple_fichier added to programme de colle"
    python $pythonpath/build_programme_colle_java.py $fichier $ProgColle
  else
      continue
  fi
done


# end and compile
echo "\end{document}" >> $ProgColle

# dates of the upcoming week
DAYCHECK=$(date +%Y-%m-%d)
numdaycheck=`date -d $DAYCHECK +%u`
sumMon=$((8-$numdaycheck))
sumFri=$((13-$numdaycheck))
NextMonday=$(date -d "$DAYCHECK $sumMon days" +%d/%m/%Y)
NextFriday=$(date -d "$DAYCHECK $sumFri days" +%d/%m/%Y)
Filedate=$(date -d "$DAYCHECK $sumMon days" +%Y_%m_%d)
pdfName="_PC_Phy_colle.pdf"
txxName="_PC_Phy_colle_ini.tex"
texName="_PC_Phy_colle.tex"
tocName="_PC_Phy_colle.toc"
# echo -e "Next monday is on ${RED}$NextMonday${END}"

#head ProgrammeColle.txm
pdflatex -synctex=1 --shell-escape  -interaction=nonstopmode $ProgColle 2>&1 > /dev/null
pdflatex -synctex=1 --shell-escape  -interaction=nonstopmode $ProgColle 2>&1 > /dev/null

# print the table of contents only
echo "\input{${stypath}progcolle.sty}%$
      \input{${stypath}programme.tex}%$
      \newcommand{\babel}[6]{
      \begin{center}
      {\Large\textsc{Programme de colle de physique}}
      \end{center}
      \begin{center}
      {Semaine du lundi $NextMonday ~au vendredi $NextFriday}
      \end{center}
      }
      \begin{document}
      \input{ProgrammeColle.toc}
      \end{document}" > $Filedate$texName
# echo "Compiling the programme de colle..."
pdflatex -synctex=1 --shell-escape  -interaction=nonstopmode $Filedate$texName 2>&1 > /dev/null
pdflatex -synctex=1 --shell-escape  -interaction=nonstopmode $Filedate$texName 2>&1 > /dev/null
# echo "Compiling OK, " 
# pdflatex -synctex=1 --shell-escape  --interaction=batchmode $Filedate$texName 2>&1 > /dev/null
# pdflatex -synctex=1 --shell-escape  --interaction=batchmode $Filedate$texName 2>&1 > /dev/null

# remove auxiliary files
aux="_PC_Phy_colle.aux"
log="_PC_Phy_colle.log"
out="_PC_Phy_colle.out"
sync="_PC_Phy_colle.synctex.gz"
rm list_TD.txt
rm list_DM.txt
rm list_DS.txt
rm list_TP.txt
rm list_cours.txt
rm $Filedate$aux
rm $Filedate$log
rm $Filedate$sync
rm $Filedate$out
#rm ProgrammeColle.toc
#rm $ProgColle
#rm ProgrammeColle_print.tex
#rm ProgrammeColle_print.aux
#rm ProgrammeColle_print.log
#rm ProgrammeColle_print.synctex.gz
#cp ProgrammeColle.toc ~/Dropbox/CPGE/Physique/Exercices/Colles/PC
#cp ProgrammeColle_print.txm $collepath$Filedate$txmName
#mv ProgrammeColle_print.pdf $collepath$Filedate$pdfName
rm $collepath*_PC_Phy_colle.*
rm $collepath*_PC_Phy_colle_ini.tex
mv $ProgColle $collepath$Filedate$txxName
mv ProgrammeColle.toc $collepath
mv $Filedate$texName $collepath
mv $Filedate$pdfName $collepath
rm ${ProgColle%.*}.*
#cd ~/Dropbox/CPGE/Physique/Exercices/Colles/
# code $Filedate$pdfName

# echo $Filedate$pdfName
