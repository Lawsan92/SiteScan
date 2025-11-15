from datacommons_client.client import DataCommonsClient
from SiteScan.settings import BASE_DIR
import csv
import os

class Database:
    def __init__(self, user_zip=None):
        self.data = {}
        self.dcids = ['zip/78735', 'zip/78730', 'zip/78721', 'zip/78729', 'zip/78734', 'zip/78652', 'zip/78725', 'zip/78617', 'zip/78703', 'zip/78645', 'zip/78701', 'zip/78719', 'zip/78737', 'zip/78752', 'zip/78681', 'zip/78758', 'zip/78738', 'zip/78705', 'zip/78717', 'zip/78742', 'zip/78759', 'zip/78746', 'zip/78741', 'zip/78736', 'zip/78753']
        self.zip_keys = [78735, 78730, 78721, 78729, 78734, 78652, 78725, 78617, 78703, 78645, 78701, 78719, 78737, 78752, 78681, 78758, 78738, 78705, 78717, 78742, 78759, 78746, 78741, 78736, 78753]
        self.data_size = len(self.zip_keys)
        return

    def API_fetch(self):
        print('fetching data from API...')
        api_key = "AIzaSyCTI4Xz-UW_G2Q2RfknhcfdAnTHq5X5XuI"  # Replace with your API key
        client = DataCommonsClient(api_key=api_key)
        self.data = client.observation.fetch(
            variable_dcids=[
                "Count_Person",
                "Mean_Income_Household",
                'Median_HomeValue_HousingUnit_OccupiedHousingUnit_OwnerOccupied',
                'Mean_CommuteTime_Person_Years16Onwards_WorkCommute_Employed_WorkedOutsideOfHome',
                'Count_HousingUnit',
                'Count_Person_BelowPovertyLevelInThePast12Months',
            ],
            date='all',
            entity_dcids= self.dcids
        )

    def print(self):
        print(self.data)

    def model_data(self):
        print('cleaning and modeling data...')
        data_model = {}
        data_keys = [
            "Count_Person",
            "Mean_Income_Household",
            'Median_HomeValue_HousingUnit_OccupiedHousingUnit_OwnerOccupied',
            'Mean_CommuteTime_Person_Years16Onwards_WorkCommute_Employed_WorkedOutsideOfHome',
            'Count_HousingUnit',
            'Count_Person_BelowPovertyLevelInThePast12Months',
        ]
        zip_keys = self.zip_keys

        for key in data_keys:
            for dataset in self.data.byVariable[key]:
                for zip_key in zip_keys:
                    filtered_dataset = dataset[1][f'zip/{zip_key}'].orderedFacets[0].observations
                    for i, entry in enumerate(filtered_dataset):

                        def missing_entry():
                            if i < len(filtered_dataset) - 1:
                                if int(filtered_dataset[i + 1].date) != int(filtered_dataset[i].date) + 1:
                                    dummy_data = type('Observation', (object,), {
                                        'date': int(filtered_dataset[i].date) + 1,
                                        'value': 'null'
                                    })
                                    filtered_dataset.insert(i + 1, dummy_data)
                            return
                        missing_entry()

                        year = entry.date
                        value = entry.value
                        model_key = '[' + str(year) + '|' + str(zip_key) + ']'
                        if model_key not in data_model:
                            data_model[model_key] = []
                        data_model[model_key].append([key, value])
        self.data = data_model
        print(f'data model created...number of zip codes: {self.data_size}')

    def save_data(self):
        print('saving data...')
        base_path = BASE_DIR
        base_path = os.path.join(base_path, 'SiteScan/csv/')
        with open( os.path.join(base_path, 'dataset.csv'), 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Year', 'Zip Code', 'Population', 'Income', 'Home Value', 'Commute Time', 'Poverty'])
            for key, entry in self.data.items():
                writer.writerow([key[1: key.find('|')], key[key.find('|') + 1:len(key) - 1], entry[0][1], entry[1][1], entry[2][1], entry[3][1], entry[4][1]])
        return

    def get_data(self):
        return self.data

# # main logic
# def main():
#     data = Database()
#     data.API_fetch()
#     data.model_data()
#     data.save_data()
#     return
#
# main()