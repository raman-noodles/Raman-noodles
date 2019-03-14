"""
This module allows for IR spectra to be downloaded from the NIST Chemistry WebBook.
The CAS Registry Number for the compound is used to download the data and then add
it to a dictionary called shoyu_data_dict
Functionality also allows for any .jdx file to be added to the shoyu_data_dict
pickle file.

Developed by Raman-Noodles team.
"""

import os
import pickle
import jcamp
import requests
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from ramannoodles import spectrafit


def download_cas(cas_num):
    """
    Function that saves raman data downloaded from NIST webpage.

	Function Input Parameters:
		cas_num - string
			The CAS number associated with the compound that is intended to be downloaded. 
			It must be in the format of a string, but it is insensitive to having hyphens.

	Function Returns:
		This function has no returns. 

    Notes: This function is meant to be an internal function to this module, and is not intended to be interacted with by 
the user, though it is not specifically problematic if it is. It is called by two other functions, the 
`intialize_standard_library` and `more_please` functions.  

    """
    # drop any '-' from cas_num
    cas_num = ''.join(cas_num.split('-'))
    if not os.path.exists('../raman_spectra/'+cas_num+'_NIST_IR.jdx'):
        os.makedirs('../raman_spectra', exist_ok=True)
        url = 'https://webbook.nist.gov/cgi/cbook.cgi?JCAMP=C'+cas_num+'&Index=1&Type=IR'
        data = requests.get(url, allow_redirects=True)
        if data.text == '##TITLE=Spectrum not found.\n##END=\n':
            print("""Bad Request: CAS # not found. Please verify
             with NIST Chemistry WebBook.""")
        else:
            if data.status_code == 200:
                open('../raman_spectra/'+cas_num+'_NIST_IR.jdx', 'wb').write(data.content)
                print('file downloaded to raman_spectra folder')
            else:
                print('Request status: {}'.format(data.status_code))
    else:
        print('file already in raman_spectra folder')


def add_jdx(filename, label=None):
    """
    Function that reads and adds a .jdx file to the raman_data_dict pickle file.
	Function Input Parameters:
		filename - string
			This filename is the exact file name that is affiliated with the .jdx file that has been
			downloaded that the user wants to add to their pickle file. 
	Function Returns:
		shoyu_data_dict - dictionary
			This is the dictionary that contains the data loaded from the pickle file and is the 
			common way in which the user interacts with data in this software.

    Notes: As with the `download_cas` function, this is not intended to be a user-interactable function.

    """
    shoyu_data_dict = pickle.load(open('../raman_spectra/shoyu_data_dict.p', 'rb'))
    data = jcamp.JCAMP_reader(filename)
    y_abs = 1 - data['y']
    data['yunits'] = 'ABSORBANCE'
    data['y'] = y_abs
    if label is None:
        shoyu_data_dict.update({data['title'].upper(): data})
        print('{} loaded into the dictionary - shoyu_data_dict.p'.format(data['title']))
    else:
        shoyu_data_dict.update({label: data})
        print('{} loaded into the dictionary - shoyu_data_dict.p'.format(label))
    pickle.dump(shoyu_data_dict, open('../raman_spectra/shoyu_data_dict.p', 'wb'))
    return shoyu_data_dict


def initialize_standard_library():
    """
    Function that downloads a standard library of raman spectra from the NIST Chemistry WebBook. It generates a 
    folder and a pickle file for storing data for future use.

    	Function Input Parameters: This function does not take input parameters

    	Function Returns: This function has no returns.

    Notes: This function must be run BEFORE any other function in this package, as all the other packages 
    assume the presence of the folder created by this function. 
    """
    # dictionary of CAS registry numbers for standard library
    cas_lib = {'water':'7732-18-5',
               'carbon monoxide':'630-08-0',
               'carbon dioxide':'124-38-9',
               'formic acid':'64-18-6',
               'isopropyl alcohol':'67-63-0',
               'ethanol':'64-17-5',
               'acetone':'67-64-1'}
    # initialize empty shoyu_data_dict
    shoyu_data_dict = {}
    os.makedirs('../raman_spectra', exist_ok=True)
    pickle.dump(shoyu_data_dict, open('../raman_spectra/shoyu_data_dict.p', 'wb'))
    for item in cas_lib:
        cas_num = ''.join(cas_lib[item].split('-'))
        download_cas(cas_num)
        add_jdx('../raman_spectra/'+cas_num+'_NIST_IR.jdx', label=None)


