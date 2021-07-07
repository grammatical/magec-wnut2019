# Minimally-Augmented Grammatical Error Correction

This repository contains models and training scripts for our MAGEC systems for
English, German and Russian described in R. Grundkiewicz, M. Junczys-Dowmunt,
_Minimally-Augmented Grammatical Error Correction_, W-NUT 2019.

This directory contains training data and scripts to synthesize it.

## Synthetic MAGEC data

Download the synthetic training data for English, German and Russian used in
original experiments from:

* http://data.statmt.org/romang/gec-wnut19/data.en.tgz
* http://data.statmt.org/romang/gec-wnut19/data.de.tgz
* http://data.statmt.org/romang/gec-wnut19/data.ru.tgz

See instructions below to generate the data from scratch.

## Generating synthetic training data

First install Marian in `../models/tools/marian-dev`, then run:

    cd tools; bash -x install.sh; cd ..
    make all

See `Makefile` for more details.
