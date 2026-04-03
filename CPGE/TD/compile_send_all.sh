#!/bin/bash
# -*- coding: utf-8 -*-
/home/eb/anaconda3/bin/python3 $HOME/Dropbox/.latex/Commands/QRcode.py
for fichier in $(find . -name *.tex);
do
    doc=$(dirname $fichier)
    abs_dir=$(realpath $doc)
    cd $doc
    # echo "Absolute directory: $abs_dir"
    # echo $(pwd)
    fichier=$(basename $fichier)
    file_noext=$(echo $fichier | cut -d'.' -f1)
    # echo $fichier 
    # echo $file_noext    
    pdflatex -synctex=1 -interaction=nonstopmode -file-line-error -shell-escape $fichier
    pdflatex -synctex=1 -interaction=nonstopmode -file-line-error -shell-escape $fichier
    bash $HOME/Dropbox/.latex/Commands/build-soluce.sh $abs_dir $file_noext
    /home/eb/anaconda3/bin/python3 $HOME/Dropbox/.latex/Commands/send_to_cahier.py $abs_dir/$fichier
    cd ..
done
