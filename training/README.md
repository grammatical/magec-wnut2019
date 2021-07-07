# Minimally-Augmented Grammatical Error Correction

This repository contains models and training scripts for our MAGEC systems for
English, German and Russian described in R. Grundkiewicz, M. Junczys-Dowmunt,
_Minimally-Augmented Grammatical Error Correction_, W-NUT 2019.

This directory contains training scripts.

## Overview

The general overview of the MAGEC training recipe:

1. Download or generate synthetic parallel data following instructions from
   `../data`.
2. Train 1-3 models using `train.sh`.
3. Train a language model using `lm.sh`.
4. If authentic parallel training data is available, fine-tune each model on
   a mixture of synthetic and authentic parallel data using `finetune.sh`.
5. Build a model ensemble from 1-3 translation models and the language model.
   Grid search the weights on a devset if available.
