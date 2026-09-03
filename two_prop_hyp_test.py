def pooled_proportion(successes_a, total_a, successes_b, total_b):
    return (successes_a + successes_b) / (total_a + total_b)


    
def pooled_standard_error(pooled_p, total_a, total_b):
    return math.sqrt(pooled_p*(1-pooled_p)* (1/total_a + 1/total_b))
