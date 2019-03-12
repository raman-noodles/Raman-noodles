"""
Tests for functions in the shoyu.py module
"""

from ramannoodles import shoyu


def test_download_cas():
    """docstring"""
    # CAS registry number for water
    cas_num = '7732-18-5'
    shoyu.download_cas(cas_num)
    assert os.path.isdir('.../raman_spectra/')
    
    
# def test_add_jdx():
#     """docstring"""
#     # i need a test jdx?

    
# def test_initialize_standard_library():
#     """docstring"""
#     shoyu.initialize_standard_library()
    
    
# def test_more_please():
#     """docstring"""
#     # CAS registry number for water
#     cas_num = '7732-18-5'
#     shoyu.more_please(cas_num)
    
    
def test_combine_spectra():
    """docstring"""
    compound_1 = 'WATER'
    compound_2 = 'CARBON MONOXIDE'
    data = shoyu.combine_spectra(compound_1, compound_2)
    assert len(data[0]) == len(data[1])
    
    
