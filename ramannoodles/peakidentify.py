"""This function takes in compounds from a dictionary from shoyu, and, using spectrafit,
identifies peaks found in both the fed-in known spectra, as well as the unknown spectra
to be analyzed. From that identification, it then classifies the peaks in the unknown
spectra based on the fed-in known spectra. 
 """
import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pickle
from ramannoodles import spectrafit
from ramannoodles import shoyu


def peak_assignment(unknown_x, unknown_y, known_compound_list, precision = 0.03, plot = True):
    """This function is a wrapper function from which all classification of peaks occurs."""
    #Lets identify the peaks in the unknown spectrum.
    unknown_peaks = spectrafit.data_report(unknown_x, unknown_y)[0]

    #OK, next identify all of the peaks present in the known compound set.
    #For efficiency, we'll also compare them against the unknown in the same for loop.
    known_compound_peaks = []
    assignment_matrix = []

    for i in range(len(known_compound_list)):
        known_compound_peaks.append(spectrafit.compound_report(known_compound_list[i])[0])
        print("The peaks that we found for " + str(known_compound_list[i]['title']) + " are: ")
        print(known_compound_peaks[i])
        assignment_matrix.append(compare_unknown_to_known(unknown_peaks, known_compound_peaks[i], precision))

    #Ok, so that generates a full association matrix that contains everything we need to assign peaks.
    #Now, let's go through and actually assign text to peaks.
    unknown_peak_assignments = peak_position_comparisons(unknown_peaks, known_compound_peaks, known_compound_list, assignment_matrix)
    print(unknown_peak_assignments)

    if plot:
        plotting_peak_assignments(unknown_x, unknown_y, unknown_peaks, unknown_peak_assignments)

    percentages = percentage_of_peaks_found(known_compound_peaks, assignment_matrix, known_compound_list)
    print(percentages)


def compare_unknown_to_known(combined_peaks, known_peaks, precision):
    """This function takes in peak positions for the spectrum to be analyzed and a single known compound and
    determines if the peaks found in the known compound are present in the unknown spectrum."""
    assignment_matrix = np.zeros(len(combined_peaks))
    peaks_found = 0
    for i in range(len(combined_peaks)):
        for j in range(len(known_peaks)):
            #instead of If, call peak_1D_score
            if math.isclose(combined_peaks[i], known_peaks[j], rel_tol = precision):
                #Instead of using a 1, just input the score from the score calculator. Bigger is better.
                #Storing only the second component in the list.
                assignment_matrix[i] = 1
                peaks_found += 1
                continue
            else:
                pass
        if peaks_found == len(known_peaks):
            continue
        else:
            pass
    return assignment_matrix

def peak_position_comparisons(unknown_peaks, known_compound_peaks, known_compound_list, association_matrix):
    """This function takes in an association matrix and turns the numbers given by said matrix into
    a text label."""
    unknown_peak_assignment = []
    #Step through the unknown peaks to make an assignment for each unknown peak.

    for i in range(len(unknown_peaks)):
        #We might be able to make a small performance improvement if we were to somehow
        #not search the peaks we already had searched, but that seems to not be trivial.
        position_assignment = []
        #We'll need an outer loop that walks through all the different compound positions
        for j in range(len(known_compound_peaks)):
            if association_matrix[j][i] == 1:
                position_assignment.append(known_compound_list[j]['title'])
            else:
                pass
        unknown_peak_assignment.append(position_assignment)

    return unknown_peak_assignment

def percentage_of_peaks_found(known_peaks, association_matrix, list_of_known_compounds):
    """This function takes in a list of classified peaks, and returns a percentage of how many of the material's
    peaks are found in the unknown spectrum. This can be used as a metric of confidence."""
    percentage_dict = {}
    for i in range(len(list_of_known_compounds)):
        count_number = sum(association_matrix[i])
        percentage_dict[list_of_known_compounds[i]['title']] = (count_number/len(known_peaks[i]))*100

    return percentage_dict


def plotting_peak_assignments(unknown_x, unknown_y, unknown_peaks, unknown_peak_assignments):
    """This function plots a set of unknown peaks, and plots the assigned classification given by
    the functions within peakassignment"""
    colors = ['b', 'r', 'g', 'c', 'm', 'y', 'b']
    fig = plt.figure(figsize = (10,4), dpi = 300)
    plt.plot(unknown_x, unknown_y, color = 'black', label = 'Unknown Spectrum')
    for i in range(len(unknown_peaks)):
        plt.axvline(x = unknown_peaks[i], color = colors[i], label = unknown_peak_assignments[i], linestyle = '--')
    plt.legend(loc=0, framealpha=1)
    plt.xlabel('Wavenumber (cm$^{-1}$)', fontsize=12)
    plt.ylabel('Counts', fontsize=12)
    plt.ylim(-0.01, 1.5)
    plt.xlim(300,3800)
    plt.show()

def peak_1D_score(rowA,rowB,scoremax):
    """
    Returns scores with respect to the reciprocal of the 
    calculated Euclidean distance between peaks
    #√((x1-x2)^2) in 1D
    #√((x1-x2)^2 + (y1-y2)^2) in 2D

    Parameters:
        row A (list):  input list
        row B (list): input list
        scoremax (float): Euclidean reciprocal score divided by max score

    Returns:
        scores (list): Euclidean reciprocal scores
        peaks (tuple): peaks associated with scores
    """
    scores = []
    peaks=[]
    

    for i in range(len(rowA)):
        for j in range(len(rowB)):
            distance = np.where((rowA[i] - rowB[j]>50),np.nan,math.sqrt(sum([math.pow(rowA[i] - rowB[j], 2)])))
            if (1/(distance + 1)>.02): # Score for peaks less than 50 units apart
                scores.append((((1/(distance + 1))/scoremax)))
                peaks.append((rowA[i],rowB[j]))
            else:
                pass
    return scores,peaks

def score_max(list_input, row,k):
    """
    Returns list of scores with respect to its output max score

    Parameters:
        list_input (list):  input list
        row (list): input list
        k (int): input integer used to sort the scores / kth highest score

    Returns:
        maxscores (list): Euclidean reciprocal score divided by max score
        maxpeaks (tuple): peaks associated with max scores
    """
    try:
        maxscores,maxpeaks = peak_1D_score(list_input,row,sorted(set(peak_1D_score(list_input,row,1)[0][:]))[-k])
    
    except Exception as e:
        
        maxscores,maxpeaks = peak_1D_score(list_input,row, scoremax=1)
        
    return maxscores,maxpeaks
def score_sort(list_input, row,k):
    """
    Returns list of scores sorted

    Parameters:
        list_input (list):  input list
        row (list): input list
        k (int): input integer used to sort the scores / kth highest score

    Returns:
        sortedscores (list): sorted Euclidean distances
    """
    sortedscores = []
    sortedscores.append(score_max(list_input,row,k))
    sortedscores.sort()
    return sortedscores