
import datetime
import pandas as pd


class dates:

    def __init__(self):
        FOMC = pd.read_csv('FOMC.csv')['FOMC'].tolist()
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
