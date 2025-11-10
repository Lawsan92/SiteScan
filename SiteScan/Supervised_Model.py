import pandas as pd

class SupervisedModel:

     data = None

     def linear_regression(self, x, y):
         return

     def import_data(self):
         print('importing data...')
         self.data = pd.read_csv('csv/research_dataset.csv', skiprows=lambda x: x in [1])
         self.data = self.data.drop(columns=['Year', 'Zip Code'])
         return

     def print(self):
         dataframe = self.data
         print(dataframe)

     def correlation(self):
         dataframe = self.data
         print(dataframe.corr()['Population_diff'])

def main():
    model = SupervisedModel()
    model.import_data()
    # model.print()
    model.correlation()
    return

main()