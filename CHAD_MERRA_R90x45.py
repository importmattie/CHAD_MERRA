
# coding: utf-8

# ## Clickable Histogram of Atmospheric Data (CHAD)
# ### *(Clickable Histogram (ClickHist) + Atmospheric Data Input)*
# 
# Author: [Mattie Niznik](http://importmattie.github.io) ([mattie.niznik@princeton.edu](mailto:mattie.niznik@princeton.edu))<br>
# Post-Doctoral Associate,
# [RSMAS](http://rsmas.miami.edu/),
# [University of Miami](http://welcome.miami.edu/)
# 
# For more information, see:<br>
# https://github.com/importmattie/ClickHist/wiki<br>

# # Let's get started.
# ## (1) Setting Input/Output Files
# ## First, you need to chose the *template* bundle.
# ### This is an IDV bundle with your desired data and displays that ClickHist will alter to focus on the time and location relevant to scatter points you select.
# **Note:** The first bundle in both lists here will be the one referenced in the later script that generates images, movies, and a .zidv file. It should probably be the "full" bundle with the variables you want to study.

# In[ ]:

bundleInFilenames = ['ClickHist_merraTrmmIR_simple']
bundleOutTags = ['simple']


# ## Now, pick a Tag for this session's *Case Notebooks*.
# #### This is a notebook that will be generated separately from this one containing snapshots of ClickHists and other images related to each case you select.
# This way, without much extra effort you can remember what you were working on!

# In[ ]:

caseNotebookFilename = 'Session1'


# ## (2) Set the variables, data sources, and other necessary information.
# ### What geographic subset are you interested in exploring?
# 
# Longitude: 0 through 360 (Degrees East)<br>
# Latitude: -90 through 90 (Degrees North)<br>

# In[ ]:

lonLow = -160.
lonHigh = -120.
latLow = -25.0
latHigh = 15.0


# In[ ]:

urlToLoad = ('http://weather.rsmas.miami.edu/repository/opendap/synth:5ca43f0f-38f6-41e7-b66b-a8f8f593df6a:L01FUlJBX1RSTU0zQjQyXzJkZWdfMTk5OC0yMDEzX3ByZWN0b3RfcnIubmM=/entry.das')


# ### Now let's get some information on the variables you want
# 
# **For this data, we've preprogrammed all of the units and data into a module so you just have to pick from a list of options (case sensitive):**<br>
# Precip_MERRA, Precip_TRMM

# In[ ]:

var1Name = 'Precip_MERRA'
var2Name = 'Precip_TRMM'


# ### Set how large you want the IDV bundle to be in space and time
# #### Each of these is calculated as distance from center, so `lonOffset = 1.0` means 2.0° of longitude.
# #### `dtFromCenter` needs to be in seconds

# In[ ]:

lonOffset = 10.0
latOffset = 10.0
dtFromCenter = 73*3600


# ### Would you like specific quantiles indicated in X and Y?
# **If so, specify them here.**

# In[ ]:

quantiles = [0.01,0.1,1,5,95,99,99.9,99.99]


# ### Import the necessary modules needed for CHAD to work

# *Currently supported graphics backends are Qt4Agg ('qt4') and TK ('tk')*

# In[ ]:

#%matplotlib tk
get_ipython().magic(u'matplotlib qt4')
import matplotlib
#matplotlib.use('TkAgg')
#matplotlib.use('Qt4Agg')

from IPython.display import clear_output
import netCDF4
import sys

import ClickHist_MERRA as ClickHist
import ClickHistDo_MERRA as ClickHistDo
import loadmod_MERRA


# #### This call is necessary to make sure the output displays properly
# 
# (If interested in the details, see: http://bit.ly/1SsishU)

# In[ ]:

oldsysstdout = sys.stdout
sys.stdout = loadmod_MERRA.flushfile(sys.stdout)


# #### The following (less often edited) items are set to default values in the module `loadmod_MERRA`
# 
# (You can change them in the module if desired, but they are left out here to save space. For "advanced" users.)

# In[ ]:

lonValueName = loadmod_MERRA.lonValueName
latValueName = loadmod_MERRA.latValueName
timeValueName = loadmod_MERRA.timeValueName
startDatetime = loadmod_MERRA.startDatetime

