# Offsets and Scaling
In this tutorial, you will learn how to combine data from different sources with the same cadence by applying a time offset, and adjust the data scales to allow for different representations of the variation of the data.

## Time Offset
Time offsets are used to compare data from different sources with the same observation cadence taken at a different times.  These can be used for several purposes, for example, to observe changes over longer timescales, compare observations of different sources or, as we'll be doing here, comparing observations from different stations.

To this end, in addition to [the data you have previously used](https://zenodo.org/record/1744987#.XAEbpdv7SUk) for these tutorials, you should **[download this new data](https://zenodo.org/record/2650313#.XMCcnEMo8UE)**.  Both datasets represent observations of CasA taken from LOFAR HBA stations on 16th-17th March 2018, the first from station SE607 in Onsala, Sweden, and the second from IE613 in Birr, Ireland.  These observations were taken concurrently from the two stations, but a slight offset in start time means the two observations would not match perfectly for comparison purposes.  Thus, a slight offset must be provided to enable the data to be matched.

Start the program as usual.  Now, instead of selecting a CSV file as the model and a HDF5 file as the "scope" or observation, we'll select the HDF5 file from SE607 as the model, and the HDF5 file from IE613 as the scope file.  If you try to plot the data, you'll get an error as shown below.

![Error with unmatched data](/images/tutorial_7_1.png)

From the filenames, it can be seen that the two observations started at 11:49:21 and 15:58:25 (both are in UTC by convention). The source data is recorded at a cadence of one data point every 519 seconds (see [iLiSA](https://github.com/2baOrNot2ba/iLiSA) for more information).  Therefore to apply the correct offset, it is necessary to first find out the difference in time between the start of the two observations.  This can be calculated to be 14,944 seconds.  By taking the modulus of this mumber by 519, it can be calculated that the offset between the datasets is 412 seconds.  Since this is more than half way through an observation window, it would be more correct to apply an offset in the other direction, i.e. an offset of (519-412) 107 seconds.  Note that the offset is applied by subtracting the specified amount from the time of the scope data so when using this for yourself, you may need to be careful about the sign of the offset chosen.  In this case, the offset will be positive.

To apply this offset, go to the "Other Options" menu and select "Set Offset" to bring up the offset menu

![misc menu](/images/interactive_snips/gicm_8_misc_menu.PNG)

From the offset menu, enter 107 and click to confirm.

![Offset menu](/images/interactive_snips/gicm_8_1_misc_offset_menu.PNG)

Then return to the main menu.  Using what you learned in previous tutorials, generate a plot of the [difference](/tutorial_2.md#differences) in [Stokes I](/tutorial_2.md#variables) between the IE613 (scope) and SE607 (model) observations using the [filtered frequency list](/tutorial_3.md#file) with both sets of data [normalised by frequency](/tutorial_1.md#normalisation).  You should end up with a plot like the one that can be seen below.

<img src="/images/tutorial_7_2.png" width=400>

From this plot, you can see a series of horizontal lines in the data reflecting RFI sources which have been folded into the normalisation.  This is because our frequency filter was built for SE607 alone, and does not account for the RFI environment of IE613.  To mitigate this, download [this file](https://zenodo.org/record/2653769), and replace the frequency filter with it.  You will then see a clearer plot of the differences between the two stations as shown below.

<img src="/images/tutorial_7_3.png" width=400>

## Logarithmic Scales

It may be necessary on occasion to use logarithmic plots to illustrate data with a large dynamic range.  To this end, logarithmic plots may be used to allow for the data to be seen at high and low values.  To activate log plotting, navigate once again to the "other options" menu, and this time toggle the option from linear to logarithmic plotting.  Plot with these options and you will generate the plot as shown below.

<img src="/images/tutorial_7_4.png" width=400>

## Percentage Scales
To activate percentage plotting, navigate once again to the "other options" menu, but this time toggle the option from raw data to percentage plotting.  Plot with these options and you will generate the plot as shown below.

<img src="/images/tutorial_7_5.png" width=400>

In [Tutorial 8](/tutorial_8.md), we will look at visual options, such as changes to the colourschemes and plot sizes.
