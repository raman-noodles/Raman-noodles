"""
Tests for functions in the shoyu.py module
"""

import os
import pickle
from ramannoodles import shoyu

# open spectra library
shoyu_data_dict = pickle.load(open('raman_spectra/shoyu_data_dict.p', 'rb'))

def test_download_cas():
    """docstring"""
    # CAS registry number for water
    cas_num = '7732-18-5'
    shoyu.download_cas(cas_num)
    assert os.path.isdir('raman_spectra/'), 'Directory not found'
    
    
def test_add_jdx():
    """docstring"""
    filename = '7732185_NIST_IR.jdx'
    shoyu.add_jdx('raman_spectra/'+filename)
    assert os.path.isfile('raman_spectra/'+filename), 'File not found'

    
def test_initialize_standard_library():
    """docstring"""
    shoyu.initialize_standard_library()
    assert os.path.isfile('raman_spectra/shoyu_data_dict.p'), 'File not found'
    
def test_more_please():
    """docstring"""
    # CAS registry number for pentane
    cas_num = '109-66-0'
    shoyu.more_please(cas_num)
    assert os.path.isfile('raman_spectra/109660_NIST_IR.jdx'), 'File not found' 
    
    
def test_combine_spectra():
    """docstring"""
    compound_1 = shoyu_data_dict['WATER']
    compound_2 = shoyu_data_dict['CARBON MONOXIDE']
    data = shoyu.combine_spectra(compound_1, compound_2)
    assert len(data[0]) == len(data[1])
    
    
