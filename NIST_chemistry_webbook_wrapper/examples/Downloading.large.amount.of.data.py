# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 14:15:33 2016

@author: AOsipenko
"""


import pandas as pd
import numpy as np
import sys
import os
DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,os.path.join(DIR, 'NIST_chemistry_webbook_wrapper'))
from getNistData import getNIST
from Fluids_ID import Fluids_ID

"""
Example of how you can download large amount of data from NIST chemistry database to csv file,
stored on your local computer.

"""
#To get isothermic data for tempetarure from 1 to 100 with step 0.1 degC
#Lets create an array with all desired temperatures
list_of_temp = np.arange(1.,100.,0.1)

list_of_data = []
for T in list_of_temp:
    data = getNIST(fluid_id = Fluids_ID['argon'], Temp = T, Plow = 100, Phigh= 200, deltaP = 10, TypeOfData ='IsoTherm')
    list_of_data.append(data)

#Loop For will create list of pandas DataFrames each of it will have
#Isothermic properties of Argon in pressure range from 100 to 200 psia
#To combine DataFrame in one we can use padas concat 
result = pd.concat(list_of_data)

#Result then can be managed like pandas DataFrame, or can be saved in csv file

result.to_csv('NistData.csv')

#Or any other file format,
#check Pandass documentation:
#http://pandas.pydata.org/pandas-docs/stable/io.html