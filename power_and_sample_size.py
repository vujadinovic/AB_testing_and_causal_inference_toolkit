import math
from normal_dist import standard_normal_ppf

def required_sample_size_per_variant(baseline_rate, minimum_detectable_effect, alpha, power):
    treatment_rate = baseline_rate + minimum_detectable_effect
    p_hat = (baseline_rate + treatment_rate) / 2
    z_alpha = standard_normal_ppf(1 - alpha / 2)
    z_power = standard_normal_ppf(power)
    formula = ((z_alpha * math.sqrt(2 * p_hat * (1 - p_hat))) + (z_power * math.sqrt(baseline_rate * (1 - baseline_rate) + treatment_rate * (1- treatment_rate))))**2/minimum_detectable_effect**2
    return math.ceil(formula)
