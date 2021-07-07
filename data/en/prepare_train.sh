#!/bin/bash

set -e

MARIAN=../../models/tools/marian-dev/build
TOOLS=../tools

# Prepare authentic parallel data
$MARIAN/spm_encode < train.err --model=vocab.spm > train.spm.err
$MARIAN/spm_encode < train.cor --model=vocab.spm > train.spm.cor
paste train.spm.err train.spm.cor | python3 $TOOLS/edit_weights.py -w 2 > train.w2

# Create data for fine-tuning: 2M synthetic + authentic x20
pigz -dc mono.cor.gz                   | head -n 2000000 > train.2m.cor
pigz -dc mono.enchant.spell.tok.err.gz | head -n 2000000 > train.2m.err
pigz -dc mono.enchant.spell.tok.w2.gz  | head -n 2000000 > train.2m.w2

for i in `seq 1 20`; do cat train.err >> train.2m.err ; done
for i in `seq 1 20`; do cat train.cor >> train.2m.cor ; done
for i in `seq 1 20`; do cat train.w2  >> train.2m.w2  ; done
