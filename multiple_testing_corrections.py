import numpy as np

def bonferroni_correction(p_values, alpha):
    if not p_values:
        return np.array([], dtype=bool)
    m = len(p_values)
    p_values_np = np.asarray(p_values)
    adjusted_alpha = alpha/m
    is_significant = p_values_np <= adjusted_alpha
    return is_significant
