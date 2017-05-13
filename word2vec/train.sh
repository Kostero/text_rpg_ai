#!/bin/bash
echo "cat data/*.txt > data/_train1.tmp"
cat data/*.txt > data/_train1.tmp
echo "python preprocess.py data/_train1.tmp data/_train2.tmp"
echo "this may take a loooong time..."
python preprocess.py data/_train1.tmp data/_train2.tmp
echo "bin/word2phrase -train data/_train2.tmp -output data/_train3.tmp -threshold 600 -debug 2"
bin/word2phrase -train data/_train2.tmp -output data/_train3.tmp -threshold 600 -debug 2
echo "bin/word2vec -train data/_train3.tmp -output data/vec.bin -size 200 -window 5 -sample 1e-4 -negative 5 -hs 0 -cbow 1 -iter 3 -binary 1 -threads 3"
bin/word2vec -train data/_train3.tmp -output data/vec.bin -size 200 -window 5 -sample 1e-4 -negative 5 -hs 0 -cbow 1 -iter 3 -binary 1 -threads 3
echo "cleanup"
rm data/_train*.tmp