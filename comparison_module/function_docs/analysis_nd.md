# Comparison Module 
**multi dimensional analysis functions\
Version 1.0\
5ᵗʰ October 2018\
Oisin Creaner**

This set of functions describes the multi-dimensional analysis elements of the 
[comparison module](/comparison_module/Comparison_Module.md).

## Functions
plot_diff_values_nf\
calc_corr_1d\
calc_rmse_1d\
calc_corr_nd\
calc_rmse_nd

## Dependencies
pandas\
numpy\
matplotlib.pyplot\
scipy.stats.stats.pearsonr

## Inputs
A merged data frame containing model and scope data\
Modes control dictionary\
list of channels\
list of sources (model, scope, difference) to plot

## Outputs
*All outputs are optional based on user input contained in the modes dictionary*
[Link to non-exhaustive sample outputs](/comparison_module/outputs.md#MultiFreq)
All of these outputs are optional as controlled by the modes dictionary
1.  A plot or animation of the values of each of the channels for model and scope and the difference between them over time
2.  A plot or animation of the values of each of the channels for model and scope and the difference between them over Altitude and/or Azimuth
3.  A plot or animation of the values of each of the figures of merit for each channel (currently: Correlation and RMSE) over time and frequency
4.  A calculation of a set of figures of merit for each channel (currently: Correlation and RMSE)
    
    
## Outline
These functions form the multi-dimensional analysis elements of the 
[comparison module](/comparison_module/Comparison_Module.md) of 
[beamModelTester](/README.md)
This element produces outputs for each polarisation for which there is a difference
recorded in the input.  

## Design Diagram
![Design diagram](/images/comparison_module_analysis_nf_fig1_v3.PNG)

## Operation
1.  If "spectra" is set in plots
    1.  calls plot_spectra_nf to plot the variation of the sources against frequency and time
        1.  If the 3-d mode is set to colour or contour, calls plot_3d_graph with time on the x-axis and frequency on the y-axis
        2.  If the 3-d mode is set to anim, calls plot_3d_graph with time on the t-axis and frequency on the x-axis
        3.  If the 3-d mode is set to animf, calls plot_3d_graph with time on the x-axis and frequency on the t-axis
2.  If "alt" or "az" are set in plots 
    1.  if Alt/az coordinates have been calculated, calls plot_altaz_values_nf to plot the variation of the sources against frequency and Altitude or Azimuth
        1.  Calls get_alt_az_var to identify the correct variables for altitude and azimuth
        2.  adds the Alt and Az parameters from the modes directory to a list of variables to plot as the x-axes and corresponding variables to act as y-axes
        3.  Splits the Alt and Az x-axis parameters and the dataframe between East and West, North and South if requested using split_df
        4.  For each of the x-axis sets,
            1.  If the 3-d mode is set to colour:
                1.  For each source
                    1.  For each channel
                        1.  For each split (East/West, North/South) if requested
                            1.  Calls four_var_plot with 
                                1.  the split data frame as  in_df
                                2.  the modes dictionary
                                3.  the altitude/azimuth variable as var_x
                                4.  Frequency as var_y
                                5.  the channel as var_z
                                6.  The counterpart to the alt/azimuth variable as var_y2
                                7.  The source as source
                                8.  The name of the split (E/W/N/S) as plot_name
            2.  If the 3-d mode is set to anim, calls plot_3d_graph with alt/az variable on the t-axis and frequency on the x-axis
            3.  If the 3-d mode is set to animf, calls plot_3d_graph with alt/az variable on the x-axis and frequency on the t-axis
    2.  Otherwise returns an error
3.  If a difference has been calculated (i.e. there are two inputs to compare)
    1.  if "corr" is to be plotted, adds it to the list of figures of merit
    2.  if "rmse" is to be plotted, adds it to the list of figures of merit
    3.  for each figure of merit (fom) to be plotted
        1.  calls plot_fom_vs_ind to plot the variation of the FoM against frequency and time
        2.  Calculates the list of values for that figure of merit using calc_fom_1d
        3.  for each channel
            1.  prints the value for the figure of merit
            2.  if output file generation is set by inputting an out_dir
                1.  Creates a file name using [prep_out_file](comparison_module/prep_out_file.md)
                2.  Saves the value for the figure of merit to an output file
4.  If there is an output directory set, outputs the dataframes from the dictionary to files
5.  returns ind_dfs
 

