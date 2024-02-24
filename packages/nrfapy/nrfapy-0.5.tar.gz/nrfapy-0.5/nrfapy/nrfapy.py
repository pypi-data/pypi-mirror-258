"""Main module."""

from __future__ import absolute_import, division, print_function, unicode_literals

import urllib.request
import json
import pandas as pd
import pkg_resources

# The base URL to access the nrfa API
BASE_URL = "https://nrfaapps.ceh.ac.uk/nrfa/ws"

VALID_DATA_TYPES = [
    'gdf', 'ndf', 'gmf', 'nmf', 'cdr', 'cdr-d', 'cmr',
    'pot-stage', 'pot-flow', 'gauging-stage', 'gauging-flow',
    'amax-stage', 'amax-flow'
]


def catalogue():
    """
    This gets the data catalog from nrfa an returns it as a pandas dataframe
    You can use this dataframe to get station characteristics
    

	Returns:
		pandas Dataframe containing the National River Flow Archive catalog, which has metadata about all stations

	Author: Simon Moulds
	Date: 20/01/2024
	"""
    
    query = "station=*&format=json-object&fields=all"
    stations_info_url = "{BASE}/station-info?{QUERY}".format(
        BASE=BASE_URL, QUERY=query
    )

    # Send request and read response
    response = urllib.request.urlopen(stations_info_url).read()

    # Decode from JSON to Python dictionary
    response = json.loads(response)
    df = pd.DataFrame(response['data'])
    return df


def _build_ts(response, date_index):
    """
    This is used to parse timeseries data from the nrfa
    
    Args:
        response (json):  this is a json that is parsed from a bitstream provided by the nrfa API

	Returns:
		pandas Dataframe containing the requested dataset

	Author: Simon Moulds
	Date: 20/01/2024
	"""
    variable = response['data-type']['id']
    dates = response['data-stream'][0::2]
    values = response['data-stream'][1::2]
    df = pd.DataFrame.from_dict({'time': dates, variable: values})

    try:
        # Get the version of pandas
        pandas_version = pkg_resources.get_distribution("pandas").version
    except pkg_resources.DistributionNotFound:
        print("pandas is not installed.")
        return    
        
    pandas_version = pd.__version__
    if pkg_resources.parse_version(pandas_version) < pkg_resources.parse_version("2.2.0"):
        #print(f"pandas version is below 2.2.0. Running alternate behavior...")
        df['time'] = pd.to_datetime(df['time'])
    else:
        #print(f"pandas version is {pandas_version}. Running normal behavior...")
        df['time'] = pd.to_datetime(df['time'], format='ISO8601')    

    if (date_index):
        if variable in ['gdf','cdr']:
            df = df.set_index('time')
        else:
            raise ValueError('date_index=True should only be used for gdf and cdr')

    return df


def get_ts(id, data_type, date_index=False):
    """
    This gets a timeseries from the UK National River Flow Archive
    
    Args:
        id (int): an integer value for a station 
        data_type (str or str list): A string describing the data type you want. Options are: 'gdf', 'ndf', 'gmf', 'nmf', 'cdr', 'cdr-d', 'cmr', 'pot-stage', 'pot-flow','gauging-stage', 'gauging-flow','amax-stage', 'amax-flow' The details of these options can be found at https://nrfa.ceh.ac.uk/data-formats-types, with a list of strings the dataframe may be large if times are not overlapping
        

	Returns:
		pandas Dataframe containing the requested dataset

	Author: Simon Moulds, Dan Goldberg
	Date: 20/01/2024
	"""
    
    if isinstance(data_type,str):
        multivar=False
        data_type = [data_type]
    elif all(isinstance(sublist, str) for sublist in data_type):
        multivar=True
    else:
        ValueError('data_type is not a string, or list of strings')

    df_list=[]
    len_var = len(data_type)
    if (not multivar): len_var=1

    for i in range(len_var):
        query = "station=" + str(id) + "&data-type=" + data_type[i] + "&format=json-object"
        stations_info_url = "{BASE}/time-series?{QUERY}".format(
            BASE=BASE_URL, QUERY=query
        )

        # Send request and read response
        response = urllib.request.urlopen(stations_info_url).read()

        # Decode from JSON to Python dictionary
        response = json.loads(response)

        df_list.append(_build_ts(response, date_index))

    if (multivar):
        df = pd.concat(df_list,axis=1)
    else:
        df = df_list[0]

    return df
