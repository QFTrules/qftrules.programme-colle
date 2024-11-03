#!/bin/bash

# colors
RED="\033[1;31m"
END='\e[0m'

fichier=$1
folder=$(dirname $fichier)
name=$(basename $fichier)
# DAYCHECK=$(date +%Y-%m-%d)
DAY=$(date +%a)
# echo $DAY
# numdaycheck=`date -d $DAYCHECK +%u`
# sumTue=$((2-$numdaycheck))
# sumsumTue=$(($sumTue + 7))
if [[ $DAY == "Tue" ]]
then
  # NextTuesday=$(date +%d/%m/%Y)
  # NextnextTuesday=$(date -d "$DAYCHECK $sumTue days" +%d/%m/%Y)
  NextTuesday=$(date +%d/%m/%Y)
  NextnextTuesday=$(date -d "next tuesday" +%d/%m/%Y)
else
  NextTuesday=$(date -d "next tuesday" +%d/%m/%Y)
  NextnextTuesday=$(date -d "1 week next tuesday" +%d/%m/%Y)
  # NextTuesday=$(date -d "$DAYCHECK $sumTue days" +%d/%m/%Y)
  # NextnextTuesday=$(date -d "$DAYCHECK $sumsumTue days" +%d/%m/%Y)
fi

echo -e "Next colle is on Tuesday ${RED}$NextTuesday${END}"
# echo $NextnextTuesday
echo -e "Building Fiche_tmp.tex for ${RED}$name${END}"
cd $folder
python3 build-fiche-colle.py $fichier $NextTuesday $NextnextTuesday $HOME
#rm $fichier
echo "Compiling..."
for i in Fiche_tmp*.tex; do pdflatex -shell-escape -interaction=nonstopmode $i $2> /dev/null; done
# pdflatex -shell-escape -interaction=nonstopmode Fiche_tmp*.tex $2> /dev/null
pdf=".pdf"
fiche="Fiche_"
pdftk Fiche_tmp*.pdf cat output $fiche${name::-4}$pdf
# mv Fiche_tmp.pdf $fiche${name::-4}$pdf
rm Fiche_tmp*.pdf
rm Fiche_tmp*.tex
# rm Fiche_tmp.out
rm Fiche_tmp*.log
rm Fiche_tmp*.aux
# rm Fiche_tmp.synctex.gz
# rm -r _minted-*

# copy to flash drive
# echo ${fichier::-4}$pdf 
echo "Moving to USB..."
cp ${fichier::-4}$pdf /media/eb/USB/Print/
cp $fiche${name::-4}$pdf /media/eb/USB/Print/
# code ${name::-4}$pdf
echo "Done !"

#rm Fiche_tmp.synctex.gz
#cp %.pdf '/media/eb/USB STICK'
#cp %_soluce.pdf '/media/eb/USB STICK'
#cp Fiche_%.pdf '/media/eb/USB STICK'
