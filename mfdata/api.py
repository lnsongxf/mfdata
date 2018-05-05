import numpy as np
import pandas as pd
from fredapi import Fred
from mfdata.utils import *
from mfdata.dates import *


class ts:

    def __init__(self,
                 frequency=None,
                 unit: str,
                 multiplier: int,
                 currency: str,
                 idenfier: str,
                 surface: int,
                 family: list,
                 value):
        self.frequency = frequency
        self.unit = unit
        self.multiplier = multiplier
        self.currency = currency
        self.idenfier = idenfier
        self.surface = surface
        self.family = family
        self.value = value


class page(object):

    def __init__(self,
                 category: str,
                 sa: str,
                 value):

        self.category = category
        self.sa = sa  # seasonally-adjusted?
        self.value = value


class frb_h8(object):
    '''
    Class designed for preparing data from Federal Reserve Board H8 table.
    The class has layers of data that is specified in the H8 table and can
    store data of different categories.

    '''

    def __init__(self,
                 filepath: list):

        self.filepath = filepath
        self.pages = []

        for path in filepath:

            df = pd.read_csv(path)
            col_names = df.columns
            category, sa = col_names[1].split(',')[-2:]

            if sa.split(' ')[1] == 'not':
                sa = 'nsa'
            else:
                sa = 'sa'

            ts_list = []
            for col in col_names[1:]:
                family = col.split(',')[0].split(':')
                surface = len(family) - 1
                unit = df.loc[df[col_names[0]] == 'Unit:', col].values[0]
                multiplier = df.loc[df[col_names[0]] == 'Multiplier:',
                                    col].values[0]
                currency = df.loc[df[col_names[0]] == 'Currency:',
                                  col].values[0]
                idenfier = df.loc[df[col_names[0]] ==
                                  'Unique Identifier: ', col].values[0]
                value = df.loc[5:, [col_names[0], col]]
                value.columns = ['Date', family[surface]]
                value.set_index('Date', inplace=True)

                ts_list.append(ts(unit=unit, multiplier=multiplier,
                                  currency=currency, idenfier=idenfier,
                                  surface=surface, family=family,
                                  value=value))
            df = pd.concat(ts_list, )

            self.pages.append()


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
                    You need to set a valid API key."""))

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
