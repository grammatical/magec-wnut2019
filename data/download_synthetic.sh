#!/bin/bash

# Download synthetic data used in original experiments: vocabs, native
# monolingual data and their counterparts with synthetic errors
for lc in en de ru; do
    cd $lc/
    wget -nc http://data.statmt.org/romang/gec-wnut19/data.$lc.tgz
    tar zxvf data.$lc.tgz
    cd ..
done
