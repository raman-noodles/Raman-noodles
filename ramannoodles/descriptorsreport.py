import matplotlib.pyplot as plt
import pickle
from ramannoodles import spectrafit




def compound_report(compound):
    # open spectra library
    shoyu_data_dict = pickle.load(open('../raman_spectra/shoyu_data_dict.p', 'rb'))
    # extract data from spectra library
    data = shoyu_data_dict[compound]
    x_data = data['x']
    y_data = data['y']
    xmin = min(x_data)
    xmax = max(x_data)
    xrange=xmax-xmin
    # subtract baseline
    y_data = spectrafit.subtract_baseline(y_data)
    # detect peaks
    peaks, peak_list = spectrafit.peak_detect(x_data, y_data)
    # assign parameters for least squares fit
    mod, pars = spectrafit.lorentz_params(peaks)
    # fit the model to the data
    out = spectrafit.model_fit(x_data, y_data, mod, pars)
    # export data in logical structure (see docstring)
    fit_peak_data = spectrafit.export_fit_data(out)
    peak_centers = [] 
    peak_sigma = [] 
    peak_ampl = []
    for i in range(len(fit_peak_data)):
        peak_sigma.append(fit_peak_data[i][0])
        peak_centers.append(fit_peak_data[i][1])
        peak_ampl.append(fit_peak_data[i][2])
    return xmin,xmax,peak_centers,peak_sigma,peak_ampl

def data_report(x_data, y_data):
    xmin = min(x_data)
    xmax = max(x_data)
    xrange=xmax-xmin
    # subtract baseline
    y_data = spectrafit.subtract_baseline(y_data)
    # detect peaks
    peaks, peak_list = spectrafit.peak_detect(x_data, y_data)
    # assign parameters for least squares fit
    mod, pars = spectrafit.lorentz_params(peaks)
    # fit the model to the data
    out = spectrafit.model_fit(x_data, y_data, mod, pars)
    # export data in logical structure (see docstring)
    fit_peak_data = spectrafit.export_fit_data(out)
    peak_centers = [] 
    peak_sigma = [] 
    peak_ampl = []
    for i in range(len(fit_peak_data)):
        peak_sigma.append(fit_peak_data[i][0])
        peak_centers.append(fit_peak_data[i][1])
        peak_ampl.append(fit_peak_data[i][2])
    return xmin,xmax,peak_centers,peak_sigma,peak_ampl