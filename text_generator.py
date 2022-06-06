#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 15:55:25 2019

@author: ameanasad
"""
import csv
import random

word_file = open('words.csv', 'rt', encoding='utf')
reader = csv.reader(word_file)


words_dictionary = {}
for row in reader:
    word = row[1].strip()
    word = word.replace("'", "")
    word = word.replace("-", "")
    word = word.replace("/", "")
    words_dictionary[row[0]] = word


def randomized_text_generator(word_number):
    string = ''
    for word in range(word_number):
        word_index = random.randint(2, 4999)
        word = words_dictionary[str(word_index)].strip()
        string = word + " " + string

    return string
