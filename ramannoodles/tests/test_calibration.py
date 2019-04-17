"""docstring"""
import os
import h5py
from ramannoodles import dataprep


def test_new_hdf5():
    """docstring"""
    cal_file = dataprep.new_hdf5('function_test')
    assert isinstance(cal_file, h5py._hl.files.File), 'output type is not a h5py._hl.files.File'
    assert len(cal_file) == 0, 'output h5py._hl.files.File is not empty'
    try:
        dataprep.new_cal(4.2)
    except TypeError:
        print('A float was passed to the function, and it was handled well with a TypeError.')
    os.remove('function_test.hdf5')
        
        
def test_add_compound():
    """docstring"""
    cal_file = dataprep.new_hdf5('test')
    cal_file.close()
    cal_file = dataprep.add_compound('test.hdf5',
                                            'ramannoodles/tests/test_files/Methane_Baseline_Calibration.xlsx',
                                            label='Methane')
    assert list(cal_file.keys())[0] == 'Methane', 'custom label not applied correctly'
    assert len(cal_file) == 1, 'more than one first order group assigned to test.hdf5'
    assert len(cal_file['Methane']) == 3, 'more then 1 peak was stored'
    assert 'Methane/x' in cal_file, 'x data (wavenumber) not stored correctly'
    assert 'Methane/y' in cal_file, 'y data (counts) not stored correctly'
    # test that function assigns filename correctly as compound label
    cal_file1 = dataprep.new_cal('test1')
    cal_file1.close()
    cal_file1 = dataprep.add_compound('test1.hdf5',
                                         'ramannoodles/tests/test_files/Methane_Baseline_Calibration.xlsx')
    assert list(cal_file1.keys())[0] == 'Methane_Baseline_Calibration', 'filename label not applied correctly'
    try:
        dataprep.add_compound(4.2, 'CarbonMonoxide_Baseline_Calibration.xlsx')
    except TypeError:
        print('A float was passed to the function, and it was handled well with a TypeError.')
    try:
        dataprep.add_compound('test.hdp5', 4.2)
    except TypeError:
        print('A float was passed to the function, and it was handled well with a TypeError.')
    os.remove('test.hdf5')
    os.remove('test1.hdf5')