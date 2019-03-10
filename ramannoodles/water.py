import matplotlib.pyplot as plt
import pickle
from ramannoodles import spectrafit


def water():
    # open spectra library
    shoyu_data_dict = pickle.load(open('../raman_spectra/shoyu_data_dict.p', 'rb'))

    # extract spectra data
    data = shoyu_data_dict['WATER']
    x_data = data['x']
    y_data = data['y']

    # detect peaks
    peaks = spectrafit.find_peaks(x_data, y_data, thres=0.25, min_dist=50)

    # assign parameters for least squares fit
    mod, pars = spectrafit.lorentz_params(peaks)

    # fit the model to the data
    out = spectrafit.model_fit(x_data, y_data, mod, pars)

    # export data in logical structure (see docstring)
    fit_peak_data = spectrafit.export_fit_data(out)

    minimum = min(x_data)
    maximum = max(x_data)
    
    peak_loc = peak_loc = []
    peak_sigma = []
    peak_ampl = []
    for i in range(len(fit_peak_data)):
        loc = fit_peak_data[i][1]
        sigma = fit_peak_data[i][0]
        ampl = fit_peak_data[i][2]
        peak_loc.append(loc)
        peak_sigma.append(sigma)
        peak_ampl.append(ampl)

    return minimum, maximum, peak_sigma, peak_loc, peak_ampl