def more_please(cas_num, label=None):
    """
    Function that downloads a spectra from the NIST
    database, adds it to shoyu_data_dict, pickles shoyu_data_dict
    and returns the updated shoyu_data_dict.
    
    	Function Input Parameters: 
		cas_num - string
			The CAS number that is associated with the compound intended to be downloaded
			It must be in the format of a string, but it is insensitive to hyphens.
		label - string (Optional)
			By passing this label, instead of using the title found on the NIST webbook, when 
			the compound spectral data is added to the shoyu_data_dict it will use the text of
			`label` as the dictionary key for this spectral data. 

	Function Returns:
		shoyu_data_dict - Dictionary
			This is the dictionary that contains the data loaded from the pickle file, and is
			the common way in which the user interacts with data in this software.

    """
    # Drop any '-' from cas_num
    cas_num = ''.join(cas_num.split('-'))
    download_cas(cas_num)
    shoyu_data_dict = add_jdx('../raman_spectra/'+cas_num+'_NIST_IR.jdx', label)
    return shoyu_data_dict


def combine_spectra(compound_1, compound_2, plot=False):
    """
    Function that combines two spectrum via interpolation and summation.
    



    """
    # compound 1
    x_comp1 = compound_1['x']
    y_comp1 = compound_1['y']
    y_comp1 = spectrafit.subtract_baseline(y_comp1)
    # compound 2
    x_comp2 = compound_2['x']
    y_comp2 = compound_2['y']
    y_comp2 = spectrafit.subtract_baseline(y_comp2)
    # zip x and y values
    comp1_data = list(zip(x_comp1, y_comp1))
    comp2_data = list(zip(x_comp2, y_comp2))
    #clean comp1
    comp1_data_clean = []
    for i in range(1, len(comp1_data)-1):
        if comp1_data[i][0] == comp1_data[i-1][0]:
            pass
        else:
            comp1_data_clean.append(comp1_data[i])
    # clean comp2
    comp2_data_clean = []
    for i in range(1, len(comp2_data)-1):
        if comp2_data[i][0] == comp2_data[i-1][0]:
            pass
        else:
            comp2_data_clean.append(comp2_data[i])
    # unzip values
    x_comp1, y_comp1 = zip(*comp1_data_clean)
    x_comp2, y_comp2 = zip(*comp2_data_clean)
    # interpolate data
    comp1_int = interpolate.interp1d(x_comp1, y_comp1, kind='cubic')
    comp2_int = interpolate.interp1d(x_comp2, y_comp2, kind='cubic')
    # define ranges
    comp1_range = np.arange(int(min(x_comp1))+1, int(max(x_comp1)), 1)
    comp2_range = np.arange(int(min(x_comp2))+1, int(max(x_comp2)), 1)
    # run interpolations
    y_comp1_interp = comp1_int(comp1_range)
    y_comp2_interp = comp2_int(comp2_range)
    # zip interpolated values
    comp1_data_int = list(zip(comp1_range, y_comp1_interp))
    comp2_data_int = list(zip(comp2_range, y_comp2_interp))
    # add the two spectra
    combined = sorted(comp1_data_int + comp2_data_int)
    # add by like
    d = {x:0 for x,_ in combined}
    for name,num in combined:
        d[name] += num
    sum_combined = list(map(tuple, d.items()))
    # unzip
    x_combined, y_combined = zip(*sum_combined)
    # set as arrays
    x_combined = np.asarray(x_combined)
    y_combined = np.asarray(y_combined)
    if plot:
        # plot original data and combined plot
        plt.figure(figsize=(15,5))
        plt.plot(x_comp1, y_comp1, 'b--', label=compound_1['title'])
        plt.plot(x_comp2, y_comp2, 'g--', label=compound_2['title'])
        plt.plot(x_combined, y_combined, 'r', label='Combination', linewidth=2, alpha=0.7)
        plt.legend()
        plt.xlabel('cm$^{-1}$', fontsize=14)
        plt.ylabel('Absoprtion', fontsize=14)
    return x_combined, y_combined
