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


def download_cas(cas_num):
    """
    Function that saves raman data
    downloaded from NIST webpage.
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
                print('file downloaded too raman_spectra folder')
            else:
                print('Request status: {}'.format(data.status_code))
    else:
        print('file already in raman_spectra folder')


def add_jdx(filename, label=None):
    """
    Function that reads and adds a .jdx file to the
    raman_data_dict pickle file.
    """
    shoyu_data_dict = pickle.load(open('../raman_spectra/shoyu_data_dict.p', 'rb'))
    data = jcamp.JCAMP_reader(filename)
    y_abs = 1 - data['y']
    data['yunits'] = 'ABSORBANCE'
    data['y'] = y_abs
    if label is None:
        shoyu_data_dict.update({data['title'].upper(): data})
        print('{} added to shoyu_data_dict.p'.format(data['title']))
    else:
        shoyu_data_dict.update({label: data})
        print('{} added to shoyu_data_dict.p'.format(label))
    pickle.dump(shoyu_data_dict, open('../raman_spectra/shoyu_data_dict.p', 'wb'))
    return shoyu_data_dict


def initialize_standard_library():
    """
    Function that downloads a standard library of raman spectra
    from the NIST Chemistry WebBook. It generates a folder and a
    pickle file for storing data for future use.
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
    """
    # Drop any '-' from cas_num
    cas_num = ''.join(cas_num.split('-'))
    download_cas(cas_num)
    shoyu_data_dict = add_jdx('../raman_spectra/'+cas_num+'_NIST_IR.jdx', label)
    return shoyu_data_dict
