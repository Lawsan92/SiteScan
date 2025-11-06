import pandas as pd
from PIL.ImageChops import composite
from pandas.core.interchange import dataframe

class PandaDataframe:

    dataframe = {}

    def __init__(self):
        return

    def load_dataframe(self):
        print('loading data')
        # create dataframe and load it with raw CSV data
        dataframe = pd.DataFrame(pd.read_csv(
            'dataset.csv',
            usecols=[2, 3, 4, 5, 6],
            header=0,
            names=['Population_diff', 'Income_diff', 'Home Value_diff', 'Commute Time_diff', 'Poverty_diff']))

        self.dataframe = dataframe

    def to_percentages(self, dataframe):
        self.dataframe = self.dataframe.pct_change()
        self.dataframe = self.dataframe.apply(lambda x: x * 100)
        self.dataframe = self.dataframe.round(2)

    def fill_discretes(self):
        col_list = self.dataframe.columns
        discrete_cols = ['pop_increase', 'income_increase', 'home_value_increase', 'commute_time_increase', 'poverty_increase']
        for i, col in enumerate(col_list):
            self.dataframe.insert(self.dataframe.columns.get_loc(col), discrete_cols[i], 1)
            self.dataframe.loc[self.dataframe[col] < 0, discrete_cols[i]] = -1

    def readd_keys(self):
        composite_keys_dataframe = pd.DataFrame(pd.read_csv(
            'dataset.csv', usecols=[0, 1], header=0))
        self.dataframe.insert(0, 'Year', composite_keys_dataframe['Year'])
        self.dataframe.insert(1, 'Zip Code', composite_keys_dataframe['Zip Code'])

    def save_dataframe(self):
        self.dataframe.to_csv('discrete_dataset.csv')
        print('dataframe saved')
        return

def main():
    panda = PandaDataframe()
    panda.load_dataframe()
    panda.to_percentages(panda.dataframe)
    panda.fill_discretes()
    panda.readd_keys()
    panda.save_dataframe()
    return
main()