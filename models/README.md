# Minimally-Augmented Grammatical Error Correction

This repository contains models and training scripts for our MAGEC systems for
English, German and Russian described in R. Grundkiewicz, M. Junczys-Dowmunt,
_Minimally-Augmented Grammatical Error Correction_, W-NUT 2019.

This subdirectory contains MAGEC systems for English, German and Russian, used
in the paper.

## Instructions

1. Download and compile Marian with SentencePiece support:

        git clone https://github.com/marian-nmt/marian-dev
        mkdir -p marian-dev/build
        cd marian-dev/build
        cmake .. -DUSE_SENTENCEPIECE=on
        make -j8
        cd ../..

    See [the official documentation](https://marian-nmt.github.io/docs/) for
    more information.

1. Download models, for example English:

        cd en
        bash download.sh

1. Run the example script:

        bash example.sh -d 0

     `d 0` means it will run on GPU 0. The input is a tokenized text as
     described in the paper.

