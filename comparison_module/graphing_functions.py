# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 13:40:49 2018

@author: User
"""

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from scipy.stats.stats import pearsonr


from appearance_functions import gen_pretty_name
from appearance_functions import colour_models
from appearance_functions import list_to_string
from appearance_functions import channel_maker
from utility_functions import plottable 
from io_functions import prep_out_file



def plot_against_freq_time(merge_df, key, modes, source):
    '''
    This function generates 3d colour plots against frequency and time for the 
    given value for a given channel
    '''
    y_var="Freq"
    x_var="d_Time"
    
    
    print("Generating a 3-d plot of "+gen_pretty_name(source)+" for "+key)
    plt.figure()
    if source == "diff":
        graph_title="\n".join([modes['title'],
            ("Plot of the differences in %s\n over time and frequency"%key)])
    else:
        graph_title="\n".join([modes['title'],
            ("Plot of the "+gen_pretty_name(source)+" for "+key+
             "-channel \nover "+gen_pretty_name(x_var)+ "and "+
             gen_pretty_name(y_var)+".")])
    plt.title(graph_title)

    #plots the channel in a colour based on its name
    plt.tripcolor(plottable(merge_df,x_var),
                  plottable(merge_df,y_var),
                  plottable(merge_df,(key+'_'+source)),
                  cmap=plt.get_cmap(colour_models(key+'_s')))
    plt.legend(frameon=False)
    #plots x-label using start time 
    plt.xlabel(gen_pretty_name(x_var,units=True)+"\nStart Time: "+str(min(merge_df.Time)))
    plt.ylabel(gen_pretty_name(y_var,units=True))
    plt.colorbar()
    #prints or saves the plot
    if modes['out_dir'] == None:
        plt.show()
    else:
        plt_file=prep_out_file(modes,source=source,plot="vals",dims="nd",
                               channel=key,
                               out_type=modes['image_type'])
        print("plotting: "+plt_file)
        plt.savefig(plt_file,bbox_inches='tight')
        plt.close()

def animated_plot(merge_df, modes, var_x, var_ys, var_t, source, time_delay=20,
                  plot_name=""):
    '''
    Produces an animated linegraph(s) with the X, Y and T variables specified
    '''

    fig, ax = plt.subplots()
    fig.set_tight_layout(True)
    
    #hard coded for now, need to parameterise
    percentile_gap = 5
    multiplier = 1.5
    
    
    #sets default values for max_ and min_y
    max_y= np.nextafter(0,1) #makes max and min values distinct
    min_y = 0
    

    
    
    # Plot a scatter that persists (isn't redrawn) and the initial line.
    var_t_vals = np.sort(merge_df[var_t].unique())
    var_t_val=var_t_vals[0]
    
    str_channel = list_to_string(var_ys,", ")
    var_t_string = str(var_t_val).rstrip('0').rstrip('.')
    anim_title=("Plot of "+gen_pretty_name(source)+" for "+
                gen_pretty_name(str_channel)+" against "+
                gen_pretty_name(var_x)+ " at\n"+gen_pretty_name(var_t)+
                " of "+gen_pretty_name(var_t_string))
    label = "\n".join([modes["title"],anim_title])
    
    print("Generating an Animated "+anim_title)
    
    plt.title(label)
    
    var_x_vals =plottable(merge_df.loc[merge_df[var_t]==var_t_val].reset_index(drop=True),
                          var_x)
    
    lines = []
    
    for i in range(len(var_ys)):
        var_y = var_ys[i]
        
        var_y_vals = plottable(merge_df.loc[merge_df[var_t]==var_t_val].reset_index(drop=True),
                               (var_y+"_"+source))
    

        line, = ax.plot(var_x_vals, var_y_vals, color=colour_models(var_y))
        lines.append(line)
            #code to set x and y limits.  
        #Really want to get a sensible way of doing this
        if plottable(merge_df[(var_ys[i]+"_"+source)]).min() < 0:
            local_min_y=np.percentile(plottable(merge_df,(var_ys[i]+"_"+source)),percentile_gap)*multiplier
        else:
            local_min_y = 0
        min_y=min(min_y,local_min_y)
        #min_y=0#min(merge_df[(var_y+"_"+source)].min(),0)
        local_max_y=np.percentile(plottable(merge_df,(var_ys[i]+"_"+source)),100-percentile_gap)*multiplier
        max_y=max(max_y,local_max_y)
    
    ax.set_ylim(min_y,max_y)
    

    ax.set_xlabel(gen_pretty_name(var_x,units=True))
    ax.set_ylabel(channel_maker(var_ys,modes,", ")+" flux\n(arbitrary units)")    
 
    ax.legend(frameon=False)
    
    if modes['out_dir']==None:
        repeat_option = True
    else:
        repeat_option = False
    
    #creates a global variable as animations only work with     
    global anim
    anim = FuncAnimation(fig, update_a, frames=range(len(var_t_vals)), 
                                 interval=time_delay,
                                 fargs=(merge_df, modes, var_x, var_ys, var_t, 
                                        source,lines,ax),
                                 repeat=repeat_option)

    if modes['out_dir']!=None:
        str_channel = channel_maker(var_ys,modes)
        #str_channel = list_to_string(var_ys,", ")
        plt_file = prep_out_file(modes,source=source,plot=plot_name,dims="nd",
                               channel=str_channel,out_type=modes['image_type'])
        anim.save(plt_file, dpi=80, writer='imagemagick')
    else:
        plt.show()# will just loop the animation forever.

def plot_values_1f(merge_df, m_keys, modes):
    '''
    This function takes a merged dataframe as an argument and plots a graph of
    each of the various values for the model and the scope against time.
    
    This plot is only usable and valid if the data is ordered in time and has 
    only a single frequency
    '''
    
    
    for key in m_keys:
        #creates a two part plot of the values of model and scope
        #part one: plots the model and scope values per channel against time
        print("Plotting values in "+key)
        plt.figure()
        graph_title="\n".join([modes['title'],
                        ("Plot of the values in "+key+"-channel over time"+
                         "\nat %.2f MHz"%(min(merge_df.Freq)/1e6))])
        
        plt.title(graph_title)

        #plots the model in one colour
        plt.plot(plottable(merge_df,"Time"),
                 plottable(merge_df,(key+'_model')),
                 label='model',
                 color=colour_models(key+'_light'))
        #plots the scope in another colour
        plt.plot(plottable(merge_df,"Time"),
                 plottable(merge_df,(key+'_scope')),
                 label='scope',
                 color=colour_models(key+'_dark'))
        plt.legend(frameon=False)
        #plots the axis labels rotated so they're legible
        plt.xticks(rotation=90)
        plt.xlabel(gen_pretty_name('Time',units=True))
        
        #prints or saves the plot
        if modes['out_dir'] == None:
            plt.show()
        else:
            plt_file=prep_out_file(modes,plot="vals",dims="1d",channel=key,
                                   freq=min(merge_df.Freq),
                                   out_type="png")
            print("plotting: "+plt_file)
            plt.savefig(plt_file,bbox_inches='tight')
            plt.close()
    return(0)
    

def four_var_plot(merge_df,modes,var_x,var_y,var_z,var_y2,source):
    '''
    Plots a two part plot of four variables from merge_df as controlled by 
    modes.
    
    Plot 1 is a 3-d colour plot with x, y and z variables controlled by 
    arguments.
    
    Plot 2 is a 2-d scatter plot with the same x parameter and another y 
    variable
    
    var_z must be one of the dependent variables
    '''
    print("Plotting "+gen_pretty_name(source)+" for "+gen_pretty_name(var_z)+\
          " against "+gen_pretty_name(var_x)+ " and "+gen_pretty_name(var_y)+\
          " and "+ gen_pretty_name(var_y2)+" against "+gen_pretty_name(var_x))
    plt.figure()
    plt.subplot(211)
    upper_title=("Plot of "+gen_pretty_name(source)+\
                 " for "+gen_pretty_name(var_z)+" against "+\
                 gen_pretty_name(var_x)+ " and "+gen_pretty_name(var_y))
    label = "\n".join([modes["title"],upper_title])
    plt.title(label)
    
    plt.tripcolor(plottable(merge_df,var_x),
                  plottable(merge_df,var_y),
                  plottable(merge_df,(var_z+'_'+source)), 
                  cmap=plt.get_cmap(colour_models(var_z+'_s')))
    
    #TODO: fix percentile plotting limits
    plt.clim(np.percentile(plottable(merge_df,(var_z+'_'+source)),5),
             np.percentile(plottable(merge_df,(var_z+'_'+source)),95))
    
    #plots axes
    plt.xticks([])
    plt.ylabel(gen_pretty_name(var_y, units=True))
    #plt.colorbar()
    
    plt.subplot(212)

    lower_title=("Plot of "+gen_pretty_name(var_y2)+" against "+\
                 gen_pretty_name(var_x))
    plt.title(lower_title)
    
    #plots the scattergraph
    plt.plot(plottable(merge_df,var_x),
             plottable(merge_df,var_y2),
             color=colour_models(var_y2), marker=".", linestyle="None")
    
    plt.xlabel(gen_pretty_name(var_x, units=True))
    plt.ylabel(gen_pretty_name(var_y2, units=True))
    plt.legend(frameon=False)

    #prints or saves the plot
    if modes['out_dir'] == None:
        plt.show()
    else:
        plt_file=prep_out_file(modes,source=source,plot=var_x,dims="nd",
                               channel=var_z,
                               out_type=modes['image_type'])
        print("plotting: "+plt_file)
        plt.savefig(plt_file,bbox_inches='tight')
        plt.close()




def update_a(i,merge_df, modes, var_x, var_ys, var_t, source,lines,ax):
    '''
    Update function for animated plots
    '''
    
    var_t_vals = np.sort(merge_df[var_t].unique())
    var_t_val=var_t_vals[i]
    str_channel = list_to_string(var_ys,", ")
    var_t_string = str(var_t_val).rstrip('0').rstrip('.')
    anim_title=("Plot of "+gen_pretty_name(source)+" for "+
                gen_pretty_name(str_channel)+" against "+
                gen_pretty_name(var_x)+ " at\n"+gen_pretty_name(var_t)+
                " of "+gen_pretty_name(var_t_string))
    label = "\n".join([modes["title"],anim_title])
    plt.title(label)
    
    var_x_vals =plottable(merge_df.loc[merge_df[var_t]==var_t_val].reset_index(drop=True),
                          var_x)
    
    for y_index in range(len(var_ys)):
        var_y = var_ys[y_index]
        var_y_vals = plottable(merge_df.loc[merge_df[var_t]==var_t_val].reset_index(drop=True),
                               (var_y+"_"+source))

        lines[y_index].set_data(var_x_vals, var_y_vals)


def plot_values_nf(merge_df, m_keys, modes):
    '''
    This function takes a merged dataframe as an argument and plots a graph of
    each of the various values for the model and the scope against time and 
    frequency.
    

    '''
    time_delay = 1000.0/modes['frame_rate']
    sources = []
    
    if "value" in modes["plots"]:
        sources.append("model")
        sources.append("scope")
    if "diff" in modes["plots"]:
        sources.append("diff")
        
    
    if modes['three_d']=="colour":
        for key in m_keys:
            #creates a plot each of the values of model and scope
            
            for source in sources:
                plot_against_freq_time(merge_df, key, modes, source)

    elif modes['three_d']=="anim":
        for source in sources:
            
            animated_plot(merge_df, modes, 'Freq', m_keys, "Time", source, time_delay)
#        if "each" in modes['values']:
##            print("WARNING: Each mode not supported by animations at this time")
#            for key in m_keys: #analyses them one at a time
#                for source in ["model","scope"]:
#                    animated_plot(merge_df, modes, 'Freq', [key], "Time", source, time_delay=20)
#        else: #allows plots to be overlaid 
#            for source in ["model","scope"]:
#                animated_plot(merge_df, modes, 'Freq', m_keys, "Time", source, time_delay=20)
                
    elif modes['three_d']=="animf":
        for source in sources:
            animated_plot(merge_df, modes, "d_Time", m_keys, 'Freq', source, time_delay)
#        if "each" in modes['values']:
##            print("WARNING: Each mode not supported by animations at this time")
#            for key in m_keys: #analyses them one at a time
#                for source in ["model","scope"]:
#                    animated_plot(merge_df, modes, "d_Time", [key], 'Freq', source, time_delay=20)
#        else: #allows plots to be overlaid 
#            for source in ["model","scope"]:
#                animated_plot(merge_df, modes, "d_Time", m_keys, 'Freq', source, time_delay=20)
                
    else:
        print("WARNING: No valid value for 3d plots")
#            plt.figure()
#            graph_title="\n".join([modes['title'],("Plot of the values in "+key+"-channel \nover time "+
#                      "and frequency for "+source)])
#            plt.title(graph_title)
#    
#            #plots the channel in a colour based on its name
#            plt.tripcolor(merge_df.d_Time,merge_df.Freq,plottable(merge_df[key+'_'+source]),
#                          cmap=plt.get_cmap(colour_models(key+'_s')))
#            plt.legend(frameon=False)
#            #plots x-label for both using start time 
#            plt.xlabel("Time in seconds since start time\n"+str(min(merge_df.Time)))
#            plt.ylabel("Frequency")
#            plt.colorbar()
#            #prints or saves the plot
#            if modes['out_dir'] == None:
#                plt.show()
#            else:
#                plt_file=prep_out_file(modes,source=source,plot="vals",dims="nd",
#                                       channel=key,
#                                       out_type="png")
#                print("plotting: "+plt_file)
#                plt.savefig(plt_file,bbox_inches='tight')
#            plt.close()
    return(0)    






    
def plot_diff_values_1f(merge_df, m_keys, modes):
    '''
    This function takes a merged dataframe as an argument and 
    plots the differences in various channel values over time
    
    This plot is only usable and valid if the data is ordered in time and has 
    only a single frequency
    '''
    print("Plotting the differences in "+channel_maker(m_keys,modes,", "))
    plt.figure()
    
    graph_title = "\n".join([modes['title'],"Plot of the differences in "])
    for key in m_keys:
        plt.plot(plottable(merge_df,"Time"),
                 plottable(merge_df,(key+'_diff')), 
                 label=r'$\Delta $'+key,
                 color=colour_models(key))
        if (m_keys.index(key) < (len(m_keys)-2)) :
            graph_title=graph_title+key+", "
        elif m_keys.index(key)==(len(m_keys)-2):
            graph_title=graph_title+key+" & "
        else:
            graph_title=graph_title+key
    
    #calculates and adds title with frequency in MHz
    
    graph_title=graph_title+"-channels over time at %.2f MHz"%(min(merge_df.Freq)/1e6)    
    
    


    
    #plots the axis labels rotated so they're legible
    plt.xticks(rotation=90)

    plt.title(graph_title)
    plt.legend(frameon=False)
    plt.xlabel(gen_pretty_name('Time',units=True))
    
    #prints or saves the plot
    if modes['out_dir'] == None:
        plt.show()
    else:
        plt_file=prep_out_file(modes,plot="diff",dims="1d",
                               out_type=modes['image_type'])
        print("plotting: "+plt_file)
        plt.savefig(plt_file,bbox_inches='tight')
        plt.close()
    return(0)





def calc_fom_nd(merge_df, var_str, m_keys, modes,fom="rmse"):
    '''
    This function calculates a figure of merit between the scope and model 
    values for the specified channels  as they are distributed against another 
    column of the dataframe merge_df which is identified by var_str
    
    in current versions, useable values for var_str are "Time" and "Freq"
    in current versions, useable values for fom are "rmse" and "corr"
    '''

    print ("Calculating the "+gen_pretty_name(fom)+\
           " between observed and model data.")        
    #creates empty lists for the Errors
    n_foms=[]
    for i in range(len(m_keys)):
        n_foms.append([])
    
    
    
    #identifies allthe unique values of the variable in the column
    unique_vals=merge_df[var_str].unique()
    
    unique_vals=np.sort(unique_vals)
    
    #iterates over all unique values
    for unique_val in unique_vals:
        #creates a dataframe with  only the elements that match the current 
        #unique value
        unique_merge_df=merge_df[merge_df[var_str]==unique_val]
        #uses this unique value for and the 1-dimensional calc_fom_1d function
        #to calculate the Figure of merit for each channel
        n_fom=calc_fom_1d(unique_merge_df, m_keys, fom)
        
        #appends these to the list
        for i in range(len(m_keys)):
            n_foms[i].append(n_fom[i])
    
    #creates an overlaid plot of how the Figure of Merit  between model and scope
    #varies for each of the channels against var_str  
    print("Plotting the "+gen_pretty_name(fom)+\
            " between model and scope for "+\
          channel_maker(m_keys,modes,", ")+" against "+\
          gen_pretty_name(var_str))
    plt.figure()
    graph_title = "\n".join([modes['title'],"Plot of the "+gen_pretty_name(fom)+\
            " in "])
    for key in m_keys:    
        plt.plot(plottable(unique_vals, var_str),
                 n_foms[m_keys.index(key)],
                label=key+'_'+fom,
                color=colour_models(key))
        
        if (m_keys.index(key) < (len(m_keys)-2)) :
            graph_title=graph_title+key+", "
        elif m_keys.index(key)==(len(m_keys)-2):
            graph_title=graph_title+key+" & "
        else:
            graph_title=graph_title+key
    
    #calculates and adds title with frequency in MHz
    
    graph_title=graph_title+"-channels over "+gen_pretty_name(var_str)    
            
    plt.title(graph_title)


    #rotates the labels.  This is necessary for timestamps
    plt.xticks(rotation=90)
    plt.legend(frameon=False)
    plt.xlabel(gen_pretty_name(var_str, units=True))
    
    #prints or saves the plot
    if modes['out_dir'] == None:
        plt.show()
    else:
        #creates an output-friendly string for the channel
        str_channel = channel_maker(m_keys,modes)
        
        
        plt_file=prep_out_file(modes,plot=fom,ind_var=var_str,
                               channel=str_channel,
                               out_type=modes['image_type'])
        print("plotting: "+plt_file)
        plt.savefig(plt_file,bbox_inches='tight')
        plt.close()
    
    #returns the correlation lists if needed    
    return (n_foms)


def calc_fom_1d(merge_df, m_keys, fom):
    '''
    This function takes a merged dataframe as an argument and 
    calculates and returns the root mean square difference between scope and 
    model
    '''
    fom_outs=[]
    if fom == "rmse":
        for key in m_keys:
            fom_outs.append(np.mean(plottable(merge_df,(key+'_diff'))**2)**0.5)
    if fom == "corr":
        for key in m_keys:
            #uses absolute values as real values cannot be negative and complex 
            #values cannot be correlated
            model_vals=list(plottable(merge_df,(key+'_model')))
            scope_vals=list(plottable(merge_df,(key+'_scope')))
            corr=pearsonr(model_vals,scope_vals)[0]
            fom_outs.append(corr)
        #using [0] from the pearsonr to return the correlation coefficient, but not
        #the 2-tailed p-value stored in [1]
   
    return(fom_outs)
    
    
#def plot_diff_values_nf(merge_df, m_keys, modes):
#    '''
#    This function creates 3d colour plots using time and frequency from a 
#    merged data frame as the independent variables and the difference between
#    source and model as the dependent (colour) variable 
#    '''
#    source = "diff"
#    
#    time_delay = 1000.0/modes['frame_rate']
#    
#    if modes['three_d']=="colour":
#        for key in m_keys:
#            #create a plot 
#            plot_against_freq_time(merge_df, key, modes, source)
#    elif modes['three_d']=="anim":
#
#        animated_plot(merge_df, modes, 'Freq', m_keys, "Time", source, time_delay)
#                
#    elif modes['three_d']=="animf":
#
#        animated_plot(merge_df, modes, "d_Time", m_keys, 'Freq', source, time_delay)
#
#    else:
#        print("WARNING: No valid value for 3d plots")
#        plt.figure()
#        
#        #display main title and subplot title together
#        graph_title="\n".join([modes['title'],("Plot of the differences in %s\n over time and frequency"%key)])
#        plt.title(graph_title)
#        
#        #plots p-channel difference
#        plt.tripcolor(merge_df.d_Time,merge_df.Freq,plottable(merge_df[key+'_diff']),
#                      cmap=plt.get_cmap(colour_models(key+'_s')))
#        plt.colorbar()
#        #plots x-label for both using start time 
#        plt.xlabel("Time in seconds since start time\n"+str(min(merge_df.Time)))
#        plt.ylabel("Frequency")
#        #prints or saves the plot
#        if modes['out_dir'] == None:
#            plt.show()
#        else:
#            plt_file=prep_out_file(modes,plot="diff", dims="nd",
#                                   channel=key,
#                                   out_type="png")
#            print("plotting: "+plt_file)
#            plt.savefig(plt_file,bbox_inches='tight')
#        plt.close()



def plot_altaz_values_nf(merge_df, m_keys, modes):
    '''
    plots a series of altitude and azimuth based graphs 
    '''
#    directions=['alt','az_ew']
#    len_dir=len(directions)
    time_delay = 1000.0/modes['frame_rate']

    source_list = ['model','scope']
    
    alt_var ="alt"
    if 'ew' in modes['plots']:
        az_var = "az_ew"
    else:
        az_var = "az"
        
    if 'stn_alt' in merge_df and 'stn_az' in merge_df:
        az_var = "stn_"+az_var
        alt_var = "stn_"+alt_var
    
    for source in source_list:
        if modes["three_d"] == 'colour':
            #plots a 3-d plot against alt or az
            for key in m_keys:
                
                if "alt" in modes['plots']:
                    four_var_plot(merge_df,modes,alt_var,"Freq",key, az_var,
                                  source)

                    
                if "az" in modes['plots']:
                    four_var_plot(merge_df,modes,az_var,"Freq",key, alt_var,
                                  source)

    
    
        elif modes['three_d']=="anim":
    
            if "alt" in modes['plots']:
                animated_plot(merge_df, modes, 'Freq', m_keys, alt_var, source, 
                              time_delay, plot_name = alt_var)
            if "az" in modes['plots']:
                animated_plot(merge_df, modes, 'Freq', m_keys, az_var, source, 
                              time_delay, plot_name = az_var)

    
        elif modes['three_d']=="animf":
    
            if "alt" in modes['plots']:
                animated_plot(merge_df, modes, alt_var, m_keys, "Freq", source, 
                              time_delay, plot_name = alt_var)
            if "az" in modes['plots']:
                animated_plot(merge_df, modes, az_var, m_keys, "Freq", source, 
                              time_delay, plot_name = az_var)