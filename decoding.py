#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: ameanasad
"""
import numpy as np
import random
import string


ascii_char = string.ascii_lowercase + string.ascii_uppercase
ascii_to_bin = {}
bin_to_ascii = {}

for char in ascii_char:
    encoded_char = bin(int.from_bytes(char.encode(), 'little'))
    ascii_to_bin[char] = encoded_char[0] + encoded_char[2:]
    bin_to_ascii[ascii_to_bin[char]] = char


def transform_text_to_binary(text):

    binary_decoding = []
    for char in text:
        if char in ascii_to_bin.keys():
            bit_vector = [int(bit) for bit in ascii_to_bin[char]]
            binary_decoding.append(bit_vector)
    return binary_decoding


class LinearCode(object):
    def __init__(self, k, n):
        """
        k: Length of message
        n: Length of codeword 
        - Here empty instances of the generator matrix, parity check matrix
        and syndrome table are created to make them accessible throughout 
        the class and to return them without having to call the function.
        """
        self.k = k
        self.n = n

        # Generate empty instances just to have them accessible in the class.
        self.generator_mat = []
        self.parity_check = []
        self.syndrome_table = []

    def generator_matrix(self):
        """
        - Uses the empty generator matrix instance. 
        - First creates a k by n empty matrix to represent the skeleton of the 
        generator matrix.
        - A_matrix is the a k by (n-k) matrix which has linearly independent 
        column vectors. 
        - Identity_i is a k by k matrix. 
        """
        self.generator_mat = np.zeros((self.k, self.n), dtype=int)
        A_matrix = np.ones((self.k, self.n-self.k), dtype=int)

        identity_i = np.identity(self.k, dtype=int)
        self.generator_mat[:, :self.k] = identity_i

        # This loop edits the A_matrix to make the column vectors linearly ind.
        for x in range(self.n-self.k):
            A_matrix[x, x] = 0

        self.generator_mat[:, self.k:] = A_matrix

#        for i in range(self.k):
#            print(self.generator_mat[i,:])

        return self.generator_mat

    def parity_check_matrix(self):
        """
        - The generator matrix is used to construct part of the parity check by 
        taking the A matrix. 
        - The other part is constructed using the (n-k) by (n-k) identity matrix

        """

        generator_mat = self.get_generator_matrix()

        # Initialize empty parity check matrix
        self.parity_check = np.zeros((self.n, self.n-self.k), dtype=int)
        # Use A_matrix of the generator matrix to construct first part
        self.parity_check[:self.k, :] = generator_mat[:, self.k:]
        # Add the identity matrix to the second part
        self.parity_check[self.k:, :] = np.identity(self.n-self.k, dtype=int)


#        for i in range(self.n):
#            print(self.parity_check[i,:])

        return self.parity_check

    def syndrome_decoding_table(self):
        """
        - Develops a  syndrome table of size 2^(n-k) - 1
        - The syndromes are developed by weighted vectors. Meaning all vectors
        with hamming weight 1 are tested first and so on.
        - Returns a dictionary mapping each syndrome to its corresponding weighted
        vector.
        """
        parity_check = self.get_parity_check_matrix()

        size = 2**(self.n-self.k) - 1
        iteration_counter = 0
        weight_counter = -1

        self.syndrome_table = {}

        for i in range(size):
            base_vector = np.zeros((1, self.n), dtype=int)

            # increase the weight by 1 every time the loop exceed the vector size.
            if iteration_counter == self.n:
                iteration_counter = 0
                weight_counter += 1
                base_vector[0, :weight_counter] = 1

            syndrome_vector = base_vector[0, :]
            syndrome_vector[iteration_counter] = 1
            syndrome = (1*np.matmul(syndrome_vector, parity_check)) % 2
            if tuple(syndrome) not in self.syndrome_table:
                self.syndrome_table[tuple(syndrome)] = 1*syndrome_vector
            iteration_counter += 1

        return self.syndrome_table

    def get_generator_matrix(self):

        if len(self.generator_mat) == 0:
            self.generator_mat = self.generator_matrix()

        return self.generator_mat

    def get_parity_check_matrix(self):
        if len(self.parity_check) == 0:
            self.parity_check = self.parity_check_matrix()

        return self.parity_check

    def get_syndrome_decoding_table(self):
        if len(self.syndrome_table) == 0:
            self.synrome_table = self.syndrome_decoding_table()

        return self.syndrome_table


class AsciiCode(object):

    def __init__(self, k, n):

        # initialize nessecary matrices using the LinearCode class
        linear_code = LinearCode(k, n)
        self.generator_matrix = linear_code.get_generator_matrix()
        self.parity_check = linear_code.get_parity_check_matrix()
        self.syndrome_table = linear_code.get_syndrome_decoding_table()

        ascii_char = string.ascii_lowercase + string.ascii_uppercase

        self.ascii_to_bin = {}
        self.bin_to_ascii = {}

        # Develop a dictionary that maps letters to corresponding ASCII binary represenations
        for char in ascii_char:
            encoded_char = bin(int.from_bytes(char.encode(), 'little'))
            self.ascii_to_bin[char] = encoded_char[0] + encoded_char[2:]
            self.bin_to_ascii[self.ascii_to_bin[char]] = char

        self.code_words = {}
        # Create code words dictionary based on the generator matrix
        for word in self.ascii_to_bin:
            binary_str = self.ascii_to_bin[word]
            binary_vector = [int(i) for i in binary_str]
            code_word_vector = np.matmul(
                binary_vector, self.generator_matrix) % 2

            self.code_words[tuple(code_word_vector)] = word

    def decode_letter(self, received_letter):
        """
         - Decode single letters using syndrome decoding.
         - Return most probable decoded letter based on linear code provided
        """
        syndrome = (np.matmul(received_letter, self.parity_check)) % 2

        try:
            error_vector = self.syndrome_table[tuple(syndrome)]
        except KeyError:
            error_vector = random.choice(list(self.syndrome_table.values()))
        letter_vector = (error_vector + received_letter) % 2

        try:
            return self.code_words[tuple(letter_vector)]
        except KeyError:

            return random.choice(list(self.code_words.values()))

    def get_generator_mat(self):
        return self.generator_matrix

    def get_code_words(self):
        return self.code_words
