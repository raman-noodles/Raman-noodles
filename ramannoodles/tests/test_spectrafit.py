"""
This is the unit test module for spectrafit.py
"""

import pickle
import numpy as np
import lmfit
from ramannoodles import spectrafit


# define gaussian function used to generate test data (fake spectra)
def gaussian(x_input, var_a, var_b, var_c):
    """Simple function to produce a gaussian distribution"""
    y_output = var_a*np.exp(-((x_input-var_b)**2)/(2*(var_c**2)))
    return y_output


# generate test data
X_TEST = np.arange(500, 3500, 5)
# generate 6 gaussians
GAUSS1 = gaussian(X_TEST, 0.9, 2000, 100)
GAUSS2 = gaussian(X_TEST, 0.5, 1000, 200)
GAUSS3 = gaussian(X_TEST, 0.4, 2500, 1000)
GAUSS4 = gaussian(X_TEST, 0.7, 3200, 50)
GAUSS5 = gaussian(X_TEST, 0.7, 2200, 20)
GAUSS6 = gaussian(X_TEST, 0.7, 4000, 500)
# add gaussians to create fake spectra
Y_TEST = GAUSS1 + GAUSS2 + GAUSS3 + GAUSS4 + GAUSS5 + GAUSS6
# normalize test spectra
Y_TEST = [(Y_TEST[i] - min(Y_TEST))/(max(Y_TEST)-min(Y_TEST)) for i in range(len(Y_TEST))]
Y_TEST = np.asarray(Y_TEST)

# open spectra library
SHOYU_DATA_DICT = pickle.load(open('raman_spectra/shoyu_data_dict.p', 'rb'))


def test_subtract_baseline():
    """docstring"""
    y_data = spectrafit.subtract_baseline(Y_TEST)
    assert isinstance(y_data, np.ndarray), 'output is not a numpy array'
    assert len(y_data) == len(Y_TEST), 'output length different from input'


def test_peak_detect():
    """docstring"""
    y_test = spectrafit.subtract_baseline(Y_TEST)
    peaks, peak_list = spectrafit.peak_detect(X_TEST, y_test)
    assert isinstance(peaks, list), 'expected output is list'
    assert isinstance(peaks[0], tuple), 'first peak data is not a tuple'
    assert min(X_TEST) <= peaks[0][0] <= max(X_TEST), '1st peak center is outside data range'
    assert 0 <= peaks[0][1] <= 1, '1st peak maximum is outside acceptable range'
    assert len(peaks) == len(peak_list), 'Number of peak indeces different than number of peak data'


def test_lorentz_params():
    """docstring"""
    y_test = spectrafit.subtract_baseline(Y_TEST)
    peaks = spectrafit.peak_detect(X_TEST, y_test)[0]
    mod, pars = spectrafit.lorentz_params(peaks)
    assert isinstance(mod, lmfit.model.CompositeModel), 'mod is not a lmfit CompositeModel'
    assert isinstance(pars, lmfit.parameter.Parameters), 'pars are not lmfit Parameters'
    assert len(pars) == 5*len(peaks), 'incorrect ratio of parameters to peaks'


def test_model_fit():
    """docstring"""
    y_test = spectrafit.subtract_baseline(Y_TEST)
    peaks = spectrafit.peak_detect(X_TEST, y_test)[0]
    mod, pars = spectrafit.lorentz_params(peaks)
    out = spectrafit.model_fit(X_TEST, y_test, mod, pars)
    assert isinstance(out, lmfit.model.ModelResult), 'output is not a lmfit ModelResult'
    assert len(out.best_fit) == len(y_test), 'size of fit incorrect'
    assert isinstance(out.best_values, dict), 'out.best_values is not a dictionary'
    assert len(out.values) == len(pars), 'number of output values not equal to number of parameters'


# need a unit test for plot_fit function


def test_export_fit_data():
    """docstring"""
    y_test = spectrafit.subtract_baseline(Y_TEST)
    peaks = spectrafit.peak_detect(X_TEST, y_test)[0]
    mod, pars = spectrafit.lorentz_params(peaks)
    out = spectrafit.model_fit(X_TEST, y_test, mod, pars)
    fit_peak_data = spectrafit.export_fit_data(out)
    assert isinstance(fit_peak_data, list), 'output is not a list'
    assert np.asarray(fit_peak_data).shape == (int(len(out.values)/5), 5), """
    output is not the correct shape"""
    assert len(fit_peak_data) == int(len(out.values)/5), 'incorrect number of peaks exported'


def test_compound_report():
    """docstring"""
    compound = SHOYU_DATA_DICT['WATER']
    data = spectrafit.compound_report(compound)
    assert len(data) == 5, 'more values in return than expected'
    assert len(data[0]) == 3, 'more than three peaks detected for WATER'
