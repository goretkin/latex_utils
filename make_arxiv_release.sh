#!/usr/bin/env bash


git --work-tree=/tmp/arxiv checkout HEAD -- .
cd /tmp/arxiv
latexmk -pdf -output-directory=/tmp/arxiv_build main.tex
# an attempt to keep using biblatex
cp main.bbl /tmp/arxiv/main.bbl
tar -cf /tmp/arxiv_release/arxiv.tar --directory=/tmp/arxiv/ .
/tmp/arxiv_release/arxiv.tar ~/Downloads/