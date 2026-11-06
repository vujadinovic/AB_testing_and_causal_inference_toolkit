# A/B Testing and Causal Inference Toolkit

An experimentation toolkit written from scratch in Python and NumPy. It covers the full path of an experiment: planning the sample size, checking that the randomization worked, testing the result, correcting for many tests, and deciding whether to ship. For settings where randomization is not possible, it adds two quasi-experimental estimators: difference-in-differences and synthetic control.

The idea is to understand each method by building it, not by calling a library. For this reason, everything rests on two small primitives: the CDF of the standard normal distribution and its inverse.

| File | What it does |
|---|---|
| `normal_dist.py` | Standard normal CDF and its inverse (PPF) |
| `two_prop_hyp_test.py` | z-test for the difference of two proportions, plus confidence intervals |
| `welch_test.py` | Test for the difference of two means with unequal variances |
| `power_and_sample_size.py` | Sample size per variant and statistical power |
| `srm_diagnostics.py` | Sample ratio mismatch check |
| `multiple_testing_corrections.py` | Bonferroni and Benjamini–Hochberg corrections |
| `ship_decision.py` | Ship/no-ship rule from a primary metric and guardrails |
| `diff_in_diff.py` | Difference-in-differences, directly and through OLS |
| `synthetic_control.py` | Synthetic control weights and treatment effect |

## Normal distribution primitives
### standard_normal_cdf
This function returns the probability that a standard normal random variable is less than or equal to z.
Here we use math.erf function, that returns: <br>
$\mathrm{erf}(x) = \frac{2}{\sqrt{\pi}} \int_{0}^{x} e^{-t^2} \, dt$ <br>
We want it to work on both Python floats and on numpy arrays, so we vectorize math.erf function with np.vectorize.
Alternatively, we could have used scipy.

### standard_normal_ppf
Inverse of standard normal cumulative density function.
There is no closed form solution for this function, so we will have to numerically approximate it.
We can go about it in two ways: Acklam and Wichura algorithms.  <br>
Wichura is the industry standard, but we go with Acklam for the simplicity with the idea to upgrade to Wichura later.
TBF: As of now, this is a copy-paste implementation on my side.

## Two proportion hypothesis testing
For two groups with observed success rates $`p_A`$ and $`p_B`$, the null hypothesis is $`p_A = p_B`$. Under the null, the difference $`\hat{p}_B - \hat{p}_A`$ is approximately normal with mean $`0`$ and standard deviation equal to the pooled standard error

```math
SE_{\text{pool}} = \sqrt{\hat{p}(1-\hat{p})\left(\frac{1}{n_A} + \frac{1}{n_B}\right)},
```

where $`\hat{p}`$ is the success rate of both groups taken together. The test statistic is

```math
z = \frac{\hat{p}_B - \hat{p}_A}{SE_{\text{pool}}}.
```

A positive $`z`$ means group B outperformed group A, and a negative $`z`$ means the reverse. Values with $`|z| > 1.96`$ correspond to a two-sided p-value below $`0.05`$.

For the confidence interval the null no longer holds, so the unpooled standard error is used instead. The interval is $`\hat{\delta} \pm z_{1-\alpha/2} \cdot SE`$.

## Welch test
The same idea, but for continuous metrics such as revenue per user. The two groups may have different variances, so each one keeps its own:

```math
SE = \sqrt{\frac{s_A^2}{n_A} + \frac{s_B^2}{n_B}}.
```

The function returns the effect, the standard error, $`z`$, the p-value and the confidence interval. For now the normal approximation is used instead of the Student $`t`$ distribution, which is accurate for large samples.

## Power and sample size
Before the experiment we ask: how many users are needed to detect an effect of a given size? For a baseline rate $`p_1`$, a minimum detectable effect $`\delta`$ and $`p_2 = p_1 + \delta`$, the required size per variant is

```math
n = \frac{\left(z_{1-\alpha/2}\sqrt{2\bar{p}(1-\bar{p})} + z_{1-\beta}\sqrt{p_1(1-p_1) + p_2(1-p_2)}\right)^2}{\delta^2}, \qquad \bar{p} = \frac{p_1 + p_2}{2}.
```

