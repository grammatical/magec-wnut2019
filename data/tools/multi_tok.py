#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Tokenize sentences line-by-line using Spacy or MyStem
# Usage: multi_tok.py [en|de|ru]

from __future__ import print_function, unicode_literals

import sys

lang = sys.argv[1] if len(sys.argv) > 1 else 'en'

if lang == 'ru':
    import pymystem3
    mystem = pymystem3.Mystem()
    for line in sys.stdin:
        toks = [t['text'] for t in mystem.analyze(line.strip())]
        print(' '.join(' '.join(toks).split()))
        
else:
    import spacy
    nlp = spacy.load(lang, parser=False, entity=False)
    for line in sys.stdin:
        toks = nlp.tokenizer(line.strip())
        print(' '.join(t.text for t in toks))
