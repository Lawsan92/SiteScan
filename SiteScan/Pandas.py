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
        self.dataframe = pd.DataFrame(pd.read_csv('csv/dataset.csv'))

    def to_percentages(self):
        print('Converting numeric columns to percentage changes by Zip Code...')
        df = self.dataframe.copy()
        numeric_cols = df.select_dtypes(include='number').columns

        # Loop through all numeric columns
        for col in numeric_cols:
            # Compute pct_change() within each Zip Code group
            df[f'{col}_pct_change'] = df.groupby('Zip Code')[col].pct_change() * 100

        df = df.round(2)

        print(df.head())
        self.dataframe = df

        df = df.drop(['Year', 'Zip Code','Population','Income', 'Home Value','Commute Time','Poverty', 'Year_pct_change', 'Zip Code_pct_change'], axis=1)
        df = df.drop([0])
        self.dataframe = df
        print('saving percentages to csv file...')
        df.to_csv('csv/grouped_dataset_percentages.csv')


    def discretize(self):
        print('converting continuous variables to discrete variables...')
        cont_cols = self.dataframe.columns
        for i, col in enumerate(cont_cols):
            self.dataframe.loc[self.dataframe[col] > 0, col] = True
            self.dataframe.loc[self.dataframe[col] < 0, col] = False
        print('saving discrete dataframe to csv file...')
        self.dataframe.to_csv('csv/discrete_dataset.csv')

    def bin_items(self):
        print('binning items')
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

        print('saving binned dataframe...')
        with open('csv/binned_dataset.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(self.binned_dataframe)

    def print(self):
        print(self.dataframe)

# def main():
#     panda = PandaDataframe()
#     panda.load_dataframe()
#     panda.to_percentages()
#     panda.discretize()
#     panda.bin_items()
#     return
# main()