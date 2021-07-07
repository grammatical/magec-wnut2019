#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import codecs

devset_file = sys.argv[1]
devset = []
with open(devset_file) as f:
    devset = [l.strip() for l in f.readlines()]
devset = set(devset)

sys.stdin = codecs.getreader('utf8')(sys.stdin.detach(), errors='ignore')

for line in sys.stdin:
    cor = line.rstrip().split('\t')[1]
    if cor not in devset:
        print(line.strip())
    else:
        sys.stderr.write(line)
