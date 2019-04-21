# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 12:38:08 2018

@author: jlevine and kwilliams
"""
import numpy as np
from functions import fft
import matplotlib.pyplot as plt
import scipy.signal as sig
plt.close('all')

#b_n comes from integral_{0}^{1} f(x) sin(n pi x) dx   where f(x) = initial conditions
#which are given by the triangle whose apex is at (x = p, y =a)
def b_n(n):
    return 2*a/(np.pi**2 * n**2*p*(1-p)) * np.sin(n*p*np.pi)
    

def u_n(n,t,x):
    return np.sin(n * np.pi * x) * np.exp(-damp * t) * b_n(n) * (np.cos(np.sqrt(n**2 + damp**2) * np.pi * t) +  \
           damp / (np.sqrt(n**2 + damp**2)) * np.sin(np.sqrt(n**2 + damp**2) *np.pi * t)) 
    

#params
n_terms = 50
xf = 1 #units are based on length = 1.
tf =3#time to run for 
dt = .01 #affects fft. big time step limits the highest frequency you can see, but it should be big for string mode or it takes forever
tsteps = int(tf/dt)
a = 1 #amp of pluck
p=.3 #pluckpoint
damp = .003  #.003 seems to be about right 

plot_type ='string' #fft or string

if plot_type == 'fft': #0 = calculate displacement for every dx , 1 = calculate only where you put "pickups" required for fft
    loc_arr = np.array([.515]) #locations of pickups
    
if plot_type == 'string':
    xsteps = 50
    loc_arr = np.linspace(0, 1, xsteps)

#throws all b_n's into an array
fourier_components_arr = np.zeros(n_terms)
for i in range(n_terms):
    fourier_components_arr[i] = b_n(i+1)

dis_dict = {}
num = len(loc_arr)
dis_temp = np.zeros([(n_terms),(tsteps),(len(loc_arr))])


for i in range(n_terms):
    for j in range(1,tsteps+1):
        for k in range(len(loc_arr)):
            dis_temp[i, j-1,  k] =  u_n(i + 1, j*dt, loc_arr[k])

dis_ana = np.sum(dis_temp, axis = 0)
#pack into a dictionary for ease of processing
v_ana_dict={}
for i in range(len(loc_arr)):
    v_ana_dict["{0}".format(i+1)] = dis_ana[:,i]

"""
Plot stuff. Type of plots are set in by plot_type
"""

#fft the output and plot
if plot_type == 'fft':
    ft_ana_dict, freq_ana_arr, db_ana_dict = fft(v_ana_dict,1/dt, num) 

    #1 -> natural amplitude units, 0 -> dB, fundamential defined as 1 amplitude unit
    if 1:
        peak_freqHZ_dict = {}

        for i in range(len(loc_arr)):     
             peak_freq_ana_index = sig.argrelmax(db_ana_dict["{0}".format(i + 1)], order =  10)[0]
             peak_freq_temp_arr = np.zeros(len(peak_freq_ana_index))
             for j in range(len(peak_freq_ana_index)):
                 peak_freq_temp_arr[j] = freq_ana_arr[int(peak_freq_ana_index[j])] 
             peak_freqHZ_dict["{0}".format(i+1)] = peak_freq_temp_arr
             peak_freq_temp_arr= np.zeros(len(peak_freq_ana_index))

        for i in range(len(loc_arr)):
            amp_ana_temp = db_ana_dict["{0}".format(i + 1)][peak_freq_ana_index[0]]
            db_ana_dict["{0}".format(i + 1)] /= amp_ana_temp
        
    for i in range(len(loc_arr)):
        plt.figure(i+10)
        plt.plot(freq_ana_arr, db_ana_dict['{0}'.format(i+1)], "b-")   
        plt.xlim(0,18)
        plt.ylim(min(db_ana_dict['{0}'.format(i+1)]) - .2, 1.2) #good to have on if you natralize amplitude units
        plt.xlabel("freq/f_0")
        plt.ylabel("amp/amp_0 (semilog)")
        

else:
 
    #both of these plots look better if you run it for 2 time units 
    plt.figure(10)
    plt.imshow(dis_ana)
    plt.colorbar(label = 'displacement')
    plt.xlabel('dx along string')
    plt.ylabel('time (units of dx)')
    plt.title(' ')
    
    numplots = 10
    color=iter(plt.cm.rainbow(np.linspace(0,1,numplots)))
    
    plt.figure(11)
    for i in range(numplots):
        c=next(color)
        plt.plot(range(0,len(dis_ana[0])),dis_ana[int(i/numplots * tf/dt)], c = c, label='t = %s' % str(round(i/numplots *tf, 2)))
        plt.xlabel('dx along string')
        plt.ylabel('displacement')
    plt.legend()
    
    """
    #3d surface plot. Does not work but would be cool if it did!!!
    plt.figure(12)
    x = np.arange(0,xf,xsteps )
    y = np.linspace(0, tf, tf/dt)
    X, Y = np.meshgrid(x, y)
    ax.scatter(x, y, dis_ana, 50, cmap='binary')
    """















































