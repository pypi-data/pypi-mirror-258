import os
import glob
import colorama as ca
from pylipd.lipd import LiPD
import xarray as xr
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import cftime


def p_header(text):
    # return cprint(text, 'cyan', attrs=['bold'])  # lib: termcolor
    print(ca.Fore.CYAN + ca.Style.BRIGHT + text)
    print(ca.Style.RESET_ALL, end='')

def p_hint(text):
    # return cprint(text, 'grey', attrs=['bold'])  # lib: termcolor
    print(ca.Fore.LIGHTBLACK_EX + ca.Style.BRIGHT + text)
    print(ca.Style.RESET_ALL, end='')

def p_success(text):
    # return cprint(text, 'green', attrs=['bold'])  # lib: termcolor
    print(ca.Fore.GREEN + ca.Style.BRIGHT + text)
    print(ca.Style.RESET_ALL, end='')

def p_fail(text):
    # return cprint(text, 'red', attrs=['bold'])  # lib: termcolor
    print(ca.Fore.RED + ca.Style.BRIGHT + text)
    print(ca.Style.RESET_ALL, end='')

def p_warning(text):
    # return cprint(text, 'yellow', attrs=['bold'])  # lib: termcolor
    print(ca.Fore.YELLOW + ca.Style.BRIGHT + text)
    print(ca.Style.RESET_ALL, end='')

def load_lipd(dirpath):
    lipd = LiPD()
    paths = glob.glob(os.path.join(dirpath, '*.lpd'))  
    lipd.load(paths)
    ts_list, df = lipd.get_timeseries(lipd.get_all_dataset_names(), to_dataframe=True)
    return df

def gcd(lat1, lon1, lat2, lon2):
	'''
	Calculate the great circle distance between two points
	on the earth (specified in decimal degrees)

	Parameters:
	-----------
	lat1: float
		Latitude of first location (degrees)
	lon1: float
		Longitude of first location (degrees)
	lat2: float
		Latitude of second location (degrees)
	lon2: float
		Longitude of second location (degrees)
		
	Returns:
	--------
	km: float
		Great circle distance between the two locations (in kilometers)
	'''
	# convert decimal degrees to radians
	lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

	# haversine formula
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
	c = 2 * np.arcsin(np.sqrt(a))

	# 6367 km is the radius of the Earth
	km = 6367 * c
	return km

def year_float2datetime(year_float, resolution='month'):
    ''' Convert an array of floats in unit of year to a datetime time; accuracy: one day
    '''
    # if np.min(year_float) < 0:
    #     raise ValueError('Cannot handel negative years. Please truncate first.')

    year = np.array([int(y) for y in year_float], dtype=int)
    month = np.zeros(np.size(year), dtype=int)
    day = np.zeros(np.size(year), dtype=int)

    for i, y in enumerate(year):
        fst_day = datetime(year=y, month=1, day=1)
        lst_day = datetime(year=y+1, month=1, day=1)
        year_length = lst_day - fst_day

        year_part = (year_float[i] - y)*year_length + timedelta(minutes=1)  # to fix the numerical error
        date = year_part + fst_day
        month[i] = date.month
        day[i] = date.day

    if resolution == 'day':
        time = [cftime.datetime(y, m, d, 0, 0, 0, 0, 0, 0, calendar='standard') for y, m, d in zip(year, month, day)]
    elif resolution == 'month':
        time = [cftime.datetime(y, m, 1, 0, 0, 0, 0, 0, 0, calendar='standard') for y, m in zip(year, month)]

    return time