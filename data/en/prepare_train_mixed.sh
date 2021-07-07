#!/bin/bash

MARIAN=../../models/tools/marian-dev/build
TOOLS=../tools

PARALLEL="parallel --no-notice --pipe -k -j $THREADS --block 50M"

mkdir -p mixed

for i in `seq -w 1 10`; do
    for j in `seq 1 10`; do paste train.{err,cor} >> mixed/train.part$i ; done

    cut -f1 mixed/train.part$i | python3 $TOOLS/scramble.py -c enchant.conf -e 0.05 --repeat --quiet | python $TOOLS/mix_chars.py -p 0.005 > mixed/train.part$i.enchant
    cut -f2 mixed/train.part$i > mixed/train.part$i.cor
    paste mixed/train.part$i.{enchant,cor} >> mixed/train.part$i

    cat mixed/mono.part$i mixed/train.part$i | shuf > mixed/corpus.part$i

    cut -f1 mixed/corpus.part$i > mixed/corpus.part$i.err
    cat mixed/corpus.part$i.err | $MARIAN/spm_encode --model=vocab.spm > mixed/corpus.part$i.spm.err
    cut -f2 mixed/corpus.part$i > mixed/corpus.part$i.cor
    cat mixed/corpus.part$i.cor | $MARIAN/spm_encode --model=vocab.spm > mixed/corpus.part$i.spm.cor

    paste mixed/corpus.part$i.spm.{err,cor} | python3 $TOOLS/edit_weights.py -w 2 > mixed/corpus.part$i.w2
done

cat mixed/corpus.part??.err | pigz > train.mixed.err.gz
cat mixed/corpus.part??.cor | pigz > train.mixed.cor.gz
cat mixed/corpus.part??.w2  | pigz > train.mixed.w2.gz
