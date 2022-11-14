#!/bin/bash

mkdir -p imgs

wordcloud_cli --text outputs/full.txt --width 1500 --height 800 --imagefile imgs/full_cloud.png --stopwords extras/stopwords.txt
wordcloud_cli --text outputs/corpus.txt --width 1500 --height 800 --imagefile imgs/wzor_cloud.png --stopwords extras/stopwords.txt
wordcloud_cli --text outputs/problem.txt --width 1500 --height 800 --imagefile imgs/problem_cloud.png --stopwords extras/stopwords.txt
