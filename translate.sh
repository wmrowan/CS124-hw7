#!/bin/sh
#node dictionary-scraper.js && node dictionary-translate.js && \
  cd stanford-postagger && \
  java -mx3000m -classpath stanford-postagger.jar edu.stanford.nlp.tagger.maxent.MaxentTagger -model models/english-bidirectional-distsim.tagger -textFile ../english.txt > ../english-tagged.txt \
  && cd ..
