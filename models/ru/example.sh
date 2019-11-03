#!/bin/bash -v
echo "Мни стрелять хне из автоматов , из тяжелого оружия ." \
    | ../marian-dev/build/marian-decoder -c config.yml $@
