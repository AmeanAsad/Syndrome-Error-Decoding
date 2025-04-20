import numpy as np
import random
from linear_code import LinearCode
from ascii_utils import create_ascii_mappings

class AsciiCode:
    def __init__(self, k, n):
        # initialize necessary matrices using the LinearCode class
        linear_code = LinearCode(k, n)
        self.generator_matrix = linear_code.get_generator_matrix()
        self.parity_check = linear_code.get_parity_check_matrix()
        self.syndrome_table = linear_code.get_syndrome_decoding_table()

        # Get ASCII mappings
        self.ascii_to_bin, self.bin_to_ascii = create_ascii_mappings()

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
        Decode single letters using syndrome decoding.
        Return most probable decoded letter based on linear code provided
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