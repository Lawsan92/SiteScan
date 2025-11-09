import csv
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

class UnsupervisedModel:
    data = []
    def __init__(self):
        return

    def load_data(self):
        with open('csv/binned_dataset.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            self.data = list(reader)

    def transaction_encoder(self):
        transaction_encoder = TransactionEncoder()
        transaction_encoder_array = transaction_encoder.fit(self.data).transform(self.data)
        dataframe = pd.DataFrame(transaction_encoder_array, columns=transaction_encoder.columns_)
        self.data = dataframe

    def print(self):
        print(self.data)

    def apriori_model(self):
        apriori_itemsets = apriori(self.data, min_support=0.4, use_colnames=True)
        apriori_itemsets['length'] = apriori_itemsets['itemsets'].apply(lambda x: len(x))
        apriori_itemsets = apriori_itemsets[(apriori_itemsets['length'] >= 2) &
                          (apriori_itemsets['support'] >= 0.4)]

        apriori_itemsets = apriori_itemsets.sort_values(by='support', ascending=False)
        return apriori_itemsets

    def save_model(self):
        with open('csv/apriori_model.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(self.apriori_model())

def main():
    model = UnsupervisedModel()
    model.load_data()
    model.transaction_encoder()
    model.apriori_model()
    print(model.apriori_model())
    model.save_model()
    return
main()