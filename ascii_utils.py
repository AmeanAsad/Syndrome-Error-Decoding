#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 15:55:25 2019

@author: ameanasad
"""
import csv
import random
import string

# Move the file opening inside a function to handle the resource better
def load_words_dictionary():
    words_dictionary = {}
    try:
        with open('words.csv', 'rt', encoding='utf-8') as word_file:
            reader = csv.reader(word_file)
            for row in reader:
                word = row[1].strip()
                word = word.replace("'", "").replace("-", "").replace("/", "")
                words_dictionary[row[0]] = word
    except FileNotFoundError:
        print("Warning: words.csv file not found")
        return {}
    return words_dictionary

def create_ascii_mappings():
    ascii_char = string.ascii_lowercase + string.ascii_uppercase
    ascii_to_bin = {}
    bin_to_ascii = {}

    for char in ascii_char:
        encoded_char = bin(int.from_bytes(char.encode(), 'little'))
        ascii_to_bin[char] = encoded_char[0] + encoded_char[2:]
        bin_to_ascii[ascii_to_bin[char]] = char

    return ascii_to_bin, bin_to_ascii

def transform_text_to_binary(text):

    ascii_to_bin, _ = create_ascii_mappings()

    binary_decoding = []
    for char in text:
        if char in ascii_to_bin.keys():
            bit_vector = [int(bit) for bit in ascii_to_bin[char]]
            binary_decoding.append(bit_vector)
    return binary_decoding

def randomized_text_generator(word_number):
    words_dictionary = load_words_dictionary()
    if not words_dictionary:
        return "test" * word_number  # fallback if dictionary is empty

    string = ''
    for _ in range(word_number):
        word_index = random.randint(2, 4999)
        word = words_dictionary.get(str(word_index), "test").strip()
        string = word + " " + string

    return string