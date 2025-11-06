import pandas as pd

class Panda:
    def __init__(self):
        return
    def load_data(self):
        print('loading data')
        pd.read_csv('dataset.csv')
        return pd.read_csv('dataset.csv')
panda = Panda()
print(panda.load_data())