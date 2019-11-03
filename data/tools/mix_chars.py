#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import argparse
import random
import string

MAX_ATTEMPTS = 5
CHARS = string.ascii_lowercase


def main():
    args = parse_user_args()

    if args.seed:
        random.seed(args.seed)

    probSub = args.sub_prob
    probSwp = args.swp_prob
    probDel = args.del_prob
    probIns = args.ins_prob

    total = 100
    actions = []
    for i in range(int(probSub * total)):
        actions.append(substitute)
    for i in range(int(probSwp * total)):
        actions.append(swap)
    for i in range(int(probDel * total)):
        actions.append(delete)
    for i in range(int(probIns * total)):
        actions.append(insert)


    for i, line in enumerate(sys.stdin):
        sentence = list(line.rstrip())

        p = abs(random.normalvariate(args.prob, 0.002))
        c = int(p * len(sentence))
        for i in range(c):
            random.choice(actions)(sentence)

        if args.duplicate and c > 0:
            print(line.rstrip())
        print(''.join(sentence))


def substitute(text):
    for _ in range(MAX_ATTEMPTS):
        i = random.randint(0, len(text) - 1)
        if text[i] in CHARS:
            text[i] = random.choice(CHARS)
            break
        else:
            continue


def swap(text):
    for _ in range(MAX_ATTEMPTS):
        i = random.randint(0, len(text) - 2)
        if text[i].isalpha() and text[i + 1].isalpha():
            text[i], text[i + 1] = text[i + 1], text[i]
            break
        else:
            continue


def delete(text):
    for _ in range(MAX_ATTEMPTS):
        i = random.randint(0, len(text) - 1)
        if text[i] in CHARS:
            del text[i]
            break
        else:
            continue


def insert(text):
    i = random.randint(1, len(text) - 2)
    text.insert(i, random.choice(CHARS))


def parse_user_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--prob", type=float, default=0.01)
    parser.add_argument("-d", "--duplicate", action='store_true')
    parser.add_argument('--sub_prob', help="sub probability", type=float, default=0.7)
    parser.add_argument('--swp_prob', help="swap probability", type=float, default=0.1)
    parser.add_argument('--del_prob', help="deletion probability", type=float, default=0.1)
    parser.add_argument('--ins_prob', help="insertion probability", type=float, default=0.1)
    parser.add_argument("--seed", type=int)
    return parser.parse_args()


if __name__ == "__main__":
    main()
