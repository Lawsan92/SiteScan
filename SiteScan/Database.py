from datacommons_client.client import DataCommonsClient
import csv

class Database:
    def __init__(self):
        self.data = {}

    def API_fetch(self):
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
            entity_dcids=['zip/78735', 'zip/78730', 'zip/78721', 'zip/78729', 'zip/78734', 'zip/78652', 'zip/78725', 'zip/78617', 'zip/78703', 'zip/78645']
        )

    def print(self):
        print(self.data)

    def model_data(self):
        data_model = {}
        data_keys = [
            "Count_Person",
            "Mean_Income_Household",
            'Median_HomeValue_HousingUnit_OccupiedHousingUnit_OwnerOccupied',
            'Mean_CommuteTime_Person_Years16Onwards_WorkCommute_Employed_WorkedOutsideOfHome',
            'Count_HousingUnit',
            'Count_Person_BelowPovertyLevelInThePast12Months',
        ]
        zip_keys = [78735, 78730, 78721, 78729, 78734, 78652, 78725, 78617, 78703, 78645]

        for key in data_keys:
            for dataset in self.data.byVariable[key]:
                for zip_key in zip_keys:
                    filtered_dataset = dataset[1][f'zip/{zip_key}'].orderedFacets[0].observations
                    for entry in filtered_dataset:
                        year = entry.date
                        value = entry.value
                        model_key = '[' + str(year) + '|' + str(zip_key) + ']'
                        if model_key not in data_model:
                            data_model[model_key] = []
                        data_model[model_key].append([key, value])
        self.data = data_model

    def save_data(self):
        with open('dataset.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Year', 'Zip Code', 'Population', 'Income', 'Home Value', 'Commute Time', 'Poverty'])
            for key, entry in self.data.items():
                writer.writerow([key.split('|')[0], key.split('|')[1], entry[0][1], entry[1][1], entry[2][1], entry[3][1], entry[4][1]])
        return

# main logic
data = Database()
data.API_fetch()
data.model_data()
data.save_data()