var1Edges = loadmod_MERRA.binOptions[var1Name]
var2Edges = loadmod_MERRA.binOptions[var2Name]

var1FmtStr = loadmod_MERRA.fmtStrOptions[var1Name]
var2FmtStr = loadmod_MERRA.fmtStrOptions[var2Name]

var1ValueName = loadmod_MERRA.valueNameOptions[var1Name]
var2ValueName = loadmod_MERRA.valueNameOptions[var2Name]

var1Units = loadmod_MERRA.varUnitOptions[var1Name]
var2Units = loadmod_MERRA.varUnitOptions[var2Name]
metadata_UD = (var1Name+' vs '+var2Name+': '+
               str(lonLow)+' to '+str(lonHigh)+' E, '+
               str(latLow)+' to '+str(latHigh)+' N')

var1ValueMult = loadmod_MERRA.varMultOptions[var1Name]
var2ValueMult = loadmod_MERRA.varMultOptions[var2Name]


# ## (3) Load the Data
# 
# **N.B.** CHAD currently expects the 3-D variables to be in the Python format `variable[times,latitudes,longitudes]`.<br>
# If this is not the default, you will have to either permute the data below or preprocess the data so that it matches this format.

# In[ ]:

cdfIn = netCDF4.Dataset(urlToLoad,'r')


# In[ ]:

lonValues = cdfIn.variables[lonValueName][:]
latValues = cdfIn.variables[latValueName][:]
timeValues = cdfIn.variables[timeValueName][:]*loadmod_MERRA.timeValueMult


# #### By finding the needed index ranges here, we can load a subset of the data over the web instead of loading it all and subsetting later.

# In[ ]:

lowLonInt,highLonInt = loadmod_MERRA.getIntEdges(lonValues,lonLow,lonHigh)
lowLatInt,highLatInt = loadmod_MERRA.getIntEdges(latValues,latLow,latHigh)


# *Based on the data chunk you're accessing, the variable load may take some time.*

# In[ ]:

var1Values = cdfIn.variables[var1ValueName][:,
                                            lowLatInt:highLatInt+1,
                                            lowLonInt:highLonInt+1]*\
                                            var1ValueMult
var2Values = cdfIn.variables[var2ValueName][:,
                                            lowLatInt:highLatInt+1,
                                            lowLonInt:highLonInt+1]*\
                                            var2ValueMult


# *(We now subset the longitudes and latitudes since the previous call to getIntEdges needed the full lon/lat.)*

# In[ ]:

lonValues = lonValues[lowLonInt:highLonInt+1]
latValues = latValues[lowLatInt:highLatInt+1]


# In[ ]:

cdfIn.close()


# ## (4) Create ClickHist and ClickHistDo Instances

# ### Initialize 'ClickHistDo'

# In[ ]:

ClickHistDo1 = ClickHistDo.ClickHistDo(lonValues,latValues,
                                       timeValues,startDatetime,
                                       bundleInFilenames,
                                       bundleOutTags,
                                       caseNotebookFilename,
                                       xVarName=var1Name,
                                       yVarName=var2Name,
                                       lonOffset=lonOffset,
                                       latOffset=latOffset,
                                       dtFromCenter=dtFromCenter)


# ### Initialize 'ClickHist' and launch!

# If you want the output of CHAD to be in a separate window, make sure `%qtconsole` below is not commented. Otherwise, the text output will appear below the last cell.

# In[ ]:

#%qtconsole
ClickHist1 = ClickHist.ClickHist(var1Edges,var2Edges,
                                 var1Values,var2Values,
                                 xVarName=var1Name,yVarName=var2Name,
                                 xUnits=var1Units,yUnits=var2Units,
                                 xFmtStr=var1FmtStr,
                                 yFmtStr=var2FmtStr,
                                 maxPlottedInBin=loadmod_MERRA.maxPlottedInBin_UD,
                                 quantiles=quantiles,
                                 metadata=metadata_UD)
ClickHist1.setDo(ClickHistDo1)
ClickHist1.showPlot()


# In[ ]:



