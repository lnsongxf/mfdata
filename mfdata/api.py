import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
from fredapi import Fred
from itertools import cycle
from mfdata.utils import *
from mfdata.dates import *


class database:

    def __init__(self,
                 database: str = None,
                 key: str = None,
                 var_list: list = None):
        self.database = database
        self.var_list = var_list  # for simple request in FRED
        self.key = key  # the form depends on the database we use

    def fetch_fred(self):
        '''
        Fetch data from FRED by names given in a list called var_list

        Return
        '''
        if self.key is None:
            import textwrap
            raise ValueError(textwrap.dedent("""\
                    You need to set a valid API key. You can set it in 3 ways:
                    pass the string with api_key, or set api_key_file to a
                    file with the api key in the first line, or set the
                    environment variable 'FRED_API_KEY' to the value of your
                    api key. You can sign up for a free api key on the Fred
                    website at http://research.stlouisfed.org/fred2/"""))

        if self.database is not 'fred':
            import textwrap
            raise ValueError(textwrap.dedent("""\
                    This function is intended for FRED, please try other
                    functions."""))

        var_list = self.var_list
        ts_list = []
        ts = None
        fred = Fred(self.key)
        for var in var_list:
            ts = fred.get_series(var)
            ts.name = var
            ts_list.append(ts)
        return pd.concat(ts_list, axis=1)


class frb_h8:
    '''
    Class designed for preparing data from Federal Reserve Board H8 table.

    '''

        def __init__(self,
                     category: str = 'domestic',
                     filepath):
            self.category = category
            self.filepath = filepath

        def fetch(self):
            if len()
