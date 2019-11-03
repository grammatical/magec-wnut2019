#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, division

import sys
import random
import argparse


def main():
    args = parse_user_args()

    if args.seed:
        random.seed(args.seed)

    conf = dict()
    with open(args.conf, 'r') as cf:
        for line in cf:
            fields = line.rstrip("\n").split("\t")
            conf[fields[0]] = fields[1:]

    senProb = args.sen_prob
    errProb = args.err_prob

    probSub = args.sub_prob
    probSwp = args.swp_prob
    probDel = args.del_prob
    probIns = args.ins_prob

    total = 100
    actions = []
    for i in range(int(probSub * total)):
        if args.repeat:
            actions.append(subrep)
        else:
            actions.append(sub)
    for i in range(int(probSwp * total)):
        actions.append(swap)
    for i in range(int(probDel * total)):
        actions.append(delete)
    for i in range(int(probIns * total)):
        actions.append(insert)

    n = 0
    for line in sys.stdin:
        line = line.rstrip()
        sentence = line.split()

        ps = random.uniform(0.0, 1.0)
        if sentence and ps < senProb:
            p = abs(random.normalvariate(errProb / senProb, 0.2))
            c = int(p * len(sentence))

            for i in range(c):
                random.choice(actions)(sentence, conf)

        # sys.stderr.write(" ".join(sentence) + "\n")
        print(" ".join(sentence))

        n += 1
        if not args.quiet and n % 100000 == 0:
            sys.stderr.write('[{}]\n'.format(n))

def subrep(cands, conf):
    cont = True
    reps = 0
    while cont:
        i = random.randrange(len(cands))
        if cands[i] in conf:
            cands[i] = random.choice(conf[cands[i]])
            cont = False
        reps += 1
        if reps > 5:
            cont = False

def sub(cands, conf):
    i = random.randrange(len(cands))
    if cands[i] in conf:
        cands[i] = random.choice(conf[cands[i]])

def swap(cands, conf):
    if len(cands) < 2:
        return
    i = random.randrange(len(cands) - 1)
    cands[i], cands[i + 1] = cands[i + 1], cands[i]

def delete(cands, conf):
    i = random.randrange(len(cands))
    cands.pop(i)

def insert(cands, conf):
    i = random.randrange(len(cands))
    j = random.randrange(len(cands))
    cands.insert(i, cands[j])


def parse_user_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--conf', required=True, help="confusion list")
    parser.add_argument('-e', '--err_prob', help="error ratio", type=float, default=0.15)
    parser.add_argument('-s', '--sen_prob', help="error sentence ratio", type=float, default=1.0)
    parser.add_argument('--sub_prob', help="sub probability", type=float, default=0.7)
    parser.add_argument('--swp_prob', help="swap probability", type=float, default=0.1)
    parser.add_argument('--del_prob', help="deletion probability", type=float, default=0.1)
    parser.add_argument('--ins_prob', help="insertion probability", type=float, default=0.1)
    parser.add_argument('--seed', type=int)
    parser.add_argument('--repeat', action='store_true')
    parser.add_argument('--quiet', action='store_true')
    return parser.parse_args()


if __name__ == '__main__':
    main()
