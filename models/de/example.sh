#!/bin/bash -v
echo "So ist est ihnen möglich zwischen des Automodel Golf und der sportart Golf zu unterscheide ." \
    | ../marian-dev/build/marian-decoder -c config.yml $@
