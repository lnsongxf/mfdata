import numpy as np
import pandas as pd
from fredapi import Fred
from mfdata.utils import *
from mfdata.dates import *


class ts(object):

    def __init__(self,
                 unit: str,
                 multiplier: int,
                 currency: str,
                 UI: str,
                 surface: int,
                 family: list,
                 value):
        self.unit = unit
        self.multiplier = multiplier
        self.currency = currency
        self.UI = UI
        self.surface = surface
        self.family = family
        self.value = value
        self.name = family[surface]


class page(object):

    def __init__(self,
                 category: str,
                 sa: str,
                 value):

        self.category = category
        self.sa = sa  # seasonally-adjusted?
        self.value = value


class frb_h8(dates, plot):
    '''
    Class designed for preparing data from Federal Reserve Board H8 table.
    The class has layers of data that is specified in the H8 table and can
    store data of different categories.

    '''

    def __init__(self,
                 filepath: list):
        '''
        At initialization, data is parsed into time series objects
        categorized by the type of institutions, and aggregated as
        a book of pages. Each time serie records the metadata such
        as the unit of measure, currency, and the unique identifier
        of the serie.

        Raw data will further be transformed into easy-to-use format
        such as Dataframe using functions defined as methods.
        '''

        super(frb_h8, self).__init__()

        self.filepath = filepath
        self.pages = []

        for path in filepath:

            df = pd.read_csv(path)
            col_names = df.columns
            category, sa = col_names[1].split(',')[-2:]
            category = category.strip().title()

            if sa.split(' ')[1] == 'not':
                sa = 'NSA'
            else:
                sa = 'SA'

            ts_list = []
            for col in col_names[1:]:
                family = col.split(',')[0].split(':')
                family = list(map(lambda x: x.strip(), family))

                surface = len(family) - 1

                unit = df.loc[df[col_names[0]] == 'Unit:', col].values[0]

                multiplier = df.loc[df[col_names[0]] == 'Multiplier:',
                                    col].values[0]

                currency = df.loc[df[col_names[0]] == 'Currency:',
                                  col].values[0]

                UI = df.loc[df[col_names[0]] ==
                            'Unique Identifier: ', col].values[0]
                UI = UI.split('/')[-1]

                value = df.loc[5:, [col_names[0], col]]
                value.columns = ['Date', family[surface]]
                value['Date'] = pd.to_datetime(value['Date'], yearfirst=True)
                value[family[surface]] = value[family[surface]].astype(float)
                value.set_index('Date', inplace=True)

                ts_list.append(ts(unit=unit, multiplier=multiplier,
                                  currency=currency, UI=UI,
                                  surface=surface, family=family,
                                  value=value))
            pg = page(category=category, sa=sa, value=ts_list)
            self.pages.append(pg)

    def list(self):
        for page in self.pages:
            page_header = page.category + ', ' + page.sa
            tsname_list = ['{}: {}{}'.format(ts.UI, ts.surface * '\t', ts.name)
                           for ts in page.value]
            page_body = '\n'.join(tsname_list)

            print(color.BOLD + color.RED + page_header + color.END)
            print(page_body)
            print('\n')

    def search(self, page, tsname: str):
        i_ts = 0
        for i, ts in enumerate(page.value):
            if ts.name == tsname:
                i_ts = i
        return i_ts

    def merge(self, tsname: str, multi_index=False):
        df_list = []
        for page in self.pages:
            ts = page.value[self.search(page, tsname)].value
            ts.columns = [tsname + ': ' + page.category]
            df_list.append(ts)
        df = pd.concat(df_list, axis=1)
        return df


class dtcc_repo(dates, plot):

    def __init__(self, filepath: str):

        super(dtcc_repo, self).__init__()

        self.filepath = filepath
        GCF = pd.read_excel(filepath, skiprows=6)
        GCF.Date = pd.to_datetime(GCF.Date, yearfirst=True)
        GCF.set_index('Date', inplace=True)
        GCF = GCF[list(GCF)[:3]]
        GCF.columns = ['Repo: MBS', 'Repo: Treasury', 'Repo: Agency']
        self.value = GCF


class database(object):

    def __init__(self,
                 database: str = None,
                 key: str = None,
                 var_list: list = None):
        self.database = database
        self.var_list = var_list  # for simple request in FRED
        self.key = key  # the form depends on the database we use

    def fetch(self):
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
