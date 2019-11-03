#!/bin/bash

MODELDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOTDIR="$( realpath "$MODELDIR/../.." )"

cat $1 | python $ROOTDIR/tools/remove_repetitions.py > $MODELDIR/devset.out.fix

timeout 3m $ROOTDIR/tools/m2scorer/m2scorer $MODELDIR/devset.out.fix $MODELDIR/devset.m2 \
	| tee $MODELDIR/devset.out.eval \
	| perl -ne 'print "$1\n" if(/^F.*: (\d\.\d+)/)' 2>/dev/null
