#!/bin/bash -xe

wget -nc http://www.sfs.uni-tuebingen.de/~adriane/download/wnut2018/data.tar.gz
tar zxvf data.tar.gz

cp data/fm-{dev,test}.* .

ln -s fm-dev.src devset.err
ln -s fm-dev.trg devset.cor
ln -s fm-dev.m2  devset.m2

# Clean trainset from sentences included in devset
paste data/fm-train.{src,trg} | python3 ./filter_devset.py devset.cor 2> train.rejected.txt > train.txt
cut -f1 train.txt > train.err
cut -f2 train.txt > train.cor
