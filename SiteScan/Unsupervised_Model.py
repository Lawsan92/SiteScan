import csv
import pandas as pd
from mlxtend.evaluate import lift_score
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
        apriori_itemsets = apriori(self.data, min_support=0.1, use_colnames=True)
        apriori_itemsets['length'] = apriori_itemsets['itemsets'].apply(lambda x: len(x))
        # apriori_itemsets = apriori_itemsets[(apriori_itemsets['length'] >= 2) &
        #                   (apriori_itemsets['support'] >= 0.4)]
        apriori_itemsets = apriori_itemsets.sort_values(by='support', ascending=False)

        return apriori_itemsets

    def association_rules(self):
        apriori_itemsets = apriori(self.data, min_support=0.1, use_colnames=True)
        rules = association_rules(apriori_itemsets, metric="confidence", min_threshold=0.1)
        rules = rules[rules['antecedents'].apply(lambda x: len(x) == 1) & rules['consequents'].apply(lambda x: len(x) == 1)]
        print("Association Rules:", rules.shape[0])
        rules['support'] = round(rules['support'] * 100, 2)
        rules['confidence'] = round(rules['confidence'] * 100, 2)
        rules['lift'] = round(rules['lift'] * 100, 2)
        rules = rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']]
        rules.sort_values(by='lift', ascending=False, inplace=True)
        rules = rules.head(10)
        rules.to_csv('csv/association_rules.csv')

    def save_model(self):
        data = self.apriori_model()
        dataframe = pd.DataFrame(data)
        data.to_csv('csv/apriori_model.csv')

def main():
    model = UnsupervisedModel()
    model.load_data()
    model.transaction_encoder()
    model.apriori_model()
    # print(model.apriori_model())
    model.association_rules()
    model.save_model()
    return
main()