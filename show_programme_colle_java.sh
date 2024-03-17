#!/bin/bash

# colors
RED="\033[1;31m"
GREEN="\033[1;32m"
END='\e[0m'
NEWLINE=$'\n'

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
# echo -e "Programme de colle : semaine du ${RED}$NextMonday${END} au ${RED}$NextFriday${END}"
printf "Programme de colle du $NextMonday au $NextFriday :\n"

# change directory
cd ~/Dropbox/.latex/Commands/
ProgColle="ProgrammeColle.tex"
# create list of files to parse
find ~/Dropbox/CPGE/Physique/Cours/ \( -name "*.tex" ! -name "*TD*" ! -name "*Fig*" ! -name "*Doc*" \) | sort > list_cours.txt
# echo "List of Cours files printed in list_cours.txt"
find ~/Dropbox/CPGE/Physique/TD/ -name "*TD*.tex" | sort > list_TD.txt
# echo "List of TD files printed in list_TD.txt"
find ~/Dropbox/CPGE/Physique/Devoirs/DM -name "*.tex" | sort > list_DM.txt
# echo "List of DM files printed in list_DM.txt"
find ~/Dropbox/CPGE/Physique/Devoirs/DS/ -name "*.tex" | sort > list_DS.txt
# echo "List of DS files printed in list_DS.txt"
find ~/Dropbox/CPGE/Physique/TP/ -name "*.tex" | sort > list_TP.txt
# echo "List of TP files printed in list_TP.txt"

# fetch program in all lecture files
# echo -e "    ${RED}Cours${END} :"
echo -e "    Cours : "
for fichier in $(cat list_cours.txt)
do
  if grep -q "\ProgrammeColle" $fichier
  then
    # simple_fichier="${fichier//+(*\/|.*)}"
    simple_fichier=$(basename "$fichier" .tex)
    # echo -e "    ${RED}Cours${END} : $simple_fichier"
    echo -e "$fichier, "
    # echo -e "$simple_fichier, "
    # code $fichier
  else
      continue
  fi
done

echo -e " : "

# fetch program in all TD files
# echo -e "    ${RED}TD${END} :"
echo "\TD" >> $ProgColle
echo -e "    TD : "
if [ -s list_TD.txt ]; then
  for fichier in $(cat list_TD.txt)
  do
    if grep -q "\ProgrammeColle" $fichier
    then
      simple_fichier=$(basename "$fichier" .tex)
      # echo -e "       ${GREEN}TD${END} : $simple_fichier"
      echo -e "$fichier, "
      # echo -e "       TD : $simple_fichier\n"
      # code $fichier
    else
        continue
    fi
  done
else
:
fi

echo -e " : "

# fetch program in all DM files
# echo -e "    ${RED}DM${END} :"
echo "\DM" >> $ProgColle
echo -e "    DM : "
if [ -s list_DM.txt ]; then
  for fichier in $(cat list_DM.txt)
  do
    if grep -q "\ProgrammeColle" $fichier
    then
      simple_fichier=$(basename "$fichier" .tex)
      echo -e "$fichier, "
      # echo -e "       ${GREEN}DM${END} : $simple_fichier"
      # code $fichier
    else
        continue
    fi
  done
else
:
fi

echo -e " : "

# fetch program in all DS files
# echo -e "    ${RED}DS${END} :"
echo "\DS" >> $ProgColle
echo -e "    DS : "
if [ -s list_DS.txt ]; then
  for fichier in $(cat list_DS.txt)
  do
    if grep -q "\ProgrammeColle" $fichier
    then
      simple_fichier=$(basename "$fichier" .tex)
      echo -e "$fichier, "
      # echo -e "       ${GREEN}DS${END} : $simple_fichier"
      # code $fichier
    else
        continue
    fi
  done
else
:
fi

echo -e " : "

# fetch program in all TP files
# echo -e "    ${RED}TP${END} :"
echo "\TP" >> $ProgColle
echo -e "    TP : "
if [ -s list_TP.txt ]; then
  for fichier in $(cat list_TP.txt)
  do
    if grep -q "\ProgrammeColle" $fichier
    then
      simple_fichier=$(basename "$fichier" .tex)
      # echo -e "       ${GREEN}TP${END} : $simple_fichier"
      echo -e "$fichier, "
      # code $fichier
    else
        continue
    fi
  done
else
:
fi