# AB_testing_-_causal_inference_toolkit


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
For two groups with observed success rates $p\_A$ and $p\_B$, the null hypothesis is $p\_A = p\_B$. Under that null, the sampling distribution of the difference $\hat{p}\_B - \hat{p}\_A$ is approximately normal with mean $0$ and standard deviation equal to the pooled standard error $SE\_{\text{pool}}$.

The standardized test statistic is:

$$z = \frac{\hat{p}_B - \hat{p}_A}{SE_{\text{pool}}}$$

A positive $z$ means group B outperformed group A; a negative $z$ means the reverse. Values with $|z| > 1.96$ correspond to a two-sided p-value below $0.05$.
