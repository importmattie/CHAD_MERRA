import datetime
import numpy as np

# These values are editable but hidden here to make the notebooks cleaner

# Figure dimensions in pixels
figureXSize = 800
figureYSize = 800
figDPI = 150
# Maximum number of points plotted in each bin
# Keep this low for faster performance
maxPlottedInBin_UD = 1000

# Easy default values for each variable

# Formatting for Output
# Basic Help: The number after the decimal point sets the number of
# decimal points shown in output
# For more on Python string formatting, see:
# (https://mkaz.github.io/2012/10/10/python-string-format/)
# These are OPTIONAL inputs to ClickHist: xFmtStr=?,yFmtStr=?)
fmtStrOptions = {'Precip_MERRA': "{:3.0f}", 'Precip_TRMM': "{:3.0f}"}

# These are the variable names in the loaded data files
valueNameOptions = {'Precip_MERRA': 'prectot', 'Precip_TRMM': 'rr'}

binOptions = {'Precip_MERRA': np.array([0., 1., 11., 21., 31., 41., 51.,
                                        61., 71., 81., 91., 101., 250.]),
              'Precip_TRMM': np.array([0., 1., 11., 21., 31., 41., 51.,
                                       61., 71., 81., 91., 101., 250.])}

varUnitOptions = {'Precip_MERRA': 'mm day-1', 'Precip_TRMM': 'mm day-1'}

# If you are converting to units different from those in the input files,
# you can set a conversion factor here
varMultOptions = {'Precip_MERRA': 86400., 'Precip_TRMM': 24.}

# These values are tied to the current data files in the loaders. If you change
# the data files, you will likely have to change many of these values

lonValueName = 'lon'
latValueName = 'lat'
timeValueName = 'time'

# Note: In future versions, this may be implemented manually
# (i.e. CHAD queries the data for what units 'time' is in)
timeValueMult = 3600.
timeValueOffset = 0

startYear = 1998
startMonth = 1
startDay = 1
startHour = 12
startMinute = 0
startSecond = 0

startDatetime = datetime.datetime(startYear, startMonth, startDay,
                                  startHour, startMinute, startSecond)

# Functions and classes that are useful in the notebook


class flushfile():

    def __init__(self, f):
        self.f = f

    def __getattr__(self,name):
        return object.__getattribute__(self.f, name)

    def write(self, x):
        self.f.write(x)
        self.f.flush()

    def flush(self):
        self.f.flush()


def getIntEdges(dim, low, high):
    lowInt = np.argmin(abs(dim-low))
    highInt = np.argmin(abs(dim-high))
    return lowInt, highInt
