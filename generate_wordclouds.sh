#!/bin/bash

mkdir -p imgs

wordcloud_cli --text full.txt --width 1500 --height 800 --imagefile imgs/full_cloud.png --stopwords stopwords.txt
wordcloud_cli --text corpus.txt --width 1500 --height 800 --imagefile imgs/wzor_cloud.png --stopwords stopwords.txt
wordcloud_cli --text problem.txt --width 1500 --height 800 --imagefile imgs/problem_cloud.png --stopwords stopwords.txt
