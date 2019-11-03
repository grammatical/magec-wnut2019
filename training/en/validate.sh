#!/bin/bash

MODELDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOTDIR="$( realpath "$MODELDIR/../.." )"

cat $1 | python $ROOTDIR/tools/remove_repetitions.py > $MODELDIR/devset.out.fix

python3 $ROOTDIR/tools/errant/parallel_to_m2.py -orig $MODELDIR/devset.err -cor $MODELDIR/devset.out.fix -out $MODELDIR/devset.out.m2 &> $MODELDIR/devset.out.m2.stderr
python3 $ROOTDIR/tools/errant/compare_m2.py -ref $MODELDIR/devset.m2 -hyp $MODELDIR/devset.out.m2 2> $MODELDIR/devset.out.m2.eval.stderr \
    | tee $MODELDIR/devset.out.m2.eval \
    | sed -n '4p' | cut -f6
