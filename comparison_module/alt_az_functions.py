# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 10:03:28 2018

@author: User
"""

###############################################################################
#
#coordinate setting functions
#    
###############################################################################

try:
    from astropy.coordinates import EarthLocation,SkyCoord
    from astropy.time import Time
    from astropy import units as u
    from astropy.coordinates import AltAz
except ImportError:
    print("WARNING: Unable to import astropy.\n"\
          "This may cause subsequent modules to fail")
    
try:
    import casacore.measures
    import casacore.quanta.quantity

except ImportError:
    print("WARNING: Unable to import casacore.\n"\
          "This may cause subsequent modules to fail")
    
try:    
    import ilisa.antennameta.antennafieldlib as antennafieldlib

except ImportError:
    print("WARNING: unable to import ilisa.\n"\
          "This may cause subsequent modules to fail")


    
def set_object_coords(name_str="", modes):
    '''
    returns a 2-long list of the coordinates of an object identified by name
    Want to replace this with something better at a later point, but this is 
    designed as a module to be replaced.
    '''
    coords=[0.0,0.0]
    if name_str == "CasA":
        coords=[350.85,  58.815]
    elif name_str == "CygA":
        coords=[299.86791667,  40.73388889]
    elif name_str == "VirA":
        coords=[187.70415,  12.39111]
    else:
        if modes['verbose'] >=1:
            print("Warning: Object: "+name_str+" not found.  Setting object "+
              "coordinates to 0,0 which will disable object tracking./n/n" + 
              "for an object at exactly 0,0 set one coordinate to 1e-308")
    #minimum float increment coordinates will not affect the actual results
    #due to precision limits but will pass a =!0 test later in the program
    
    return(coords)
    
def set_location_coords(name_str="", modes):
    '''
    returns a 2-long list of the coordinates of an observing location 
    identified by name.
    Want to replace this with something better at a later point, but this is 
    designed as a module to be replaced.
    '''
    coords=[0.0,0.0,0.0]
    if name_str == "IE613": 
        coords=[53.095263, -7.922245,150.0] #coords for LBA.  HBA almost identical
    elif name_str == "SE607":
        coords=[57.398743, 11.929636, 20.0]
    else:
        if modes['verbose'] >=1:
            print("Warning: Site: "+name_str+" not found.  Setting site "+
              "coordinates to 0,0,0 which will disable object tracking./n/n" )    
        #there is no land at lat/long (0,0), so it should be ok to assume no
        #observations at this location
    return(coords)











def calc_alt_az(merge_df,modes):
    '''
    This function uses astropy to calculate a set of altitude and azimuth 
    coordinates for the target object at each time in the the dataset
    '''
    if modes['verbose'] >=2:
        print("Calculating Horizontal Coordinates")
    observing_location = EarthLocation(lat= modes['location_coords'][0],
                                       lon= modes['location_coords'][1],
                                       height =modes['location_coords'][2]*u.m)
    
    coord = SkyCoord(modes['object_coords'][0],
                     modes['object_coords'][1], 
                     unit='deg')
    
    time_set = Time(list(merge_df.Time))
    aa_set= AltAz(location=observing_location, obstime=time_set)
    coord_set=coord.transform_to(aa_set)
    
    merge_df['alt'] = coord_set.alt
    merge_df['az'] = coord_set.az
    
    merge_df['az_ew'] = coord_set.az
    if modes['verbose'] >=2:
        print("Calculating East/West Horizontal Coordinates")
    (merge_df.loc[merge_df['az']>180,'az_ew'])=(merge_df.loc[merge_df['az']>180,'az'])-360
    return (merge_df)

def calc_alt_az_lofar(merge_df,modes):
    '''
    This function is not currently defined.  This placeholder will be used to 
    define the function to calculate LOFAR specific coordinates
    '''
    if modes['verbose'] >=2:
        print("Calculating LOFAR Coordinates")
    stn_id=modes['location_name']
    stn_alt_az=horizon_to_station(stn_id, merge_df.az, merge_df.alt)
    
    merge_df['stn_alt']=np.array(stn_alt_az[1])
    merge_df['stn_az_ew']=np.array(stn_alt_az[0])
    merge_df['stn_az']=merge_df['stn_az_ew']
    (merge_df.loc[merge_df['stn_az_ew']<0,'stn_az'])=(merge_df.loc[merge_df['stn_az_ew']<0,'stn_az_ew'])+360
    return (merge_df)

def horizon_to_station(stnid, refAz, refEl):
    # Algorithm does not depend on time but need it for casacore call.
    obstimestamp = "2000-01-01T12:00:00" 


    obsstate = casacore.measures.measures()
    when = obsstate.epoch("UTC", obstimestamp)
    # Use antennafieldlib to get station position and rotation
    # (using HBA here but it shouldn't matter much if it were LBA)
    stnPos, stnRot, arrcfgpos_ITRF, stnIntilePos = \
                         antennafieldlib.getArrayBandParams(stnid, 'HBA')

    # Convert from ITRF to LOFAR station coordsys
    #arrcfgpos_stncrd = stnRot.T * arrcfgpos_ITRF.T
    pos_ITRF_X = str(stnPos[0,0])+'m'
    pos_ITRF_Y = str(stnPos[1,0])+'m'
    pos_ITRF_Z = str(stnPos[2,0])+'m'
    where = obsstate.position("ITRF", pos_ITRF_X, pos_ITRF_Y, pos_ITRF_Z)
    
    
    
    obsstate.doframe(where)
    obsstate.doframe(when)
    
    # Set Horizontal AZEL (not really necessary since request is already in
    # coordinate system, but acts as a check)
#    whatconv=obsstate.measure(what,'AZEL')
#    az = whatconv['m0']['value']
#    el = whatconv['m1']['value']
#    print "Horizontal coord. AZ, EL: {}deg, {}deg".format(numpy.rad2deg(az),
#                                                          numpy.rad2deg(el))
    az_stn=[]
    el_stn=[]
    for i in range(len(refAz)):
        refAz_i = np.deg2rad(float(refAz[i]))
        refEl_i = np.deg2rad(float(refEl[i]))
        what = obsstate.direction("AZEL", str(refAz_i)+"rad", str(refEl_i)+"rad")
        # Convert to Station Coordinate system.
        # First convert to ITRF
        whatconvITRF=obsstate.measure(what,'ITRF')
        lonITRF = whatconvITRF['m0']['value']
        latITRF = whatconvITRF['m1']['value']
        # then turn it into a vector
        xITRF = np.cos(lonITRF)*np.cos(latITRF)
        yITRF = np.sin(lonITRF)*np.cos(latITRF)
        zITRF = np.sin(latITRF)
        xyzITRF = np.matrix([[xITRF],[yITRF],[zITRF]])
        # then rotate it using station's rotation matrix
        what_stn = stnRot.T * xyzITRF
        l_stn=what_stn[0,0]
        m_stn=what_stn[1,0]
        n_stn=what_stn[2,0]
        # now convert vector in station local coordinate system to az/el
        az_stn.append(np.rad2deg(np.arctan2(l_stn,m_stn)))
        el_stn.append(np.rad2deg(np.arcsin(n_stn)))
    
    return(az_stn, el_stn)
