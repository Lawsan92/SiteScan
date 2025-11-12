import csv
import pandas as pd
from mlxtend.evaluate import lift_score
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

class UnsupervisedModel:
    increase_data = []
    decrease_data = []

    def __init__(self):
        return

    def load_data(self):

        def load_increase_data():
            print('loading increase data...')
            with open('csv/increase/binned_dataset_increase.csv', 'r') as csvfile:
                print('loading increase data...')
                reader = csv.reader(csvfile)
                self.increase_data = list(reader)
        load_increase_data()

        def load_decrease_data():
            print('loading decrease data...')
            with open('csv/decrease/binned_dataset_decrease.csv', 'r') as csvfile:
                print('loading decrease data...')
                reader = csv.reader(csvfile)
                self.decrease_data = list(reader)
        load_decrease_data()

    def transaction_encoder(self):
        transaction_encoder = TransactionEncoder()

        def encode_increase():
            print('encoding increase data...')
            transaction_encoder_array = transaction_encoder.fit(self.increase_data).transform(self.increase_data)
            dataframe = pd.DataFrame(transaction_encoder_array, columns=transaction_encoder.columns_)
            self.increase_data = dataframe
        encode_increase()

        def encode_decrease():
            print('encoding decrease data...')
            transaction_encoder_array = transaction_encoder.fit(self.decrease_data).transform(self.decrease_data)
            dataframe = pd.DataFrame(transaction_encoder_array, columns=transaction_encoder.columns_)
            self.decrease_data = dataframe
        encode_decrease()

    def print(self):
        print(self.increase_data)
        print(self.decrease_data)

    def apriori_model(self):
        apriori_itemsets = apriori(self.increase_data, min_support=0.1, use_colnames=True)
        apriori_itemsets['length'] = apriori_itemsets['itemsets'].apply(lambda x: len(x))
        # apriori_itemsets = apriori_itemsets[(apriori_itemsets['length'] >= 2) &
        #                   (apriori_itemsets['support'] >= 0.4)]
        apriori_itemsets = apriori_itemsets.sort_values(by='support', ascending=False)

        return apriori_itemsets

    def association_rules(self):

        def increase_association_rules():
            print('generating increase association rules...')
            apriori_itemsets = apriori(self.increase_data, min_support=0.1, use_colnames=True)
            rules = association_rules(apriori_itemsets, metric="confidence", min_threshold=0.1)
            rules = rules[rules['antecedents'].apply(lambda x: len(x) == 1) & rules['consequents'].apply(lambda x: len(x) == 1)]
            print("Association Rules:", rules.shape[0])
            rules['support'] = round(rules['support'] * 100, 2)
            rules['confidence'] = round(rules['confidence'] * 100, 2)
            rules['lift'] = round(rules['lift'] * 100, 2)
            rules = rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']]
            rules.sort_values(by='lift', ascending=False, inplace=True)
            rules = rules.head(10)
            rules.to_csv('csv/increase/increase_association_rules.csv')
        increase_association_rules()

        def decrease_association_rules():
            print('generating decrease association rules...')
            apriori_itemsets = apriori(self.decrease_data, min_support=0.1, use_colnames=True)
            rules = association_rules(apriori_itemsets, metric="confidence", min_threshold=0.1)
            rules = rules[rules['antecedents'].apply(lambda x: len(x) == 1) & rules['consequents'].apply(lambda x: len(x) == 1)]
            print("Association Rules:", rules.shape[0])
            rules['support'] = round(rules['support'] * 100, 2)
            rules['confidence'] = round(rules['confidence'] * 100, 2)
            rules['lift'] = round(rules['lift'] * 100, 2)
            rules = rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']]
            rules.sort_values(by='lift', ascending=False, inplace=True)
            rules = rules.head(10)
            rules.to_csv('csv/decrease/decrease_association_rules.csv')
        decrease_association_rules()

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
    # model.save_model()
    return
main()