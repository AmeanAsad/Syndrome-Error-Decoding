import numpy as np

class LinearCode:
    def __init__(self, k, n):
        """
        k: Length of message
        n: Length of codeword
        """
        self.k = k
        self.n = n
        self.generator_mat = []
        self.parity_check = []
        self.syndrome_table = []

    def generator_matrix(self):
        self.generator_mat = np.zeros((self.k, self.n), dtype=int)
        A_matrix = np.ones((self.k, self.n-self.k), dtype=int)
        identity_i = np.identity(self.k, dtype=int)
        self.generator_mat[:, :self.k] = identity_i

        for x in range(self.n-self.k):
            A_matrix[x, x] = 0

        self.generator_mat[:, self.k:] = A_matrix
        return self.generator_mat

    def parity_check_matrix(self):
        generator_mat = self.get_generator_matrix()
        self.parity_check = np.zeros((self.n, self.n-self.k), dtype=int)
        self.parity_check[:self.k, :] = generator_mat[:, self.k:]
        self.parity_check[self.k:, :] = np.identity(self.n-self.k, dtype=int)
        return self.parity_check

    def syndrome_decoding_table(self):
        parity_check = self.get_parity_check_matrix()
        size = 2**(self.n-self.k) - 1
        iteration_counter = 0
        weight_counter = -1
        self.syndrome_table = {}

        for i in range(size):
            base_vector = np.zeros((1, self.n), dtype=int)
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