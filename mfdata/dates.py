
import datetime
import pandas as pd


class dates:

    def __init__(self):
        FOMC = ['2013-01-29', '2013-03-19', '2013-04-30',
                '2013-06-18', '2013-07-30', '2013-09-17', '2013-10-29',
                '2013-12-17', '2014-01-28', '2014-03-18', '2014-04-29',
                '2014-06-17', '2014-07-29', '2014-09-16', '2014-10-28',
                '2014-12-16', '2015-01-27', '2015-03-17', '2015-04-28',
                '2015-06-16', '2015-07-28', '2015-09-16', '2015-10-27',
                '2015-12-15', '2016-01-26', '2016-03-15', '2016-04-26',
                '2016-06-14', '2016-07-26', '2016-09-20', '2016-11-01',
                '2016-12-13', '2017-01-31', '2017-03-14', '2017-05-02',
                '2017-06-13', '2017-07-25', '2017-09-19', '2017-10-31',
                '2017-12-12', '2018-01-30', '2018-03-20']

        self.FOMC = pd.to_datetime(FOMC, yearfirst=True)

    # find the subsample before and after the FOMC meetings

    def FOMC_sample(self, df, window: int):
        '''
        Input:
            df: a pandas.Dataframe object contains the full sample
            FOMC_dates: a pandas.DatetimeIndex object that contains the
            historical dates of FOMC meetings

        Output:
            df_FOMC: a pandas.Dataframe object that contains the subsample
            for the window period specified
        '''

        w = datetime.timedelta(weeks=window)
        after = pd.to_datetime([d + w for d in self.FOMC], yearfirst=True)
        before = pd.to_datetime([d - w for d in self.FOMC], yearfirst=True)

        indexlist = []
        for before, after in zip(before, after):
            indexlist += [before + datetime.timedelta(days=x)
                          for x in range(0, (after - before).days)]
        return df.loc[df.index.intersection(indexlist), :]
