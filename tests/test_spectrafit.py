"""
This is the unit test module for spectrafit.py
"""

import numpy as np
import spectrafit


# define gaussian function used to generate test data (fake spectra)
def gaussian(x_input, var_a, var_b, var_c):
    """Simple function to produce a gaussian distribution"""
    y_output = var_a*np.exp(-((x_input-var_b)**2)/(2*(var_c**2)))
    return y_output


# generate test data
X_TEST = np.arange(500, 3500, 5)
# generate 6 gaussians
gauss1 = gaussian(X_TEST, 0.9, 2000, 100)
gauss2 = gaussian(X_TEST, 0.5, 1000, 200)
gauss3 = gaussian(X_TEST, 0.4, 2500, 1000)
gauss4 = gaussian(X_TEST, 0.7, 3200, 50)
gauss5 = gaussian(X_TEST, 0.7, 2200, 20)
gauss6 = gaussian(X_TEST, 0.7, 4000, 500)
# add gaussians to create fake spectra
Y_TEST = gauss1 + gauss2 + gauss3 + gauss4 + gauss5 + gauss6
# normalize test spectra
Y_TEST = [(Y_TEST[i] - min(Y_TEST))/(max(Y_TEST)-min(Y_TEST)) for i in range(len(Y_TEST))]
Y_TEST = np.asarray(Y_TEST)


def test_subtract_baseline():
    """docstring"""
    y_data = spectrafit.subtract_baseline(Y_TEST)
    assert isinstance(y_data, np.ndarray), 'output is not a numpy array'
    assert len(y_data) == len(Y_TEST), 'output length different from input'
