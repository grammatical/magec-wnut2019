#!/bin/bash -v

set -e

ROOTDIR="$( realpath ../.. )"
MARIAN=$ROOTDIR/marian-dev/build
DATA=$ROOTDIR/data/de
MODELDIR=.

$MARIAN/marian --type lm-transformer \
    --model $MODELDIR/lm.npz \
    -d 0 1 2 3 \
    --train-sets $DATA/mono.cor.gz --shuffle-in-ram --tempdir tmp \
    --vocabs $DATA/vocab.{spm,spm} --tied-embeddings-all \
    --max-length 150 --max-length-crop \
    --enc-depth 6 --dec-depth 6 --transformer-heads 16 \
    --dim-emb 1024 --transformer-dim-ffn 4096 --transformer-ffn-activation relu --transformer-postprocess dan \
    --dropout-src 0.2 --dropout-trg 0.1 --transformer-dropout 0.3 --transformer-dropout-ffn 0.1 --transformer-dropout-attention 0.1 \
    --exponential-smoothing --label-smoothing 0.1 \
    --mini-batch-fit -w 9500 --mini-batch 1000 --maxi-batch 1000 --sync-sgd --optimizer-delay 6 \
    --learn-rate 0.0002 --lr-warmup 16000 --lr-decay-inv-sqrt 16000 --lr-report \
    --optimizer-params 0.9 0.998 1e-09 --clip-norm 0 \
    --cost-type perplexity \
    --valid-metrics perplexity \
    --valid-sets $DATA/devset.cor \
    --valid-mini-batch 16 --beam-size 12 --normalize 1.0 \
    --early-stopping 5 --after-epochs 10 \
    --valid-freq 5000 --save-freq 5000 --disp-freq 500 --disp-first 10 \
    --overwrite --keep-best \
    --log $MODELDIR/train.log --valid-log $MODELDIR/valid.log
