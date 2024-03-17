#!/bin/bash
find ~/Dropbox/CPGE/Physique/Exercices/Recueil/Thermo -name "*.tex" | sort > list_thermo.txt
# fetch program in all lecture files
# echo -e "    ${RED}Cours${END} :"
echo -e "    Cours : "
for fichier in $(cat list_exos.txt)
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
