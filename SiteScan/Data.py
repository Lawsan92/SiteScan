import base64
from io import BytesIO
from matplotlib import pyplot as plt
from datacommons_client.client import DataCommonsClient

class Data:
    def __init__(self, user_zip):
        self.zip = user_zip
        self.data = {}
        self.year_list = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
        self.dcids = [
                "Count_Person",
                "Mean_Income_Household",
                'Median_HomeValue_HousingUnit_OccupiedHousingUnit_OwnerOccupied',
                'Count_HousingUnit',
                'Count_Person_BelowPovertyLevelInThePast12Months',
            ]
        self.graph_data = {}
        self.table_data = {}

    def API_fetch(self):
        print('fetching data from API...')
        zip_code = self.zip
        api_key = "AIzaSyCTI4Xz-UW_G2Q2RfknhcfdAnTHq5X5XuI"  # Replace with your API key
        client = DataCommonsClient(api_key=api_key)
        self.data = client.observation.fetch(
            variable_dcids=self.dcids,
            date='',
            entity_dcids=[f'zip/{zip_code}']
        )

    def model_data(self):
        print('cleaning and modeling data...')
        cleaned_data = {}
        for dcid in self.dcids:
            if len(self.data.byVariable[dcid].byEntity[f'zip/{self.zip}'].orderedFacets) == 0:
                cleaned_data[dcid] = []
            else:
                cleaned_data[dcid] = self.data.byVariable[dcid].byEntity[f'zip/{self.zip}'].orderedFacets[0].observations
                cleaned_data[dcid] = [item for item in cleaned_data[dcid] if 2013 <= int(item.date)]
        self.data = cleaned_data

    def print(self):
        print('printing data...')
        print(self.data)

    def graph_data_line(self):
        print('generating graphs...')
        data = self.data

        # X-data points (= years), Y-data points (= population)
        year_list = self.year_list
        data_list = {}
        for key, dataset in data.items():
            data_list[key] = []
            for item in dataset:
                data_list[key].append(int(item.value))

        self.data = data_list
        # draw the line graph, i.e., the matplotlib plot figure

        graph_payload = {}

        for key, dataset in data_list.items():
            # generate plot
            plt.figure(figsize=(10, 6))
            plt.title(f'{key} of {self.zip}')
            plt.xlabel(f'{key}')
            plt.ylabel(f'{key}')
            plt.plot(year_list, dataset, color='blue')

            #convert to html markdown element
            graph_buffer_file = BytesIO()
            plt.savefig(graph_buffer_file, format='png')
            graph_buffer_file_base64 = base64.b64encode(graph_buffer_file.getvalue())
            graph_buffer_file_html = graph_buffer_file_base64.decode('utf-8')
            graph_html = '<img src=\'data:image/png;base64,{}\'>'.format(graph_buffer_file_html)
            graph_payload[key] = graph_html

        return graph_payload

    def graph_data_table(self):
        print('generating tables...')
        data = self.data
        year_list = self.year_list
        table_payload = {}

        for key, dataset in data.items():
            # Column labels
            col_labels = ['Year', f'{key}']

            # Data for the table
            table_data = []

            for index, item in enumerate(dataset):
                year = year_list[index]
                item = int(dataset[index])
                table_data.append([year, item])

            # Create a figure and axes
            fig, ax = plt.subplots(figsize=(6, 3))

            # Hide the axes to display only the table
            ax.axis('off')
            ax.axis('tight')  # Adjust limits to fit the table

            # Create the table fig
            ax.table(cellText=table_data, colLabels=col_labels, loc='center', cellLoc='center')
            ax.set_title(f'{key} of {self.zip}')

            # convert table fig to html markdown
            table_file = BytesIO()
            fig.savefig(table_file, format='png')
            table_file_encoded = base64.b64encode(table_file.getvalue()).decode('utf-8')
            table_html = '<img src=\'data:image/png;base64,{}\'>'.format(table_file_encoded)

            table_payload[key] = table_html

        return table_payload


def main():
    data = Data(78735)
    data.API_fetch()
    data.model_data()
    data.graph_data_line()
    data.graph_data_table()
    return
# main()