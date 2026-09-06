import math
from normal_dist import standard_normal_cdf

def pooled_proportion(successes_a, total_a, successes_b, total_b):
    return (successes_a + successes_b) / (total_a + total_b)

def pooled_standard_error(pooled_p, total_a, total_b):
    return math.sqrt(pooled_p*(1-pooled_p)* (1/total_a + 1/total_b))

def two_proportion_z_statistic(p_a, p_b, pooled_se):
    return (p_b - p_a) / (pooled_se)

def two_sided_p_value(z):
    return 2.0*(1.0-standard_normal_cdf(abs(z)))