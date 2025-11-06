import pandas as pd
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

    def fill_discretes(self):
        col_list = self.dataframe.columns
        discrete_cols = ['pop_increase', 'income_increase', 'home_value_increase', 'commute_time_increase', 'poverty_increase']
        # print(self.dataframe['Population_diff'])
        for i, col in enumerate(col_list):
            self.dataframe.insert(self.dataframe.columns.get_loc(col), discrete_cols[i], 1)
            self.dataframe.loc[self.dataframe[col] < 0, discrete_cols[i]] = -1

    def save_dataframe(self):
        self.dataframe.to_csv('dataframe.csv')
        return

def main():
    panda = PandaDataframe()
    panda.load_dataframe()
    panda.to_percentages(panda.dataframe)
    panda.fill_discretes()
    print(panda.dataframe)
    panda.save_dataframe()
    return
main()


'''
df = pd.DataFrame({'a': [1, 2, 3, 4, 5, 6],
                   'b': [1, 1, 2, 3, 5, 8],
                   'c': [1, 4, 9, 16, 25, 36]})
print('df:', df, '\ndf.diff():\n', df.diff())


df:    a  b   c
0  1  1   1
1  2  1   4
2  3  2   9
3  4  3  16
4  5  5  25
5  6  8  36
 
df.diff():
      a    b     c
0  NaN  NaN   NaN
1  1.0  0.0   3.0
2  1.0  1.0   5.0
3  1.0  1.0   7.0
4  1.0  2.0   9.0
5  1.0  3.0  11.0
'''


# # Creating a list of tuples for the DataFrame
# matrix = [(1, 2, 3, 4),
#           (5, 6, 7, 8),
#           (9, 10, 11, 12),
#           (13, 14, 15, 16)]
#
# # Creating the DataFrame
# df = pd.DataFrame(matrix, columns=list('abcd'))
#
# # Output the DataFrame
# print("Original DataFrame:")
# print(df)
# print('\n')
#
# # Applying lambda function to add 10 to each value in every column
# new_df = df.apply(lambda x: x + 10)
# print("New DataFrame:")
# print(new_df)