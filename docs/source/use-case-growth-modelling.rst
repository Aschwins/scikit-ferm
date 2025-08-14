Growth Modeling
---------------

Scikit-ferm provides a datasets subpackage that includes some growth models that can be used.

**Available Growth Models:**

- ``"logistic"``: Classic logistic growth model
- ``"gompertz"``: Gompertz growth model
- ``"modified_gompertz"``: Modified Gompertz growth model

**Parameters:**

- ``time``: Array-like time points where you want to generate data
- ``model``: String specifying which growth model to use
- ``noise_std``: Standard deviation of Gaussian noise to add (default: 0.0 for noiseless data)
- ``**kwargs``: Model-specific parameters (K, r, N0 for logistic; A, mu, lag for Gompertz models)

**Returns:**

The function returns a dictionary with:
- ``"time"``: The input time array
- ``"population"``: The generated population values (with noise if specified)

This makes it easy to create realistic synthetic datasets for testing your fermentation analysis pipelines or comparing different growth models.
