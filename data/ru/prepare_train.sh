#!/bin/bash

TOOLS=../tools

test -e RozovskayaRothTACL2018-dataset.zip || { echo "The ZIP file with the dataset is not here. Copy it into this folder first, then re-run the script."; exit 1; }

unzip RozovskayaRothTACL2018-dataset.zip
mv RozovskayaRothTACL2018-dataset/RULEC-GEC.{dev,test}.M2 .

python3 $TOOLS/parallel_from_m2.py RULEC-GEC.dev.M2 -out RULEC-GEC.dev.txt
cut -f1 RULEC-GEC.dev.txt > devset.err
cut -f2 RULEC-GEC.dev.txt > devset.cor

python3 $TOOLS/parallel_from_m2.py RULEC-GEC.test.M2 -out RULEC-GEC.test.txt
cut -f1 RULEC-GEC.test.txt > testset.err
cut -f2 RULEC-GEC.test.txt > testset.cor
