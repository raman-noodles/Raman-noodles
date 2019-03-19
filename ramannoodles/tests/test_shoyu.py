"""
Test functions for the shoyu.py module
"""

import os
import pickle
from ramannoodles import shoyu

# open spectra library
shoyu_data_dict = pickle.load(open('raman_spectra/shoyu_data_dict.p', 'rb'))

def test_download_cas():
    """
    Test function that confirms that the raman_spectra/ directory exists/was created,
    and confirms that the .jdx file was saved with the correct filename.
    """
    # CAS registry number for water
    cas_num = '7732-18-5'
    shoyu.download_cas(cas_num)
    assert os.path.isdir('raman_spectra/'), 'directory not found'
    assert os.path.isfile('raman_spectra/7732185_NIST_IR.jdx'), 'file not saved correctly'


def test_add_jdx():
    """
    Test function that confirms that custom labeling is successful when updating shoyu_data_dict.p,
    and that the y units are correctly converted to ABSORBANCE instead of the default TRANSMITTENCE.
    """
    # .jdx file containing water data
    filename = '7732185_NIST_IR.jdx'
    shoyu_data_dict = shoyu.add_jdx('raman_spectra/'+filename, label='Water_label_test')
    assert 'Water_label_test' in shoyu_data_dict, 'custom label not applied successfully'
    water = shoyu_data_dict['Water_label_test']
    assert water['yunits'] == 'ABSORBANCE', 'Incorrect y units stored'


def test_initialize_standard_library():
    """
    Test function that confirms the raman_spectra/ directory is created, the .jdx files are downloaded
    and stored correctly, and that the shoyu_data_dict.p file is generated.
    """
    shoyu.initialize_standard_library()
    assert os.path.isdir('raman_spectra/'), 'Directory not found'
    assert os.path.isfile('raman_spectra/7732185_NIST_IR.jdx'), 'file not saved correctly'
    assert os.path.isfile('raman_spectra/shoyu_data_dict.p'), 'shoyu_data_dict.p not found'
    
    
def test_more_please():
    """
    Test function that confirms that the pentane .jdx file was downloaded correctly and was
    successfully added to shoyu_data_dict.p
    """
    # CAS registry number for pentane
    cas_num = '109-66-0'
    shoyu_data_dict = shoyu.more_please(cas_num)
    assert os.path.isfile('raman_spectra/109660_NIST_IR.jdx'), 'file not found'
    assert 'N-PENTANE' in shoyu_data_dict, 'N-PENTANTE not successfully added to shoyu_data_dict'


def test_combine_spectra():
    """
    Test function that confirms that the two compounds from shoyu_data_dict.p were combined sucessfully,
    that the output data has the correct shape, and that the output range is within the overall
    range of the two individual compounds.
    """
    compound_1 = shoyu_data_dict['WATER']
    compound_2 = shoyu_data_dict['CARBON MONOXIDE']
    data = shoyu.combine_spectra(compound_1, compound_2)
    assert len(data[0]) == len(data[1]), 'lengths of x and y data do not match'
    assert len(data) == 2, 'shape of output data different than expected'
    ranges = [max(compound_1['x']), min(compound_1['x']), max(compound_2['x']), min(compound_2['x'])]
    assert min(ranges) <= min(data[0]), 'output data contains values below the minimum range of either compound'
    assert max(ranges) >= max(data[0]), 'output data contains values above the maximum range of either compound'