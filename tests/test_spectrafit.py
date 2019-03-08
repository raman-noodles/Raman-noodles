"""
This is the unit test module for spectrafit.py
"""

import numpy as np
import lmfit
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


def test_find_peaks():
    """docstring"""
    peaks = spectrafit.find_peaks(X_TEST, Y_TEST)
    assert isinstance(peaks, list), 'expected output is list'
    assert isinstance(peaks[0], tuple), 'first peak data is not a tuple'
    assert min(X_TEST) <= peaks[0][0] <= max(X_TEST), '1st peak center is outside data range'
    assert 0 <= peaks[0][1] <= 1, '1st peak maximum is outside acceptable range'


def test_lorentz_params():
    peaks = spectrafit.find_peaks(X_TEST, Y_TEST)
    mod, pars = spectrafit.lorentz_params(peaks)
    assert isinstance (mod, lmfit.model.CompositeModel), 'mod is not a lmfit CompositeModel'
    assert isinstance (pars, lmfit.parameter.Parameters), 'pars are not lmfit Parameters'
    assert len(pars) == 5*len(peaks), 'incorrect ratio of parameters to peaks'


def test_model_fit():
    peaks = spectrafit.find_peaks(X_TEST, Y_TEST)
    mod, pars = spectrafit.lorentz_params(peaks)
    out = spectrafit.model_fit(X_TEST, Y_TEST, mod, pars)
    assert isinstance(out, lmfit.model.ModelResult), 'output is not a lmfit ModelResult'
    assert len(out.best_fit) == len (Y_TEST), 'size of fit incorrect'
    assert isinstance(out.best_values, dict), 'out.best_values is not a dictionary'
    assert len(out.values) == len(pars), 'number of output values not equal to number of parameters'
