#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
I wrote this simulation to test the accuracy of the developed linear code.
The functions below are not nessecary for the LinearCode class to work properly
but just provide an elegant demonstration of how the code can be used to evaluate
syndrome decoding as an efficient algorithm for error correction. I developed a
randomized text generator to get my text"

@author: ameanasad
"""

import numpy as np
import random
import matplotlib.pyplot as pl
import time
from ascii_code import AsciiCode, LinearCode
from ascii_utils import randomized_text_generator, transform_text_to_binary


def distort_message(binary_letters, generator_m, k, n):
    """
    - This function randomly distorts one bit in each given codeword in a
    transmitted message.
    - Returns a list of distorted bit codeword vectors.
    - This simulates noisy channel with that distorts 12.5% of received bits
    randomly.
    """
    disorted_m = [np.matmul(i, generator_m) % 2 for i in binary_letters]

    for letter in disorted_m:
        rand = random.randint(1, n-1)
        letter[rand] = (letter[rand] + 1) % 2

    return disorted_m


def decode_text(text, k, n):
    """
    - Function will develop a ASCII linear code using an 8, n code.
    - Decoding occurs per letter.
    """

    code = AsciiCode(k, n)
    generator_m = code.get_generator_mat()
    stripped_text = text.replace(" ", "")
    binary_text_form = transform_text_to_binary(stripped_text)
    disorted_text = distort_message(binary_text_form, generator_m, k, n)
    decoded_text = ""

    t1 = time.time()
    for letter in disorted_text:
        corrected_letter = code.decode_letter(letter)
        decoded_text = decoded_text + str(corrected_letter)

    t2 = time.time()
    total_time = t2-t1
    return decoded_text, total_time


def get_error_number(message, received):
    """
    - Helper function to compare an original message and received text.
    - Returns number of errors.
    """
    stripped_message = message.replace(" ", "")
    stripped_message = stripped_message.strip()
    errors = 0
    for idx in range(len(received)):
        if stripped_message[idx] != received[idx]:
            errors += 1
    return errors


def single_decoding_simulation(text_length, numTrials, n_start, n_cieling):
    percentage_error = []
    times = []
#    print("Running Error Simulation with ", numTrials, " trials\n")

    for n in range(n_start, n_cieling):
        total_errors = 0
        l = 0
        total_time = 0
        for i in range(numTrials):
            text = randomized_text_generator(text_length)
            l = l + len(text)

            decoded_text, time = decode_text(text, 8, n)
            total_time += time
            errors = get_error_number(text, decoded_text)
            total_errors = total_errors + errors

        avg_time = total_time/numTrials
        l_avg = float(l/numTrials)
        total_mean = float(total_errors/numTrials)
        times.append(avg_time)
        percentage = 100*round(float(total_mean/l_avg), 4)
        percentage_error.append(percentage)

#
#        print("Mean error percentage for 8,", n, " code is ",\
#              str(percentage)+"%" )
#        print("Time Taken: " , time)
    results_array = np.multiply(percentage_error, times)
    return results_array, percentage_error


def stochastic_simulation(word_limit, num_trials, n_start, n_ceiling):

    word_count = []
    count_increase_factor = 10
    table_length = int(word_limit/count_increase_factor)
    text_length = 10
    row_index = 0
    n_values = np.zeros((table_length - 1, (n_ceiling-n_start)), dtype=float)
    percentage_matrix = np.zeros(
        (table_length-1, (n_ceiling - n_start)), dtype=float)

    while(text_length < word_limit):
        text_length = text_length + count_increase_factor
        word_count.append(text_length)
        n_values[row_index, :], percentage_matrix[row_index, :] = single_decoding_simulation(
            text_length, num_trials, n_start, n_ceiling)
        row_index += 1

    return n_values, word_count, percentage_matrix


def visualization(word_limit, num_trials):
    n_start, n_ceiling = 10, 16

    result_matrix, word_count, percentage_matrix = stochastic_simulation(
        word_limit, num_trials, n_start, n_ceiling)

    row_labels = []
    column_labels = ["Avg Error Percentage(%)", "Standard Deviation"]
    table_text = np.zeros((n_ceiling-n_start, 2), dtype=float)

    # Create a figure with two subplots
    fig = pl.figure(figsize=(10, 10))
    gs = fig.add_gridspec(2, 1, height_ratios=[1, 1], hspace=0.3)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])

    # Plot error percentages
    for idx in range(n_start, n_ceiling):
        matrix_index = idx - n_start
        line_label = "8, "+str(idx) + " code"
        row_labels.append(line_label)
        table_text[matrix_index, :] = [np.mean(
            percentage_matrix[:, matrix_index]), np.std(percentage_matrix[:, matrix_index])]

        ax1.plot(word_count, percentage_matrix[:, matrix_index], label=line_label)

    ax1.set_ylabel("Error Percentage (%)")
    ax1.set_xlabel("Text Word Count")
    ax1.set_title("Error Percentage vs Word Count")
    ax1.legend(loc='upper left')
    ax1.grid(True)

    # Plot execution times (convert to milliseconds)
    times = (result_matrix / percentage_matrix) * 1000  # Convert seconds to milliseconds
    for idx in range(n_start, n_ceiling):
        matrix_index = idx - n_start
        line_label = "8, "+str(idx) + " code"
        ax2.plot(word_count, times[:, matrix_index], label=line_label)

    ax2.set_ylabel("Execution Time (ms)")
    ax2.set_xlabel("Text Word Count")
    ax2.set_title("Execution Time vs Word Count")
    ax2.legend(loc='upper left')
    ax2.grid(True)

    pl.tight_layout()
    pl.show()

    # Display statistics table
    table_text = np.around(table_text, 3)
    fig, ax = pl.subplots()
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.table(cellText=table_text,
             rowLabels=row_labels,
             colLabels=column_labels,
             colWidths=[0.3 for x in column_labels],
             loc='center')

    return None

visualization(500, 10)