The second function answers the opposite question: for a fixed $`n`$, what is the probability that the test detects the effect?

## Sample ratio mismatch diagnostics
If users were meant to be split 50/50 and the observed split is noticeably different, something is wrong with the assignment, and the results cannot be trusted. Microsoft (and LinkedIn) say that around 6% (10%) of A/B tests have SRM (https://www.microsoft.com/en-us/research/articles/diagnosing-sample-ratio-mismatch-in-a-b-testing/).

The check is a chi-square goodness-of-fit test:

```math
\chi^2 = \sum_i \frac{(O_i - E_i)^2}{E_i}.
```

The p-value uses the fact that, with one degree of freedom, $`\chi^2 = Z^2`$, so it is computed from the normal CDF. This is exact for two variants.

## Multiple testing corrections
When we test many metrics at once, some of them will look significant by chance alone. Two corrections are implemented:

- **Bonferroni** compares every p-value to $`\alpha / m`$. It controls the probability of even one false positive, but it is conservative.
- **Benjamini–Hochberg** sorts the p-values and finds the largest $`k`$ such that $`p_{(k)} \le \frac{k}{m}\alpha`$. All hypotheses up to $`k`$ are rejected. It controls the false discovery rate and keeps more power.

## Ship decision
A simple rule that turns test results into a decision. The change is shipped only if:

1. the primary metric is significant,
2. its effect is positive,
3. no guardrail metric is significantly harmed. For each guardrail we say which direction counts as harm (for example, an increase in latency).

The function returns the decision and the reason for it.

## Difference-in-differences
When we cannot randomize, we compare how the outcome changed in the treated group with how it changed in a control group:

```math
\hat{\tau} = (\bar{y}_{T,\text{post}} - \bar{y}_{T,\text{pre}}) - (\bar{y}_{C,\text{post}} - \bar{y}_{C,\text{pre}}).
```

The same estimate is obtained from the regression

```math
y = \beta_0 + \beta_1 \cdot \text{treated} + \beta_2 \cdot \text{post} + \beta_3 \cdot (\text{treated} \times \text{post}) + \varepsilon,
```

where $`\beta_3`$ is the effect. Both versions are implemented, which makes it easy to check that they agree. The key assumption is parallel trends: without the treatment, both groups would have changed in the same way.

## Synthetic control
When there is only one treated unit (a city, a country), there is often no single good control. Instead, we build one as a weighted combination of untreated "donor" units that best follows the treated unit before the treatment:

```math
\min_{w} \|X w - y\|^2, \qquad w_j \ge 0, \quad \sum_j w_j = 1.
```

The constraints are satisfied by writing the weights as a softmax, $`w = \mathrm{softmax}(\theta)`$, and optimizing $`\theta`$ with gradient descent. After the treatment, the effect is the gap between the treated unit and its synthetic version, averaged over the post period.



### standard_normal_ppf
Inverse of standard normal cumulative density function.
There is no closed form solution for this function, so we will have to numerically approximate it.
We can go about it in two ways: Acklam and Wichura algorithms.  <br>
Wichura is the industry standard, but we go with Acklam for the simplicity with the idea to upgrade to Wichura later.
TBF: As of now, this is a copy-paste implementation on my side.



## Two proportion hypothesis testing
For two groups with observed success rates $p\_A$ and $p\_B$, the null hypothesis is $p\_A = p\_B$. Under that null, the sampling distribution of the difference $\hat{p}\_B - \hat{p}\_A$ is approximately normal with mean $0$ and standard deviation equal to the pooled standard error $SE\_{\text{pool}}$.

The standardized test statistic is:

$$z = \frac{\hat{p}_B - \hat{p}_A}{SE_{\text{pool}}}$$

A positive $z$ means group B outperformed group A; a negative $z$ means the reverse. Values with $|z| > 1.96$ correspond to a two-sided p-value below $0.05$.


## Sample ratio mismatch diagnostics
Microsoft (and LinkedIn) say that around 6% (10%) of A/B tests have SRM (https://www.microsoft.com/en-us/research/articles/diagnosing-sample-ratio-mismatch-in-a-b-testing/).
