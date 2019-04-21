# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 19:49:06 2018

@author: joseph levine

We used the output from lab view as out array (lmv file). if you did not you will have to
set your sample time manually

makes sure functions file is in directory

"""

from functions import fft
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
import scipy as sp
import scipy.signal as sig
plt.close('all')


#input or hard code file names

sampleHZ = 50000 #should be able to extract this automatically but i couldent get it to work :(
select_input = 'hard code'
if select_input == 'hard code':
    pickup_number = 4
    filename = "DATA/lowedata_2.lvm"
else:
    pickup_number = int(input("how many pickups did you use? "))
    if pickup_number == 1:
        filenames_dict["1"] = input("enter file name  ")
    else:
        for i in range(pickup_number):
            filenames_dict["{0}".format(i+1)] = input("enter name  ")

#unpack data,make new dict
v_dict = {}
tSEC = pl.loadtxt(filename, skiprows = 23, unpack = True, usecols = (0,))
for i in range(pickup_number):
    v_dict["{0}".format(i+1)] = pl.loadtxt(filename, skiprows = 23, unpack = True, usecols = (i + 1,))
    
#run fft
ft_dict, freq_arr, db_dict = fft(v_dict, sampleHZ, pickup_number)

#generate peak frequencys 
peak_freqHZ_dict = {}

for i in range(pickup_number):     
     peak_freq_index = sig.argrelmax(db_dict["{0}".format(i + 1)], order =  100)[0]
     peak_freq_temp_arr = np.zeros(len(peak_freq_index))
     for j in range(len(peak_freq_index)):
         peak_freq_temp_arr[j] = freq_arr[int(peak_freq_index[j])] 
     peak_freqHZ_dict["{0}".format(i+1)] = peak_freq_temp_arr
     peak_freq_temp_arr= np.zeros(len(peak_freq_index))

     
fundHZ = peak_freqHZ_dict['1'][0]

#1= natural frequency units. fundamental freq natural = 1/2. this makes the length of the string = 1
if 1:    
    freq_arr =  freq_arr/(2 * fundHZ)
    tNAT = tSEC * 2 * fundHZ
    
#1 = natural amplitude units, 0 -> dB, 1 -> fundamential = 1 amplitude unit
if 1:
    for i in range(pickup_number):
        amp_temp = db_dict["{0}".format(i + 1)][peak_freq_index[0]]
        db_dict["{0}".format(i + 1)] /= amp_temp
        


"""        
plot stuff
"""     
#dB v freq
if 1:
    plt.figure(1)
    plt.plot(freq_arr, db_dict['1'], "r-")
    plt.xlim(0,18)    
    
    plt.figure(2)
    plt.plot(freq_arr, db_dict['2'], "b-")
    plt.xlim(0,18)

    plt.figure(3)
    plt.plot(freq_arr, db_dict['3'], "m-")
    plt.xlim(0,18)

    plt.figure(4)
    plt.plot(freq_arr, db_dict['4'], "b.")
    plt.xlim(0,18)
    
#voltage v time
if 0:
    plt.figure(5)
    plt.plot(tNAT, v_dict['1'], 'b-') #v_dict{'i'} plots pickup i 
    plt.xlabel("Time * 2 * fundfreq")
    plt.ylabel("Voltage")
    
    plt.figure(6)
    plt.plot(tNAT, v_dict['2'], 'b-') #v_dict{'i'} plots pickup i 
    plt.xlabel("Time * 2 * fundfreq")
    plt.ylabel("Voltage")
    
    plt.figure(7)
    plt.plot(tNAT, v_dict['3'], 'b-') #v_dict{'i'} plots pickup i 
    plt.xlabel("Time * 2 * fundfreq")
    plt.ylabel("Voltage")
    
    plt.figure(8)
    plt.plot(tNAT, v_dict['4'], 'b-') #v_dict{'i'} plots pickup i 
    plt.xlabel("Time * 2 * fundfreq")
    plt.ylabel("Voltage")

#frequency time spectrum
if 0:
    plt.figure(9)
    f, t, Sxx = sig.spectrogram(v_dict['1'], fs = sampleHZ , nperseg= 5000)
    pl.pcolormesh(t, f, Sxx)
    pl.colorbar(label = 'amplitude')
    pl.ylabel('Frequency (Hz)')
    pl.xlabel('Time / t0')
    plt.ylim(0,18)
    pl.show()





















        

