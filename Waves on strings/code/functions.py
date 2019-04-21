# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 09:39:30 2018

@author: Physlab121
"""
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
import scipy as sp

#takes in dict of signals,fft's them, packs them up
def fft(v_dict, sample_rate, num):

    ft_dict = {}
    freq_dict = {}
    db_dict = {}
    
    freq_arr = np.fft.rfftfreq(v_dict['1'].size, d=1/sample_rate)
    for i in range(1,num+1):
        ft_dict["{0}".format(i)] = np.fft.rfft(v_dict["{0}".format(i)])
        #freq_dict["{0}".format(i)] = np.fft.rfftfreq(v_dict["{0}".format(i)].size, d=1/sample_rate)
        

    for i in ft_dict:    
        db_dict[i] =  20*np.log(np.abs(ft_dict[i])**2)
        
        
    return ft_dict, freq_arr, db_dict
