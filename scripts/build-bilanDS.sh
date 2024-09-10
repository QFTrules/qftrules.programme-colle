#!/bin/bash
# find ods file in folder
note_file=$1
folder_path=$(dirname $1)
dir_name=$2
# folder_path=$1
cd $folder_path
# echo $folder_path
substring=$(basename "$note_file" | cut -d '_' -f 1)
# echo $substring
tmp_dir="$dir_name/tmp/bilanDS_tmp"
sty_file="$dir_name/templates/bilanDS.sty"
py_file="$dir_name/scripts/bilanDS.py"
# rm -r $tmp_dir
mkdir $tmp_dir
python $py_file $note_file $tmp_dir $sty_file
# get folder path of note_file
# create tmp file if not already existent
# for all .tex files
cd $tmp_dir
# echo "Processing $note_file"
for fichier in $(ls *.tex);
do
    # echo "Processing $fichier"
    pdflatex -synctex=1 --shell-escape -interaction=nonstopmode -output-directory=$tmp_dir $fichier > /dev/null &
done
# wait for parallel runs of pdflatex to finish
wait
# use pdftk to concatenate all pdf files in a single file
# echo $folder_path/"$substring"_bilan.pdf
pdftk *_bilan.pdf cat output $folder_path/"$substring"_bilan.pdf
echo $folder_path/"$substring"_bilan.pdf
# remove all tmp files
# rm 
cd ..
rm -r $tmp_dir
