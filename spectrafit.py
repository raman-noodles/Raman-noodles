"""
This module allows for baseline subtraction, peak detection, and
lorentzian/gaussian fitting of spectra data.
"""


from peakutils.baseline import baseline
import matplotlib.pyplot as plt


def subtract_baseline(y_data, deg=5, plot=False):
    """
    Function that fits a n-degree polynomial (default: n=5)
    baseline and subtracts it from the input data
    """
    yb = baseline(y_data, deg=deg, max_it=200)
    # to avoid strange results,
    # change all negative values to zero
    yb_plus = [0 if i < 0 else i for i in yb]
    y_out = y_data - yb_plus
    
    if plot:
        plt.figure(figsize=(10,4))
        plt.plot(x, y_data, 'b--', label='original')
        plt.plot(x, y_out, 'b', label='output')
        plt.plot(x, yb_plus, 'r', label='baseline')
        plt.plot(x, yb, 'r--', label='negative baseline')
        plt.axhline(y=0, color='orange', alpha=0.5, label='zero') 
        plt.legend()
    return y_out
