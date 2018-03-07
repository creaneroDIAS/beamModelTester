#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 13:39:28 2018

@author: Oisin Creaner
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr

def read_dreambeam_csv(in_file):
    out_df=pd.read_csv(in_file,\
                        converters={'J11':complex,'J12':complex,\
                                    'J21':complex,'J22':complex}, \
                        parse_dates=['Time'], skipinitialspace=True)  
    return out_df

if __name__ == "__main__":
    #temporarily hard-coded filenames
    in_file_model=raw_input("Please enter the model filename:\n")#"~/outputs/test/dreamBeam/2018-03-05/SE607_1d_160M.csv"
    in_file_scope=raw_input("Please enter the scope filename:\n")#"~/outputs/test/dreamBeam/2018-03-05/IE613_1d_160M.csv"
    
    #read in the csv files from DreamBeam and format them correctly
    #want to modularise this
    model_df=read_dreambeam_csv(in_file_model)
    
    #using dreambeam input initially, will replace this with something suited to real telescope input if possible
    scope_df=read_dreambeam_csv(in_file_scope)
    
    #merges the two datagrames using time and frequency
    merge_df=pd.merge(model_df,scope_df,on=('Time','Freq'),suffixes=('_model','_scope'))
    
    #calculates the p-channel intensity as per DreamBeam for both model and scope
    merge_df['p_ch_model'] = np.abs(merge_df['J11_model'])**2+np.abs(merge_df['J12_model'])**2
    merge_df['p_ch_scope'] = np.abs(merge_df['J11_scope'])**2+np.abs(merge_df['J12_scope'])**2
    #calculates the difference between model and scope
    merge_df['p_ch_diff'] = merge_df['p_ch_model'] - merge_df['p_ch_scope']
    
    #calculates the q-channel intensity as per DreamBeam for both model and scope
    merge_df['q_ch_model'] = np.abs(merge_df['J21_model'])**2+np.abs(merge_df['J22_model'])**2
    merge_df['q_ch_scope'] = np.abs(merge_df['J21_scope'])**2+np.abs(merge_df['J22_scope'])**2
    #calculates the difference between model and scope
    merge_df['q_ch_diff'] = merge_df['q_ch_model'] - merge_df['q_ch_scope']
    
    #creates a two part plot of the values of model and scope
    #part one: plots the model and scope values for p-channel against time
    plt.figure()
    plt.title("Plot of the values in p- and q-channels over time")
    plt.subplot(211)
    plt.title("p-channel")
    plt.plot(merge_df['Time'],merge_df['p_ch_model'],label='model',color='orangered')
    plt.plot(merge_df['Time'],merge_df['p_ch_scope'],label='scope',color='darkred')
    plt.legend(frameon=False)
    plt.xticks([])
    
    #part two: plots the model and scope values for q-channel against time
    plt.subplot(212)
    plt.title("q-channel")
    plt.plot(merge_df['Time'],merge_df['q_ch_model'],label='model',color='limegreen')
    plt.plot(merge_df['Time'],merge_df['q_ch_scope'],label='scope',color='darkgreen')
    plt.xticks(rotation=90)
    plt.legend(frameon=False)
    plt.xlabel('Time')
    
    #prints the plot
    plt.show()
    
    
    
    
    #plots the differences in p-channel and q-channel values over time
    plt.plot(merge_df['Time'],merge_df['p_ch_diff'],label=r'$\Delta p$',color='red')
    plt.plot(merge_df['Time'],merge_df['q_ch_diff'],label=r'$\Delta q$',color='green')
    plt.xticks(rotation=90)
    plt.title("Plot of the differences in p- and q-channels over time")
    plt.legend(frameon=False)
    plt.xlabel('Time')
    plt.show()
    
    #calculates the pearson correlation coefficient between scope and model
    p_corr=pearsonr(merge_df['p_ch_model'],merge_df['p_ch_scope'])[0]
    q_corr=pearsonr(merge_df['q_ch_model'],merge_df['q_ch_scope'])[0]
    print("\nThe P-channel correlation is %f\nThe Q-channel correlation is %f"%(p_corr,q_corr))
    
    #calculates the root mean squared error between scope and model
    p_rmse=np.mean(merge_df['p_ch_diff']**2)**0.5
    q_rmse=np.mean(merge_df['q_ch_diff']**2)**0.5
    print("\nThe P-channel RMSE is %f\nThe Q-channel RMSE is %f"%(p_rmse,q_rmse))
