#!/bin/bash

cpgePath=$1

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

emit_matches() {
  # Print one file per line with trailing comma to keep extension parser behavior.
  xargs -0 -r grep --color=never -Fl '\ProgrammeColle' 2>/dev/null | sort | while IFS= read -r file; do
    if [ -n "$file" ]; then
      printf '%s, \n' "$file"
    fi
  done
}

# fetch program in all lecture files
echo -e "    Cours : "
if [ -d "$cpgePath/Cours/" ]; then
  find "$cpgePath/Cours/" -type f -name "*.tex" ! -name "*TD*" ! -name "*Fig*" ! -name "*Doc*" -print0 | emit_matches
fi
echo -e " : "

# fetch program in all TD files
echo -e "    TD : "
if [ -d "$cpgePath/TD/" ]; then
  find "$cpgePath/TD/" -type f -name "*TD*.tex" -print0 | emit_matches
fi
echo -e " : "

# fetch program in all DM files
echo -e "    DM : "
if [ -d "$cpgePath/Devoirs/DM/" ]; then
  find "$cpgePath/Devoirs/DM/" -type f -name "*.tex" -print0 | emit_matches
fi
echo -e " : "

# fetch program in all DS files
echo -e "    DS : "
if [ -d "$cpgePath/Devoirs/DS/" ]; then
  find "$cpgePath/Devoirs/DS/" -type f -name "*.tex" -print0 | emit_matches
fi
echo -e " : "

# fetch program in all TP files
echo -e "    TP : "
if [ -d "$cpgePath/Devoirs/TP/" ]; then
  find "$cpgePath/Devoirs/TP/" -type f -name "*.tex" -print0 | emit_matches
fi