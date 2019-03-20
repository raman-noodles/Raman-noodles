"""
This module allows for baseline subtraction using polynomial subtraction at a user-specified
degree, peak detection using scipy.signal find_peaks module, and then utilizes 
Lorentzian fitting of spectra data, enabling extraction of full-width, half-max peak data.
Note that Lorentzian fitting was chosen explicitly as it is the proper descriptor of peak
shapes from Raman spectra. 

Developed by the Raman-Noodles team.
"""


import matplotlib.pyplot as plt
import numpy as np
import lmfit
from lmfit.models import LorentzianModel
from peakutils.baseline import baseline
from scipy.signal import find_peaks


def subtract_baseline(y_data, deg=3, plot=False, x_data=None):
    """
    Function that fits an n-degree polynomial (default: n = 3) baseline to the spectral data,
    and subtracts it from the input data.

    	Function Input Parameters:
		y_data - numpy array
			The intensity data of the spectra to be baselined. 
		deg - integer (Optional)
			Integer value for the degree of the polynomial to be used to baseline data.
			The value defaults to 3 if no value is specified.
		plot - Boolean (Optional)
			Boolean value that indicates whether or not to plot the baselined and 
			original data. If true, it plots both spectra on the same plot. Note that 
			if the user wants plotting functionality, x_data must be provided.
		x_data - numpy array (Optional)
			The x-values associated with the y_data that is being baselined. 
			These values are only needed for the function if the user desires plotting.

	Function Return Parameters:
		y_out - numpy array
			The baselined values of the y-axis. 
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


def peak_detect(x_data, y_data, height=0.1, prominence=0.1, distance=10):
    """
    Function that utilizes scipy to find peak maxima from input spectral data. Default 
    detection parameters are chosen for the user based upon values that worked well during
    initial testing of the function; however, the option remains to adjust the parameters
    to achieve the best fit, if the user so chooses.
    WARNING: This function may return unexpected results or unreliable results for data 
    that contains NaNs. Please remove any NaN values prior to passing data. 

	Function Input Parameters:
		x_data - numpy array
			The x-values of the spectra from which peaks will be detected.
		y_data - numpy array
			The y-values of the spectra from which peaks will be detected.
		height - float (Optional)
			The minimum floor of peak-height below which all peaks will be ignored. Any 
			peak that is detected that has a maximum height less than `height` will not 
			be collected. NOTE: This value is highly sensitive to baselining, so the 
			Raman-noodles team recommends ensuring a quality baseline before use.
		prominence - float (Optional)
			The prominence of the peak. In short, it's a comparison of the height of a 
			peak relative to adjacent peaks that considers both the height of the adjacent
			peaks, as well as their distance from the peak being considered. More details 
			can be found in the `peak_prominences` module from scipy. 
		distance - float (Optional)
			The minimum distance between adjacent peaks. 
	Function Returns:
		peaks - list
			A list of the x and y-values where peaks were detected.
		peak_list - numpy array
			An array of the indices of the fed-in data that correspond to the detected 
			peaks.

    """
    # find peaks
    peak_list = find_peaks(y_data, height=height, prominence=prominence, distance=distance)
    # convert peak indexes to data values
    peaks = []
    for i in peak_list[0]:
        peak = (x_data[i], y_data[i])
        peaks.append(peak)
    peaks
    return peaks, peak_list


def lorentz_params(peaks):
    """
    This module takes in the list of peaks from the peak detection modules, and then uses that to initialize
    parameters for a set of Lorentzian models that are not yet fit. There is a single model for every peak.

	Function Input Parameters:
		peaks - list
			A list containing the x and y-values of the peaks
	Function Returns:
		mod - lmfit.model.CompositeModel
			This is an array of the initialized lorentzian models. The array contains all of the
			values that are found in `pars` that are fed to an lmfit lorentzian model class.
		pars - lmfit.parameter.Parameters
                        An array containing the parameters for each peak that were generated through the
                        use of a Lorentzian fit. The pars array contains a center value, a height, a
                        sigma, and an amplitude value. The center value is allowed to vary +- 10 wavenumber
                        from the peak max that was detected in scipy. Some wiggle room was allowed to help
                        mitigate problems from slight issues in the peakdetect algorithm for peaks that might
                        have relatively flat maxima. The height value was allowed to vary between 0 and 1, as
                        it is assumed the y-values are normalized. Sigma is set to a maximum of 500, as we
                        found that giving it an unbound maximum led to a number of peaks that were unrealistic
                        for Raman spectra (ie, they were far too broad, and shallow, to correspond to real data.
                        Finally, the amplitude for the peak was set to a minimum of 0, to prevent negatives.
    """
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
    """
    This function takes in the x and y data for the spectrum being analyzed, as well as the model 
    parameters that were generated in `lorentz_params` for a single peak, and uses it to generate 
    a fit for the model at that one single peak position, then returns that fit. 

	Function Input Parameters:
		x_data - numpy array
			The x-values for the spectrum that is being fit.
		y_data - numpy array
			The y-values for the spectrum that is being fit.
		mod - lmfit.model.CompositeModel
			This is an array of the initialized Lorentzian models from the `lorentz_params` 
			function. This array contains all of the values that are found in pars, that are
			fed to an lmfit Lorentzian model class. 
		pars - lmfit.parameter.Parameters
                        An array containing the parameters for each peak that were generated through the
                        use of a Lorentzian fit. The pars array contains a center value, a height, a
                        sigma, and an amplitude value. The center value is allowed to vary +- 10 wavenumber
                        from the peak max that was detected in scipy. Some wiggle room was allowed to help
                        mitigate problems from slight issues in the peakdetect algorithm for peaks that might
                        have relatively flat maxima. The height value was allowed to vary between 0 and 1, as
                        it is assumed the y-values are normalized. Sigma is set to a maximum of 500, as we
                        found that giving it an unbound maximum led to a number of peaks that were unrealistic
                        for Raman spectra (ie, they were far too broad, and shallow, to correspond to real data.
                        Finally, the amplitude for the peak was set to a minimum of 0, to prevent negatives.
		report - Boolean (Optional)
			This value details whether or not the users wants to receive a report of the fit values.
			If True, the function will print a report of the fit.
	Function Returns:
		out - lmfit.model.ModelResult 
			An lmfit model class that contains all of the fitted values for the input model.
    """
    # fit model
    init = mod.eval(pars, x=x_data)
    out = mod.fit(y_data, pars, x=x_data)
    if report:
        print(out.fit_report())
    else:
        pass
    return out


def plot_fit(x_data, y_data, fit_result, plot_components=False):
    """
    This function fits all of the models previously generated, and then concatenates them into a single fit.

	Function Input Parameters:
		x_data - numpy array
			The x-values of the spectrum to be fitted.
		y_data - numpy array
			The y-values of the spectrum to be fitted.
		fit_result - lmfit.model.ModelResult
			An lmfit model class that contains all of the fitted values for the single input model.
		plot_components - Boolean (Optional)
			A Boolean that dictates whether or not curves for individual fit components are shown in 
			addition to the concatenated fit that shows all of the function fits. Defaults to False,
			but True will enable component plotting.

	Function Returns: This function does not have any returns.

    """
    
    fig = plt.figure(figsize=(15,6))
    plt.ylabel('Counts (Normalized)', fontsize=14)
    plt.xlabel('Wavenumber (cm$^{-1}$)', fontsize=14)
    plt.xlim(min(x_data), max(x_data))
    # plt.ylim(min(y_data)-(max(y_data)-min(y_data))*0.1, max(y_data)+(max(y_data)-min(y_data))*0.1)
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
    This function returns fit information for an input lmfit model set. 

	Function Input Parameters:
		out - lmfit.model.ModelResult 
			An lmfit model class that contains all of the fitted values for the input model class.
	Function Returns:
		fit_peak_data - numpy array
			An array containing both the peak number, as well as the sigma, center, amplitude, 
			full-width, half-max, and the height of the peaks. The data can be accessed by the 
			array positions shown here:
				fit_peak_data[i][0] = p[i]_simga
    				fit_peak_data[i][1] = p[i]_center
    				fit_peak_data[i][2] = p[i]_amplitude
    				fit_peak_data[i][3] = p[i]_fwhm
    				fit_peak_data[i][4] = p[i]_height
    """
    fit_peak_data = []
    for i in range(int(len(out.values)/5)):
        peak = np.zeros(5)
        prefix = 'p{}_'.format(i+1)
        peak[0] = out.values[prefix+'sigma']
        peak[1] = out.values[prefix+'center']
        peak[2] = out.values[prefix+'amplitude']
        peak[3] = out.values[prefix+'fwhm']
        peak[4] = out.values[prefix+'height']
        fit_peak_data.append(peak)
    return fit_peak_data


def compound_report(compound):
    """
    Wrapper fucntion that utilizes many of the functions
    within spectrafit to give the peak information of a compound
    in shoyu_data_dict.p
    """
    x_data = compound['x']
    y_data = compound['y']
    # subtract baseline
    y_data = subtract_baseline(y_data)
    # detect peaks
    peaks, peak_list = peak_detect(x_data, y_data)
    # assign parameters for least squares fit
    mod, pars = lorentz_params(peaks)
    # fit the model to the data
    out = model_fit(x_data, y_data, mod, pars)
    # export data in logical structure (see docstring)
    fit_peak_data = export_fit_data(out)
    peak_centers = [] 
    peak_sigma = [] 
    peak_ampl = []
    for i in range(len(fit_peak_data)):
        peak_sigma.append(fit_peak_data[i][0])
        peak_centers.append(fit_peak_data[i][1])
        peak_ampl.append(fit_peak_data[i][2])
    xmin = min(x_data)
    xmax = max(x_data)
    return peak_centers, peak_sigma, peak_ampl, xmin, xmax

def data_report(x_data, y_data):
    """
    Wrapper fucntion that utilizes many of the functions
    within spectrafit to give the peak information of inputted x
    and y data that have been initialized beforehand
    in shoyu_data_dict.p
    """
    # subtract baseline
    y_data = subtract_baseline(y_data)
    # detect peaks
    peaks, peak_list = peak_detect(x_data, y_data)
    # assign parameters for least squares fit
    mod, pars = lorentz_params(peaks)
    # fit the model to the data
    out = model_fit(x_data, y_data, mod, pars)
    # export data in logical structure (see docstring)
    fit_peak_data = export_fit_data(out)
    peak_centers = [] 
    peak_sigma = [] 
    peak_ampl = []
    for i in range(len(fit_peak_data)):
        peak_sigma.append(fit_peak_data[i][0])
        peak_centers.append(fit_peak_data[i][1])
        peak_ampl.append(fit_peak_data[i][2])
    xmin = min(x_data)
    xmax = max(x_data)
    return peak_centers, peak_sigma, peak_ampl, xmin, xmax
