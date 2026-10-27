# currently with normal distribution approximation

import numpy as np

def welch_standard_error(values_a, values_b):
	if len(values_a) < 2 or len(values_b) < 2:
		raise ValueError("Sample has less than 2 observations.")

	values_a_np = np.asarray(values_a, dtype=float)
	values_b_np = np.asarray(values_b, dtype=float)

	n_a = len(values_a)
	n_b = len(values_b)

	a_average = np.average(values_a_np)
	b_average = np.average(values_b_np)

	s_a = 1/(n_a-1) * np.sum(np.square(values_a_np - a_average))
	s_b = 1/(n_b-1) * np.sum(np.square(values_b_np - b_average))


	SE = np.sqrt((s_a / n_a) + (s_b / n_b))

	return SE

