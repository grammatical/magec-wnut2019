#!/bin/bash

# Install Ubuntu and Python packages

# Enchant
apt-get install enchant
pip3 install pyenchant

# Tokenization from Spacy
pip3 install --upgrade nltk spacy==1.9.0
python3 -m spacy download en
python3 -m spacy download de

# Tokenizer for Russian
pip3 install git+https://github.com/nlpub/pymystem3

# Spell-checking dictionaries
apt-get install aspell-en
apt-get install aspell-de
apt-get install aspell-ru



