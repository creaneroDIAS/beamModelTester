# Comparison Module
## Argument parsing function
**Version 1.0\
21st August 2018\
Oisin Creaner**

## Outline
This function parses the arguments from the command line and returns the 
file names for the model data and the scope data

Several options are provided: Positional arguments, followed by optional
arguments followed by interactive entry of the argument values.

*future expansions to arguments will allow the user to specify modes of 
operation and the type of output generated*

## Dependencies
argparse

## Outputs
A dictionary called modes containing the arguments parsed by the function

## Design Diagram
![Design Diagram](/images/comparison_module_parse_args_fig1_v2.PNG)


## Operations

1.  adds the optional argument -V or --verbose to set the verbosity of the output
2.  adds the optional argument -I or --interactive to set the interactivity level
2.  Creates a mutually exclusive group for model filenames
    1.  adds the positional argument model_p to that group
    2.  adds the optional argument -m or --model to that group
3.  Creates a mutually exclusive group for scope filenames
    1.  adds the positional argument scope_p to that group
    2.  adds the optional argument -s or --scope to that group

3.  adds the optional argument -o or --out_dir for the output
4.  adds the optional argument -t or --title for the graph 
(and output file) titles
5.  adds the optional argument -i or --image_type to set the file type for the output image files
6.  adds the optional argument -n or --norm for which mode 
to normalise the data in \
options: {t,f,n}
6.  adds the optional argument -N or --norm_data for which 
data to normalise \
options: {s,m,n,b}
7.  adds the optional argument -C or --crop_type which specifies 
what factor to crop upon\
options: {median,mean,percentile}
8.  adds the optional argument -c or --crop which specifies a 
number by which to carry out the crop
9.  adds the optional argument -k or --crop_basis which specifies 
whether to crop by frequency or overall or not at all\
options: {t,f,n}
10.  adds the optional argument -K or --crop_data for which set of data to crop\
options: {s,m,n,b}
11.  adds the optional argument -d or --diff to identify 
how to determine the difference between scope and model\
options: {sub,div,idiv}]
12.  adds the optional argument -v or --values to identify
which values to plot\
options: {"all","linear","stokes",\
          "xx","xy","yy","U","V","I","Q",\
          "each"}
13.  adds the optional argument -p or --plots to determine 
which graphs to show\
options: {"rmse", "corr", "spectra",\
         "file",\
         "alt","az","ew", "stn", "split",\
         "values","model","scope", "diff",\
         "overlay"}
14.  adds the optional argument -3 or --three_d to determine 
which values to plothow to plot 3-variable graphs
Options: {"colour","color", "anim", "animf","contour"}
14.  adds the optional argument -r or --frame_rate to determine the frame rate of animated outputs if any
15.  adds an optional argument -O or --offset for a time offset between model and scope
14.  Creates a mutually exclusive group for exclusion frequencies
     1.  adds the optional argument -f or --freq which specifies 1 or more frequencies at the command lines
     2.  adds the optional argument -F or --freq_file which specifies a file in which frequencies might be found
15.  adds an optional argument -O or --offset for a time offset between model and scope
14.  Creates a mutually exclusive group for target objects
     1.  adds the optional argument -X or --object_name to determine the target object by name
     2.  adds the optional argument -x or --object_coords to determine the target object by coordinates
14.  Creates a mutually exclusive group for observing location
     1.  adds the optional argument -L or --location_name to determine the observing location by name
     2.  adds the optional argument -l or --location_coords to determine the observing location by coordinates
15.  Retrieves the model file name
     1.  If the positional argument model_p was used, that is stored in the dictionary
     2.  Otherwise, if the optional argument -m or --model was used, 
    that is stored in a variable called in_file_model
     3.  Otherwise, the user is prompted to enter the filename and
    that is stored in a variable called in_file_model
16.  Retrieves the scope file name
     1.  If the positional argument scope_p was used, that is stored in a 
    variable called in_file_scope
     2.  Otherwise, if the optional argument -s or --scope was used, 
    that is stored in a variable called in_file_scope
     3.  Otherwise, the user is prompted to enter the filename and
    that is stored in a variable called in_file_scope
17.  Returns the dictionary mode

## Usage and arguments
This function is only used as part of the comparison module. Detailed usage notes at [this link for command line](/comparison_module/cli_arguments.md) and [this link for interactive use](/comparison_module/interactive_mode.md)

