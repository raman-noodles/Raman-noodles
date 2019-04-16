"""docstring"""
import h5py

def new_cal(new_filename):
    """docstring"""
    # handling input errors
    if not isinstance(new_filename, str):
        raise TypeError('Passed value of `filename` is not a string! Instead, it is: '
                        + str(type(new_filename)))
    # w- mode will create a file and fail if the file already exists
    cal_file = h5py.File('{}.hdf5'.format(new_filename), 'w-')
    return cal_file