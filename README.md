# AB_testing_-_causal_inference_toolkit


## Normal distribution primitives
### standard_normal_cdf
This function returns the probability that a standard normal random variable is less than or equal to z.
Here we use math.erf function, that returns: <br>
$\mathrm{erf}(x) = \frac{2}{\sqrt{\pi}} \int_{0}^{x} e^{-t^2} \, dt$ <br>
We want it to work on both Python floats and on numpy arrays, so we vectorize math.erf function with np.vectorize.
Alternatively, we could have used scipy.
