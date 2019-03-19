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
    assert os.path.isdir('raman_spectra/'), 'directory not found'
    assert os.path.isfile('raman_spectra/7732185_NIST_IR.jdx'), 'file not saved correctly'
    
    
def test_add_jdx():
    """docstring"""
    # .jdx file containing water data
    filename = '7732185_NIST_IR.jdx'
    shoyu_data_dict = shoyu.add_jdx('raman_spectra/'+filename, label='Water_label_test')
    assert os.path.isfile('raman_spectra/'+filename), 'File not found'
    assert 'Water_label_test' in shoyu_data_dict, 'custom label not applied sucessfully'
    water = shoyu_data_dict['WATER']
    assert water['yunits'] == 'ABSORBANCE', 'Incorrect y units stored'

    
def test_initialize_standard_library():
    """docstring"""
    shoyu.initialize_standard_library()
    assert os.path.isdir('raman_spectra/'), 'Directory not found'
    assert os.path.isfile('raman_spectra/shoyu_data_dict.p'), 'file not found'
    
    
def test_more_please():
    """docstring"""
    # CAS registry number for pentane
    cas_num = '109-66-0'
    shoyu_data_dict = shoyu.more_please(cas_num)
    assert os.path.isfile('raman_spectra/109660_NIST_IR.jdx'), 'file not found'
    assert 'N-PENTANE' in shoyu_data_dict, 'N-PENTANTE not successfully added to shoyu_data_dict'
    
    
def test_combine_spectra():
    """docstring"""
    compound_1 = shoyu_data_dict['WATER']
    compound_2 = shoyu_data_dict['CARBON MONOXIDE']
    data = shoyu.combine_spectra(compound_1, compound_2)
    assert len(data[0]) == len(data[1]), 'lengths of x and y data do not match'
    assert len(data) == 2, 'shape of output data different than expected'
    ranges = [max(compound_1['x']), min(compound_1['x']), max(compound_2['x']), min(compound_2['x'])]
    assert min(ranges) <= min(data[0]), 'output data contains values below the minimum range of either compound'
    assert max(ranges) >= max(data[0]), 'output data contains values above the maximum range of either compound'
    
    
