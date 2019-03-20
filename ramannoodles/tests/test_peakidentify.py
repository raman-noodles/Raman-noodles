"""
Module used to unit test the functionality and outputs the peakidentify.py module
"""
# IMPORTING MODULES 
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
from ramannoodles import peakidentify
from ramannoodles import shoyu
from ramannoodles import spectrafit


def test_peak_1D_score():
    """Evaluates the functionality of the peak_1D_score function"""
    # Initialize the test arguments 
    row_i=[0,1]
    row_j=[2,1]
    rowcat=row_i+row_j
    ArrayA=np.array([[0,1], [2,1],[0,3]])
    # Run Function for lists
    testscore=peak_1D_score(row_i,row_j,1)[0][:]
    testpeaks=peak_1D_score(row_i,row_j,1)[1][:]
    # Run Function for arrays
    Arrayscore=peak_1D_score(ArrayA[0],ArrayA[2],1)[0][:]
    arraycat=np.concatenate((ArrayA[0],ArrayA[2]))
    # make assertions
    assert len(row_i) == len(row_j), 'Input lengths do not match'
    assert len(Arrayscore) == len(arraycat), 'Output list length different than concatenated lists length'
    for i in range(len(rowcat)):
        assert testscore[i] <= 1, 'Output value outside acceptable range'

def test_score_max():
    """Evaluates the functionality of the score_max function"""
    # Initialize the test arguments 
    row_i=[0,1]
    row_j=[2,1]
    rowcat=row_i+row_j
    ArrayA=np.array([[0,1], [2,1],[0,3]])
    k=2
    arraycat=np.concatenate((ArrayA[0],ArrayA[1]))
    # Run Function for lists
    maxscores,maxpeaks = score_max(row_i,row_j,k)
    # Run Function for arrays
    Arrmaxscores,Arrmaxpeaks = score_max(ArrayA[0],ArrayA[1],k)
    # make assertions
    assert len(Arrmaxscores) == len(arraycat), 'Output list length different than array length'
    for i in range(len(arraycat)):
        assert Arrmaxscores[i] <= 2, 'Output value outside acceptable range'
        
def test_score_sort():
    """Evaluates the functionality of the score_sort function"""
    # Initialize the test arguments 
    row_i=[0,1]
    row_j=[2,1]
    rowcat=row_i+row_j
    ArrayA=np.array([[0,1], [2,1],[0,3]])
    k=2
    arraycat=np.concatenate((ArrayA[0],ArrayA[1]))
    # Run Previous Function to get max score normalization
    maxscores,maxpeaks = score_max(row_i,row_j,k)
    # Run Function for lists
    sortedscores=score_sort(row_i,row_j,max(maxscores))[0][0]
    # Run Function for arrays
    Arrsortedscores=score_sort(ArrayA[0],ArrayA[1],max(maxscores))[0][0]
    # make assertions
    assert len(arraycat) == len(Arrsortedscores), 'Output list length different than concatenated lists length'