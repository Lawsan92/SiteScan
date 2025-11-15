import csv
import os
import pandas as pd
from mlxtend.evaluate import lift_score
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
from SiteScan.settings import BASE_DIR

class UnsupervisedModel:

    increase_data = []
    decrease_data = []
    base_path = os.path.join(BASE_DIR, 'SiteScan/csv/')
    increase_path = os.path.join(base_path, 'increase')
    decrease_path = os.path.join(base_path, 'decrease')

    def __init__(self):
        return

    def load_data(self):

        def load_increase_data():
            print('loading increase data...')
            self.increase_data = pd.read_csv(os.path.join(self.increase_path, 'increase_discrete_dataset.csv'), usecols=[1, 2, 3, 4, 5])
        load_increase_data()

        def load_decrease_data():
            print('loading decrease data...')
            self.decrease_data = pd.read_csv(os.path.join(self.decrease_path, 'decrease_discrete_dataset.csv'), usecols=[1, 2, 3, 4, 5])
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

            frequent_itemsets = apriori(
                self.increase_data,
                min_support=0.01,
                use_colnames=True
            )

            rules = association_rules(
                frequent_itemsets,
                metric="lift",
                min_threshold=1.0
            )

            rules = rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']]
            rules.sort_values(by='support', ascending=False, inplace=True)
            print('saving increase association rules to csv file...')
            rules.to_csv(os.path.join(self.increase_path, 'increase_association_rules.csv'))
        increase_association_rules()

        def decrease_association_rules():
            print('generating decrease association rules...')
            frequent_itemsets = apriori(
                self.decrease_data,
                min_support=0.01,
                use_colnames=True
            )

            rules = association_rules(
                frequent_itemsets,
                metric="lift",
                min_threshold=1.0
            )
            print('rules:', rules)

            rules = rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']]
            rules.sort_values(by='support', ascending=False, inplace=True)
            print('saving decrease association rules to csv file...')
            rules.to_csv(os.path.join(self.decrease_path, 'decrease_association_rules.csv'))
        decrease_association_rules()

    def save_model(self):
        data = self.apriori_model()
        dataframe = pd.DataFrame(data)
        data.to_csv('csv/apriori_model.csv')

def main():
    model = UnsupervisedModel()
    model.load_data()
    # model.transaction_encoder()
    # model.apriori_model()
    model.association_rules()
    return
main()