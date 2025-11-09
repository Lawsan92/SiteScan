import pandas as pd
import csv

class PandaDataframe:

    dataframe = {}
    binned_dataframe = []

    def __init__(self):
        return

    def load_dataframe(self):
        print('loading data')
        # create dataframe and load it with raw CSV data
        dataframe = pd.DataFrame(pd.read_csv(
            'csv/dataset.csv',
            usecols=[2, 3, 4, 5, 6],
            header=0,
            names=['Population_diff', 'Income_diff', 'Home Value_diff', 'Commute Time_diff', 'Poverty_diff']))

        self.dataframe = dataframe

    def to_percentages(self, dataframe):
        self.dataframe = self.dataframe.pct_change()
        self.dataframe = self.dataframe.apply(lambda x: x * 100)
        self.dataframe = self.dataframe.round(2)

    def fill_discretes(self):
        cont_cols = self.dataframe.columns
        discrete_cols = ['pop_increase', 'income_increase', 'home_value_increase', 'commute_time_increase', 'poverty_increase']
        for i, col in enumerate(cont_cols):
            self.dataframe.insert(self.dataframe.columns.get_loc(col), discrete_cols[i], True)
            self.dataframe.loc[self.dataframe[col] < 0, discrete_cols[i]] = False

    def readd_keys(self):
        composite_keys_dataframe = pd.DataFrame(pd.read_csv(
            'csv/dataset.csv', usecols=[0, 1], header=0))
        self.dataframe.insert(0, 'Year', composite_keys_dataframe['Year'])
        self.dataframe.insert(1, 'Zip Code', composite_keys_dataframe['Zip Code'])

    def filter_cont_cols(self):
        self.dataframe = self.dataframe.drop(columns=['Population_diff', 'Income_diff', 'Home Value_diff', 'Commute Time_diff', 'Poverty_diff'])

    def save_dataframe(self):
        self.dataframe.to_csv('csv/discrete_dataset.csv')
        print('dataframe saved')
        return

    def bin_items(self):
        dataframe  = self.dataframe
        cols = dataframe.columns
        itemsets = []
        for index, row in dataframe.iterrows():
            basket = []
            for i, item in enumerate(row):
                if item:
                    basket.append(cols[i])
            itemsets.append(basket)
        self.binned_dataframe = itemsets


    def save_binned_dataframe(self):
        with open('csv/binned_dataset.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(self.binned_dataframe)
        return

    def save_data(self):
        self.dataframe.to_csv('csv/research_dataset.csv', index=False)

    def print(self):
        print(self.dataframe)

def main():
    panda = PandaDataframe()
    panda.load_dataframe()
    panda.to_percentages(panda.dataframe)
    panda.fill_discretes()
    panda.filter_cont_cols()
    panda.bin_items()
    panda.save_binned_dataframe()
    panda.readd_keys()
    panda.save_dataframe()
    return
main()

# def main_2():
#     panda = PandaDataframe()
#     panda.load_dataframe()
#     panda.to_percentages(panda.dataframe)
#     panda.readd_keys()
#     panda.print()
#     # panda.save_data()
#
# main_2()