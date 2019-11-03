#!/bin/bash -v
echo "I though so I played a pretty good , its was a realy longer match ." \
    | ../marian-dev/build/marian-decoder -c config.yml $@
