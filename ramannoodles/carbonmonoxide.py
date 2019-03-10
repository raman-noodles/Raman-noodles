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
# import data dict
shoyu_data_dict = pickle.load(open('../raman_spectra/shoyu_data_dict.p', 'rb'))

def CarbonMonoxide():
    data = shoyu_data_dict['CARBON MONOXIDE']
    x_data = data['x']
    y_data = data['y']
    xmin = data['x'].min()
    xmax = data['x'].max()
    xrange=xmax-xmin
    # # subtract baseline
    # y_data = spectrafit.subtract_baseline(y_data, deg=3, plot=True, x_data=x_data)
    #print(xmin,xmax,xrange)
    # detect peaks
    peaks = spectrafit.find_peaks(x_data, y_data)
    # assign parameters for least squares fit
    mod, pars = spectrafit.lorentz_params(peaks)
    # fit the model to the data
    out = spectrafit.model_fit(x_data, y_data, mod, pars, report=True)
    # plot fit results
    plot = spectrafit.plot_fit(x_data, y_data, out, plot_components=True)
    # export data in logical structure (see docstring)
    fit_peak_data = spectrafit.export_fit_data(out)
    # print docstring which outlines data structure
    spectrafit.export_fit_data.__doc__
    for i in range(len(fit_peak_data)):
        sigma = fit_peak_data[i][0]  
        center = fit_peak_data[i][1]    
        amplitude = fit_peak_data[i][2] 
    return xmin,xmax,sigma,center,amplitude