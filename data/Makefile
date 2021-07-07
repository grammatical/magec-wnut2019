SHELL=/bin/bash
THREADS=24
PARALLEL=parallel --no-notice --pipe -k -j $(THREADS) --block 50M

MARIAN=../models/tools/marian-dev/build
MARIANOPTS=--type lm-transformer --mini-batch 1 --after-batches 1 --learn-rate 0.0 --no-shuffle -w 100
TOOLS=../tools
MOSESSCRIPTS=$(TOOLS)/moses-scripts/scripts

SEED=1234
DATASIZE=100000000	# 100M segments
VOCABSIZE=32000		# 32k SPM vocab for model training
VOCABTXT=96000		# 96k vocab for noise generation

# extract language code from file path
define langcode
$(subst /,,$(dir $<))
endef

# spelling dictionaries for languages may not be named just by language codes
DICTIONARIES=en_GB de-common zh ru

.DELETE_ON_ERROR:
.SUFFIXES:
.PHONY: all news
.SECONDARY:


en-mono: en/mono.gz
en-vocab: en/vocab.spm en/vocab.txt
en-train: en/enchant.conf \
	en/mono.cor.gz \
	en/mono.enchant.tok.err.gz \
	en/mono.enchant.spell.tok.err.gz
en-weights: \
	en/mono.enchant.tok.spm.w2.gz \
	en/mono.enchant.spell.tok.spm.w2.gz

de-mono: de/mono.gz
de-vocab: de/vocab.spm de/vocab.txt
de-train: de/enchant.conf \
	de/mono.cor.gz \
	de/mono.enchant.tok.err.gz \
	de/mono.enchant.spell.tok.err.gz
de-weights: de/mono.enchant.spell.tok.w2.gz

ru-mono: ru/mono.gz
ru-vocab: ru/vocab.spm ru/vocab.txt
ru-train: ru/enchant.conf \
	ru/mono.cor.gz \
	ru/mono.enchant.tok.err.gz \
	ru/mono.enchant.spell.tok.err.gz
ru-weights: ru/mono.enchant.spell.tok.w2.gz


###############################################################################
### SYNTHETIC ERRORS

%.spell.tok.err.gz: %.tok.err.gz
	pigz -dc $^ | $(PARALLEL) python $(TOOLS)/mix_chars.py -p 0.01 | pigz > $@


%.enchant.tok.err.gz: %.tok.err.gz
	pigz -dc $< | $(PARALLEL) python3 $(TOOLS)/scramble.py -c $(call langcode)/enchant.conf -e 0.15 --seed $(SEED) --repeat | pigz > $@
%/enchant.conf: %/vocab.txt
	python3 $(TOOLS)/conf_lists_enchant.py -v $< -d $(filter $(call langcode)%,$(DICTIONARIES)) -c | sort > $@


%.random.tok.err.gz: %.tok.err.gz
	pigz -dc $< | $(PARALLEL) python3 $(TOOLS)/scramble_randomly.py -v $(call langcode)/vocab.txt -e 0.1 --seed $(SEED) | pigz > $@


%.tok.err.gz: %.tok.gz
	cp $< $@

%.enchant.tok.w2.gz: %.enchant.tok.spm.err %.tok.spm.cor
	paste $^ | $(PARALLEL) python $(TOOLS)/edit_weights.py -w 2 | pigz > $@
%.enchant.spell.tok.w2.gz: %.enchant.spell.tok.spm.err %.tok.spm.cor
	paste $^ | $(PARALLEL) python $(TOOLS)/edit_weights.py -w 2 | pigz > $@


%/vocab.txt: %/mono.shuf.tok.gz
	pigz -dc $< | head -n 10000000 | bash -x create_vocab.sh $(call langcode) | head -n $(VOCABTXT) > $@

%/mono.shuf.tok.gz: %/mono.cor.gz
	pigz -dc $< | shuf | pigz > $@


###############################################################################
### MONOLINGUAL DATA & VOCABS

%.tok.spm.err: %.tok.err.gz
	pigz -dc $< | $(PARALLEL) $(MARIAN)/spm_encode --model=$(call langcode)/vocab.spm > $@
%.tok.spm.cor: %.tok.gz
	pigz -dc $< | $(PARALLEL) $(MARIAN)/spm_encode --model=$(call langcode)/vocab.spm > $@


%/vocab.spm: %/mono.cor.gz
	cd $* && $(MARIAN)/marian $(MARIANOPTS) -t ../$< -v ../$@ --dim-vocabs $(VOCABSIZE) || echo OK
	rm -f $*/model.npz*


%.clean.tok.gz: %.tok.gz
	pigz -dc $< | parallel --no-notice --pipe -k -j $(THREADS) --block 50M \
		'python ./clean_mono.py en 2> $@.rejected | perl $(MOSESSCRIPTS)/recaser/detruecase.perl' \
		| pigz > $@

%/mono.cor.gz: %/mono.gz
	cat $^ | pigz -dc \
		| head -n $(DATASIZE) \
		| parallel --no-notice --pipe -k -j $(THREADS) --block 50M \
		' perl $(MOSESSCRIPTS)/tokenizer/normalize-punctuation.perl | python3 $(TOOLS)/spacy_tok.py $*' \
	| pigz > $@

%/mono.gz: %/download_mono.sh
	cd $* && bash -x download_mono.sh


###############################################################################
### HELPERS

clean:
	rm -f data
