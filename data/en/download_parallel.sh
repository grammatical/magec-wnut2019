#!/bin/bash -xe

TOOLS=../tools

wget -nc https://www.cl.cam.ac.uk/research/nl/bea2019st/data/wi+locness_v2.1.bea19.tar.gz
tar zxvf wi+locness_v2.1.bea19.tar.gz

cat wi+locness/m2/ABCN.dev.gold.bea19.m2 > devset.m2
python3 $TOOLS/parallel_from_m2.py devset.m2 -out devset.txt
cut -f1 devset.txt > devset.err
cut -f2 devset.txt > devset.cor

cat wi+locness/m2/*.train.gold.bea19.m2  > train.m2
python3 $TOOLS/parallel_from_m2.py train.m2 -out train.txt
cut -f1 train.txt > train.err
cut -f2 train.txt > train.cor
