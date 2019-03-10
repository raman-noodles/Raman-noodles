import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import peakutils
import jcamp
from ramannoodles import shoyu
from ramannoodles import spectrafit
import pickle

shoyu.initialize_standard_library()
# open spectra library
shoyu_data_dict = pickle.load(open('../raman_spectra/shoyu_data_dict.p', 'rb'))
# list keys
sorted(shoyu_data_dict.keys())

def h2o():
    data = shoyu_data_dict['WATER']
    x_data = data['x']
    y_data = data['y']

    data_range = max(x_data) - min(x_data)
    data_range
    xmin = data['x'].min()
    xmax = data['x'].max()
    xrange=xmax-xmin
    # subtract baseline
    y_data = spectrafit.subtract_baseline(y_data, deg=3, plot=True, x_data=x_data)
    # detect peaks
    # detect peaks
    peaks = spectrafit.find_peaks(x_data, y_data, thres=0.25, min_dist=50)
    # assign parameters for least squares fit
    mod, pars = spectrafit.lorentz_params(peaks)
    # fit the model to the data
    out = spectrafit.model_fit(x_data, y_data, mod, pars, report=True)
    # plot fit results
    spectrafit.plot_fit(x_data, y_data, out, plot_components=True)
    # export data in logical structure (see docstring)
    fit_peak_data = spectrafit.export_fit_data(out)
    # print docstring which outlines data structure
    spectrafit.export_fit_data.__doc__
    center = [] 
    sigma = [] 
    amps = []
    for i in range(len(fit_peak_data)):
        sigma.append(fit_peak_data[i][0])
        center.append(fit_peak_data[i][1])  
        amps.append(fit_peak_data[i][2])
    return xmin,xmax,sigma,center,amps