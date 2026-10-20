import numpy as np

def group_mean_change(pre_outcomes, post_outcomes):
    np_pre = np.asarray(pre_outcomes)
    np_post = np.asarray(post_outcomes)
    pre_average = np.mean(np_pre)
    post_average = np.mean(np_post)
    return post_average - pre_average 

def difference_in_differences_simple(treated_pre, treated_post, control_pre, control_post):
    treated_change = group_mean_change(treated_pre, treated_post)
    control_change = group_mean_change(control_pre, control_post)
    return treated_change - control_change