all: marian-dev

marian-dev:
	git clone https://github.com/marian-nmt/marian-dev
	mkdir -p marian-dev/build
	cd marian-dev/build && cmake .. -DUSE_SENTENCEPIECE=on && make -j8

.PHONY: all
