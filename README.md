# AB_testing_-_causal_inference_toolkit


## Normal distribution primitives
### standard_normal_cdf
Here we use math.erf function, that returns:
\operatorname{erf}(x) = \frac{2}{\sqrt{\pi}} \int_{0}^{x} e^{-t^2} \, dt
We want it to on both Python floats and on numpy arrays, so we vectorize math.erf function with np.vectorize.
Alternatively, we could have used scipy.
