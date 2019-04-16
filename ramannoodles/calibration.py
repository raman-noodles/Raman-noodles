"""docstring"""
import h5py
import pandas as pd
from ramannoodles import spectrafit


def new_cal(new_filename):
    """docstring"""
    # handling input errors
    if not isinstance(new_filename, str):
        raise TypeError('Passed value of `filename` is not a string! Instead, it is: '
                        + str(type(new_filename)))
    # w- mode will create a file and fail if the file already exists
    cal_file = h5py.File('{}.hdf5'.format(new_filename), 'w-')
    return cal_file


def add_compound(cal_filename, data_filename, label=None):
    """docstring"""
    # handling input errors
    if not isinstance(cal_filename, str):
        raise TypeError('Passed value of `cal_filename` is not a string! Instead, it is: '
                        + str(type(cal_filename)))
    if not isinstance(data_filename, str):
        raise TypeError('Passed value of `data_filename` is not a string! Instead, it is: '
                        + str(type(data_filename)))
    # r+ is read/write mode and will fail if the file does not exist
    cal_file = h5py.File(cal_filename, 'r+')
    data = pd.read_excel(data_filename, header=None, names=('x', 'y'))
    if data_filename.split('.')[-1] == 'xlsx':
        data = pd.read_excel(data_filename, header=None, names=('x', 'y'))
    elif data_filename.split('.')[-1] == 'csv':
        data = pd.read_csv(data_filename, header=None, names=('x', 'y'))
    else:
        print('data file type not recognized')
    # ensure that the data is listed from smallest wavenumber first
    if data['x'][:1].values > data['x'][-1:].values:
        data = data.iloc[::-1]
        data.reset_index(inplace=True, drop=True)
    else:
        pass
    # peak detection and data fitting
    peaks = spectrafit.peak_detect(data['x'].values, data['y'].values, height=10, prominence=20)[0]
    mod, pars = spectrafit.set_params(peaks)
    out = spectrafit.model_fit(data['x'].values, data['y'].values, mod, pars)
    fit_result = spectrafit.export_fit_data(out)
    # write data to .hdf5 using custom label if provided
    if label is not None:
        cal_file['{}/x'.format(label)] = data['x']
        cal_file['{}/y'.format(label)] = data['y']
        for i, _ in enumerate(fit_result):
            cal_file['{}/Peak_{}'.format(label, i+1)] = fit_result[i]
    else:
        label = (data_filename.split('/')[-1]).split('.')[0]
        cal_file['{}/x'.format(label)] = data['x']
        cal_file['{}/y'.format(label)] = data['y']
        for i, _ in enumerate(fit_result):
            cal_file['{}/Peak_{}'.format(label, i+1)] = fit_result[i]
    return cal_file