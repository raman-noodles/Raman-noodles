"""
This module allows for baseline subtraction, peak detection, and
lorentzian/gaussian fitting of spectra data.
"""


import matplotlib.pyplot as plt
import numpy as np
import peakutils
import lmfit
from lmfit.models import LorentzianModel
from peakutils.baseline import baseline


def subtract_baseline(y_data, deg=3, plot=False, x_data=None):
    """
    Function that fits a n-degree polynomial (default: n=5)
    baseline and subtracts it from the input data
    """
    y_base = baseline(y_data, deg=deg, max_it=200)
    # to avoid strange results,
    # change all negative values to zero
    yb_plus = [0 if i < 0 else i for i in y_base]
    y_out = y_data - yb_plus
    # plot that lets you see the baseline fitting
    if plot and x_data is None:
        print('Please add x_data as input to plot')
    elif plot:
        plt.figure(figsize=(10,4))
        plt.plot(x_data, y_data, 'b--', label='input')
        plt.plot(x_data, y_out, 'b', label='output')
        plt.plot(x_data, yb_plus, 'r', label='baseline')
        plt.plot(x_data, y_base, 'r--', label='negative baseline')
        plt.axhline(y=0, color='orange', alpha=0.5, label='zero') 
        plt.legend()
    else:
        pass
    return y_out


def find_peaks(x_data, y_data, thres=0.25, min_dist=10):
    """docstring"""
    # find peaks
    indexes = peakutils.indexes(y_data, thres=thres, min_dist=min_dist)
    # convert peak indexes to data values
    peaks = []
    for i in indexes:
        peak = (x_data[i], y_data[i])
        peaks.append(peak)
    peaks
    return peaks


def lorentz_params(peaks):
    peak_list = []
    for i in range(len(peaks)):
        prefix = 'p{}_'.format(i+1)
        peak = LorentzianModel(prefix=prefix)
        if i == 0:
            pars = peak.make_params()
        else:
            pars.update(peak.make_params())
        pars[prefix+'center'].set(peaks[i][0], vary=True, min=(peaks[i][0]-10), max=(peaks[i][0]+10))
        pars[prefix+'height'].set(peaks[i][1], vary=True, min=0, max=1)
        pars[prefix+'sigma'].set(min=0, max=500)
        pars[prefix+'amplitude'].set(min=0)
        peak_list.append(peak)
        if i == 0:
            mod = peak_list[i]
        else:
            mod = mod + peak_list[i]
    return mod, pars


def model_fit(x_data, y_data, mod, pars, report=False):
    # fit model
    init = mod.eval(pars, x=x_data)
    out = mod.fit(y_data, pars, x=x_data)
    if report:
        print(out.fit_report())
    else:
        pass
    return out


def plot_fit(x_data, y_data, fit_result, plot_components=False):
    fig = plt.figure(figsize=(15,6))
    plt.ylabel('Absorbance', fontsize=14)
    plt.xlabel('Wavenumber (cm$^{-1}$)', fontsize=14)
    plt.xlim(min(x_data), max(x_data))
    plt.ylim(min(y_data)*-0.9, max(y_data)*1.1)
    plt.plot(x_data, y_data, 'r', alpha=1, linewidth=2, label='data')
    plt.plot(x_data, fit_result.best_fit, 'c-', alpha=0.5, linewidth=3, label='fit')
    if plot_components:
        comps = fit_result.eval_components(x=x_data)
        prefix = 'p{}_'.format(1)
        plt.plot(x_data, comps[prefix], 'b--', linewidth=1, label='peak lorentzians')
        for i in range(1, int(len(fit_result.values)/5)):
            prefix = 'p{}_'.format(i+1)
            plt.plot(x_data, comps[prefix], 'b--', linewidth=1)
    plt.legend(fontsize=12)
    plt.show()


def export_fit_data(out):
    """
    fit_peak_data[i][0] = p[i]_simga
    fit_peak_data[i][1] = p[i]_center
    fit_peak_data[i][2] = p[i]_amplitude
    fit_peak_data[i][3] = p[i]_fwhm
    fit_peak_data[i][4] = p[i]_center
    """
    fit_peak_data = []
    for i in range(int(len(out.values)/5)):
        peak = np.zeros(5)
        prefix = 'p{}_'.format(i+1)
        peak[0] = out.values[prefix+'sigma']
        peak[1] = out.values[prefix+'center']
        peak[2] = out.values[prefix+'amplitude']
        peak[3] = out.values[prefix+'fwhm']
        peak[4] = out.values[prefix+'center']
        fit_peak_data.append(peak)
    return fit_peak_data
