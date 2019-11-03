#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, division

import sys
import argparse
import numpy as np
import enchant

SPM_SEPARATOR = "▁"


def main():
    args = parse_user_args()
    vocab = read_vocab(args.vocab, args.min_word_length, args.spm)

    debug("Initializing Enchant for:", args.dictionary)
    spell = enchant.Dict(args.dictionary)
    debug("Dictionary file:", spell.provider.file)

    debug("Generating confusion lists...")
    n = 0
    c = 0
    for word in vocab:
        confs_list = []
        word_clean = word.replace(SPM_SEPARATOR, '')
        if args.alpha and not word_clean.replace('-', '').isalpha():
            continue
        else:
            suggs = spell.suggest(word_clean)[:args.k_top]
            for i, sugg in enumerate(suggs):
                if sugg == word_clean:
                    continue
                # skip a suggestion if it's first letter has different casing than the original word
                if args.case_sensitive:
                    w = word_clean[0]
                    s = sugg[0]
                    if not (w.isupper() and s.isupper()) and not (w.islower() and s.islower()):
                        continue
                # add _ to suggestions if working on SentencePiece-segmented data
                sugg_tok = sugg
                if args.spm:
                    sugg_tok = SPM_SEPARATOR + sugg_tok
                if args.oov or (sugg_tok in vocab):
                    confs_list.append(sugg_tok)

        if confs_list:
            print(word, end='\t')
            print("\t".join(confs_list))
            c += 1

        n += 1
        if n % 5000 == 0:
            debug('[{}]'.format(n))

    debug("Confusion sets:", c)


def read_vocab(vocab_path, min_length, spm):
    debug("Loading vocab:", vocab_path)
    vocab = []
    with open(vocab_path) as vocab_io:
        for i, line in enumerate(vocab_io):
            try:
                word = line.strip().split('\t')[0]
                if spm and SPM_SEPARATOR not in word:
                    continue
                word_clean = word.replace(SPM_SEPARATOR, '')
                if len(word_clean) >= min_length and not any(c.isdigit() for c in word_clean):
                    vocab.append(word)
            except:
                # debug("Can't read the line:", line.rstrip())
                pass
    vocab = set(vocab)
    debug("Vocab size:", len(vocab))
    return vocab


def debug(*args):
    sys.stderr.write(' '.join(str(e) for e in args) + '\n')


def parse_user_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--vocab', required=True, help="vocab")
    parser.add_argument('-d', '--dictionary', required=True, help="dictionary", default="en_GB")
    parser.add_argument('-k', '--k-top', type=int, default=20)
    parser.add_argument('-m', '--min-word-length', type=int, default=2)
    parser.add_argument('-c', '--case-sensitive', action='store_true', help="suggestions have to have the same casing as the original word")
    parser.add_argument('--alpha', action='store_true', help="require all characters are alpha")
    parser.add_argument('--spm', action='store_true', help="assume texts segmented with SentencePiece")
    parser.add_argument('--oov', action='store_true', help="allow OOV suggestions")
    return parser.parse_args()


if __name__ == '__main__':
    main()
