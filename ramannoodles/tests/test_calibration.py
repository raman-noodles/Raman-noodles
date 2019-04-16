"""docstring"""
import h5py
from ramannoodles import calibration

def test_new_cal():
    """docstring"""
    cal_file = calibration.new_cal('function_test')
    assert isinstance(cal_file, h5py._hl.files.File), 'output type is not a h5py._hl.files.File'
    assert len(cal_file) == 0, 'output h5py._hl.files.File is not empty'
    try:
        calibration.new_cal(4.2)
    except TypeError:
        print('A float was passed to the function, and it was handled well with a TypeError.')