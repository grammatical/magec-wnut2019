#!/bin/bash -x

wget -nc -i news.urls -O news.gz
pigz -dc news.gz | wc -l | tee news.wc
