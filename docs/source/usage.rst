Usage
=====

.. _installation:

Installation
------------

To use scikit-ferm, first install it using pip:

.. code-block:: console

   (.venv) $ pip install scikit-ferm

Datasets
--------

Scikit-ferm provides a datasets subpackage that includes both real experimental data and tools for generating synthetic datasets. This is useful for testing algorithms, learning how to use the package, and benchmarking different growth models.

Real Datasets
~~~~~~~~~~~~~

The package includes real experimental datasets that you can load and explore:

**Rheolaser Dataset**

The Rheolaser dataset contains elasticity index measurements over time from fermentation experiments. This data comes from a Rheolaser instrument and provides insights into the rheological properties of fermenting cultures.

.. code-block:: python

   from skferm.datasets.rheolaser import load_rheolaser_data

   # Load the raw data as it comes from the instrument
   raw_data = load_rheolaser_data(clean=False)

   # Load cleaned data in long format (recommended)
   clean_data = load_rheolaser_data(clean=True)

   # Load data with a time cutoff (e.g., first 24 hours)
   limited_data = load_rheolaser_data(clean=True, cutoff=24)

   print(clean_data.head())
   # Shows columns: sample_id, time (hours), elasticity_index

The cleaned dataset is in long format with the following columns:
- ``sample_id``: Identifier for each fermentation sample
- ``time``: Time in hours
- ``elasticity_index``: Elasticity measurement (scaled by 1000)

Synthetic Data Generation
~~~~~~~~~~~~~~~~~~~~~~~~~

For testing and experimentation, you can generate synthetic growth data using various mathematical models:

.. code-block:: python

   import numpy as np
   from skferm.datasets.synthetic import generate_synthetic_growth

   # Create time points
   time_points = np.linspace(0, 24, 100)  # 24 hours, 100 data points

   # Generate logistic growth data
   logistic_data = generate_synthetic_growth(
       time=time_points,
       model="logistic",
       K=100,        # carrying capacity
       r=0.1,        # growth rate
       N0=1,         # initial population
       noise_std=2.0 # add some realistic noise
   )

   # Generate Gompertz growth data
   gompertz_data = generate_synthetic_growth(
       time=time_points,
       model="gompertz",
       A=100,        # asymptotic value
       mu=0.5,       # maximum growth rate
       lag=2.0,      # lag time
       noise_std=1.5
   )

   # Generate modified Gompertz growth data
   modified_gompertz_data = generate_synthetic_growth(
       time=time_points,
       model="modified_gompertz",
       A=100,        # asymptotic value
       mu=0.3,       # maximum growth rate
       lag=3.0,      # lag time
       noise_std=1.0
   )

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

Data Cleaning Utilities
~~~~~~~~~~~~~~~~~~~~~~~~

The package also provides utilities for cleaning and preprocessing experimental data:

.. code-block:: python

   from skferm.datasets.rheolaser import clean_rheolaser
   import pandas as pd

   # If you have raw rheolaser data
   raw_df = pd.read_csv('your_rheolaser_export.csv')
   cleaned_df = clean_rheolaser(raw_df, cutoff=48)  # Keep only first 48 hours

The ``clean_rheolaser`` function transforms the wide format output from Rheolaser instruments into a tidy long format suitable for analysis and visualization.

Curve Smoothing
----------------

Scikit-ferm includes a curve smoothing utility to help with noisy fermentation data. This is particularly useful for visualizing trends in growth curves.

Growth Models
----------------

Scikit-ferm provides implementations of several growth models commonly used in fermentation analysis:
