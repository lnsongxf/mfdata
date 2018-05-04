import numpy as np
import pandas as pd
from fredapi import Fred
from mfdata.utils import *
from mfdata.dates import *


class ts:

    def __init__(self, frequency, unit, multiplier, currency, idenfier, value):
        self.frequency = frequency
        self.unit = unit
        self.multiplier
        self.currency
        self.idenfier
        self.value


class page(ts):

    def __init__(self, country, sa, value, surface: int = 0):
        super(page, self).__init__()
        self.country = country
        self.sa = sa
        self.value = value
        self.surface = surface # the larger the number, 


class frb_h8(page):
    '''
    Class designed for preparing data from Federal Reserve Board H8 table.
    The class has layers of data that is specified in the H8 table and can
    store data of different categories.

    '''

    def __init__(self,
                 filepath: list):
        super(page, self).__init__()
        self.filepath = filepath

        for path in filepath:
            df = pd.read_csv(path)
            col_names = df.columns
            self. = col_names[1].split('')

    def parse(self):
        '''
        Parse the information in the H8 table provided by the filepath into
        series. If there are multiple items in filepath, each table will be
        parsed into series with their own metadata.
        '''


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
