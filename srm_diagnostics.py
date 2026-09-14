import numpy as np

def chi_square_statistic(observed_counts, expected_counts):
    np_observed_counts = np.asarray(observed_counts, dtype = float)
    np_expected_counts = np.asarray(expected_counts, dtype = float)
    np_difference = np_observed_counts - np_expected_counts
    return float(np.dot(np_difference, np_difference / np_expected_counts) )