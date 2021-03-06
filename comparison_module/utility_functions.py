# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 13:08:14 2018

@author: User
"""

def plottable(in_series, col_name=""):
    '''
    produces plot and print friendly versions of variables
    '''
    if col_name == "":
        #if it is a single series, tides up the complex components
        out_series = clean_complex(in_series)
    elif col_name == "Freq":
        if str(type(in_series))=="<class 'pandas.core.frame.DataFrame'>":
            out_series = in_series[col_name]/1e6
        else:
            out_series = in_series/1e6
    else:
        if str(type(in_series))=="<class 'pandas.core.frame.DataFrame'>":
            out_series = clean_complex(in_series[col_name])
        else:
            out_series = clean_complex(in_series)
    return(out_series)

def clean_complex(in_series):
    '''
    turns a complex series into a series of absolute values, but just returns a
    real number
    '''    
    try:
        out_series=in_series.reset_index(drop=True)
    except AttributeError: #if reset index doesn't work
        out_series=in_series
    if len(out_series)>0:
        if 'complex' in str(type(out_series[0])):
            out_series =  abs(in_series)
        else:
            out_series =  in_series
    else:
        out_series = abs(in_series)
    return (out_series)
    
def get_source_separator(source):
    if source == "":
        sep = ""
    else:
        sep = "_"
    return (sep)

def get_df_keys(merge_df, modes={"values":"all"}):
    '''
    Calculates the keys from a given dataframe or based on the input modes.
    '''
    if modes['verbose'] >=2:
        print("Identifying channels to analyse")
    m_keys=[]
    
    #if key groups have been supplied, extend the keylist with their components
    if "all" in modes["values"]:
        m_keys.extend(["xx","xy","yy","U","V","I","Q"])
    else:
        if "stokes" in modes["values"]:
            m_keys.extend(["U","V","I","Q"])
        if "linear" in modes["values"]:
            m_keys.extend(["xx","xy","yy"])
       
        #if keys have been supplied individually                
        if "xx" in modes["values"]:
            m_keys.append("xx")
        if "xy" in modes["values"]:
            m_keys.append("xy")
        if "yy" in modes["values"]:
            m_keys.append("yy")
        if "U" in modes["values"]:
            m_keys.append("U")
        if "V" in modes["values"]:
            m_keys.append("V")
        if "I" in modes["values"]:
            m_keys.append("I")
        if "Q" in modes["values"]:
            m_keys.append("Q")
    
    
    #if the keys are still blank
    if m_keys == []:
        if modes['verbose'] >=1:
            print ("Warning, no appropriate keys found!")
    
    
    return(m_keys)

def split_df(merge_df, modes, splitter):
    '''
    This function splits a dataframe into eastern and western or northern and
    southern halves to prevent aliasing of data in various plots.
    
    Returns a list of dataframes and a list of strings identifying those DFs
    '''
    alt_var,az_var,az_var_ew = get_alt_az_var(merge_df, modes)  
    out_list = []
    out_names = []
    
    #if a split has been requested and the variable is suitable to split
    if "split" in modes['plots'] and splitter in [alt_var,az_var,az_var_ew]:
        if modes['verbose'] >=2:
            print("Splitting the dataframe")
            
        #if splitting for altitude, splits into East and West
        if alt_var ==splitter:
            #identifies the southernmost point
            south_point = min(merge_df[alt_var])
            #identifies the azimuth of that point
            south_point_az =min(merge_df.loc[merge_df[alt_var]==south_point,az_var_ew])
            
            #creates dataframes which include the points east and west of the southern most point
            east_half=merge_df.loc[merge_df[az_var_ew]>=south_point_az].reset_index(drop=True)#east half
            west_half=merge_df.loc[merge_df[az_var_ew]<south_point_az].reset_index(drop=True)#west_half
            out_list.extend([east_half,west_half])
            out_names.extend(["East","West"])
        
        #if splitting for azimuth, splits into North and South
        elif splitter in [az_var,az_var_ew]:
            #identifies the Easternmost point
            east_point = max(merge_df[az_var_ew])
            #identifies the altitude of that point
            east_point_alt =max(merge_df.loc[merge_df[az_var_ew]==east_point,alt_var])
            
            #creates dataframes which include the points North and South of the eastern most point
            north_half=merge_df.loc[merge_df[alt_var]>=east_point_alt].reset_index(drop=True)
            south_half=merge_df.loc[merge_df[alt_var]<east_point_alt].reset_index(drop=True)
            out_list.extend([north_half,south_half])
            out_names.extend(["North","South"])

    else:
        #otherwise returns a 1-long list including the original dataframe
        out_list.extend([merge_df])
        out_names.extend([""])
    return(out_list,out_names)
    
def get_alt_az_var(merge_df, modes):
    alt_var ="alt"
    az_var = "az"
    az_var_ew ="az_ew" #for when East-west is 100% needed
    if 'ew' in modes['plots']:
        az_var = az_var_ew

        
        
    if ('stn' in modes['plots'] and
        'stn_alt' in merge_df and 
        'stn_az' in merge_df):
        az_var = "stn_"+az_var
        alt_var = "stn_"+alt_var
    return(alt_var, az_var, az_var_ew)