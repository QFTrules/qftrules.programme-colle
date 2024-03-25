# Author: Eric Brillaux
# Date: 2021-08-22
# Version: 1.0
# Description: Convert a pdf file to a latex file
# Usage: math_pix_pdf_to_latex.sh <pdf file> <tex file>
# Example: math_pix_pdf_to_latex.sh 2021-08-22_11-00-00.pdf 2021-08-22_11-00-00.tex
# Dependencies: mpx
#!/bin/bash

# inputs
file=$1
directory=$2
archive=$3
pages=$4

# Prompt message in red
# RED='\033[0;31m'
# NC='\033[0m' # No Color
# printf "Please enter the ${RED}page range${NC} :\n"
# read pages

# cut pages necessary
cd $directory
# file_to_convert="file_to_convert.pdf"
pdftk $file cat $pages output "file_to_convert.pdf"
# echo "pdftk "$directory/$file" cat $pages output $file_to_convert"
# file_to_convert=$(basename "$file_to_convert")

# fetch username and password for mathpix account
# list_usernames=/home/eb/Dropbox/.latex/Commands/ident-mathspix-list.txt
# random_username=$(shuf -n 1 $list_usernames)
localmpx=mpx
# echo "$localmpx"
# printf "$random_username\nPhila618033%%"
# $localmpx logout
# printf "Phila618033%%" | printf "$random_username" |  $localmpx login

# convert pdf to latex  
# echo $file_to_convert
# echo "$directory/file_to_convert.tex"
# echo $directory
today=$(date +%Y_%m_%d)
# find . -name "$today_*.tex" -exec code {} \;
filename=$(find . -name "$today_*.tex")
corrected="_corrected.tex"
# mpx convert "./file_to_convert.pdf" "./file_to_convert.tex"
# unzip "file_to_convert.tex.zip" -d .
# /home/eb/anaconda3/bin/python3 /home/eb/Dropbox/.latex/Commands/change_width.py  $filename $archive
# unzip "file_to_convert.tex.zip" -d .
# open in vscode
# newfile=${filename::-4}$corrected
# printf "Please enter the ${RED}destinnation tex file${NC} among the list:\n"
# tree /home/eb/Dropbox/CPGE/Physique/Exercices/Recueil/ -L 2 -P "*.tex"
# read archive
# archive=$(find ~/Dropbox/CPGE/ -name "$archive")
# echo $archive
# sleep 0.5
# code $archive
# rm $filename
# rm ./file_to_convert.pdf
# rm ./file_to_convert.tex.zip
# /home/eb/anaconda3/bin/python3 /home/eb/Dropbox/.latex/Commands/mask_terminal.py