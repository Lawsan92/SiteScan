import pandas as pd
import csv

class PandaDataframe:

    dataframe = {}
    binned_dataframe = []
    increased_dataframe = []
    decreased_dataframe = []

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

        # print(df.head())
        self.dataframe = df

        df = df.drop(['Year', 'Zip Code','Population','Income', 'Home Value','Commute Time','Poverty', 'Year_pct_change', 'Zip Code_pct_change'], axis=1)
        df = df.drop([0])
        self.dataframe = df
        print('saving percentages to csv file...')
        df.to_csv('csv/grouped_dataset_percentages.csv')

    def discretize(self):
        print('converting continuous variables to discrete variables...')
        cont_cols = self.dataframe.columns

        def discretize_increase():
            increase_data = self.dataframe.copy()
            for i, col in enumerate(cont_cols):
                increase_data[col] = (increase_data[col] > 0).astype(int)
                increase_data.loc[increase_data[col] > 0, col] = 1
                increase_data.loc[increase_data[col] < 0, col] = 0
            print('saving increasing discrete dataframe to csv file...')
            increase_data.to_csv('csv/increase/increase_discrete_dataset.csv')
            return increase_data

        self.increased_dataframe = discretize_increase()

        def discretize_decrease():
            decrease_data = self.dataframe.copy()
            for i, col in enumerate(cont_cols):
                decrease_data.loc[decrease_data[col] > 0, col] = 0
                decrease_data.loc[decrease_data[col] < 0, col] = 1
            print('saving decreasing discrete dataframe to csv file...')
            decrease_data.to_csv('csv/decrease/decrease_discrete_dataset.csv')
            return decrease_data

        self.decreased_dataframe =  discretize_decrease()

    def bin_items(self):
        print('binning items...')

        def bin_increase():
            dataframe = self.increased_dataframe.copy()
            cols = dataframe.columns
            itemsets = []
            for index, row in dataframe.iterrows():
                basket = []
                for i, item in enumerate(row):
                    if item == 1.0:
                        basket.append(cols[i])
                itemsets.append(basket)

            print('saving increase binned dataframe...')
            with open('csv/increase/binned_dataset_increase.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(itemsets)
        bin_increase()

        def bin_decrease():
            dataframe = self.decreased_dataframe.copy()
            cols = dataframe.columns
            itemsets = []
            for index, row in dataframe.iterrows():
                basket = []
                for i, item in enumerate(row):
                    if item == 1.0:
                        basket.append(cols[i])
                itemsets.append(basket)

            print('saving decreased binned dataframe...')
            with open('csv/decrease/binned_dataset_decrease.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(itemsets)
        bin_decrease()

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