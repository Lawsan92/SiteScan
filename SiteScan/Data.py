import base64
from io import BytesIO
from matplotlib import pyplot as plt
from datacommons_client.client import DataCommonsClient

class Data:
    def __init__(self, user_zip):
        self.zip = user_zip
        self.data = self.API_fetch()
        self.line_graph = self.graph_data_line()

    def API_fetch(self):
        zip_code = self.zip
        api_key = "AIzaSyCTI4Xz-UW_G2Q2RfknhcfdAnTHq5X5XuI"  # Replace with your API key
        client = DataCommonsClient(api_key=api_key)
        response = client.observation.fetch(
            variable_dcids=[
                "Count_Person"],
            date='',
            entity_dcids=[f'zip/{zip_code}']
        )

        response_body = response.byVariable['Count_Person'].byEntity[f'zip/{zip_code}'].orderedFacets[0].observations
        filtered_response_body = [item for item in response_body if 2013 <= int(item.date)]
        return filtered_response_body

    def print(self):
        print(self.data)

    def graph_data_line(self):
        data = self.data
        # X-data points (= years), Y-data points (= population)
        year_list, population_list = [], []
        for index, item in enumerate(data):
            year_list.append(int(item.date))
            population_list.append(float(item.value))

        # draw the line graph, i.e., the matplotlib plot figure
        plt.figure(figsize=(10, 6))
        plt.title(f'Population of {self.zip}')
        plt.xlabel('Year')
        plt.ylabel('Population (in thousands)')
        plt.plot(year_list, population_list, color='blue')

        # convert the figure into a PNG and save it to a buffer file
        graph_buffer_file = BytesIO()
        plt.savefig(graph_buffer_file, format='png')
        # encode the PNG file into base64, decode it to utf-8, embed it in a src attribute
        graph_buffer_file_base64 = base64.b64encode(graph_buffer_file.getvalue())
        graph_buffer_file_html = graph_buffer_file_base64.decode('utf-8')
        graph_html = '<img src=\'data:image/png;base64,{}\'>'.format(graph_buffer_file_html)
        return graph_html

    def graph_data_table(self):

        data = self.data
        # Column labels
        col_labels = ['Year', 'Population']

        # Data for the table
        table_data = []

        for index, item in enumerate(data):
            year = int(item.date)
            population = int(item.value)
            table_data.append([year, population])

        # Create a figure and axes
        fig, ax = plt.subplots(figsize=(6, 3))

        # Hide the axes to display only the table
        ax.axis('off')
        ax.axis('tight')  # Adjust limits to fit the table

        # Create the table
        ax.table(cellText=table_data, colLabels=col_labels, loc='center', cellLoc='center')

        #convert table to base64 image and inject in html <img> template
        table_file = BytesIO()
        fig.savefig(table_file, format='png')
        table_file_encoded = base64.b64encode(table_file.getvalue()).decode('utf-8')

        table_html = '<img src=\'data:image/png;base64,{}\'>'.format(table_file_encoded)

        return

    def model_data(self):
        api_key = "AIzaSyCTI4Xz-UW_G2Q2RfknhcfdAnTHq5X5XuI"  # Replace with your API key
        client = DataCommonsClient(api_key=api_key)
        raw_data = client.observation.fetch(
            variable_dcids=[
                "Count_Person",
                "Mean_Income_Household",
                'Median_HomeValue_HousingUnit_OccupiedHousingUnit_OwnerOccupied',
                'Mean_CommuteTime_Person_Years16Onwards_WorkCommute_Employed_WorkedOutsideOfHome',
                'Count_HousingUnit',
                'Count_Person_BelowPovertyLevelInThePast12Months',
            ],
            date='all',
            entity_dcids=["zip/78735", "zip/78730"]
        )
        data_model = {}
        data_keys = [
            "Count_Person",
            "Mean_Income_Household",
            'Median_HomeValue_HousingUnit_OccupiedHousingUnit_OwnerOccupied',
            'Mean_CommuteTime_Person_Years16Onwards_WorkCommute_Employed_WorkedOutsideOfHome',
            'Count_HousingUnit',
            'Count_Person_BelowPovertyLevelInThePast12Months',
        ]
        zip_keys = [78735, 78730]

        for key in data_keys:
            for dataset in raw_data.byVariable[key]:
                for zip_key in zip_keys:
                    filtered_dataset = dataset[1][f'zip/{zip_key}'].orderedFacets[0].observations
                    for entry in filtered_dataset:
                        year = entry.date
                        value = entry.value
                        model_key = '[' + str(year) + '|' + str(zip_key) + ']'
                        if model_key not in data_model:
                            data_model[model_key] = []
                        data_model[model_key].append([key, value])

        print('data_model:', data_model)

        return data_model

# main logic
data = Data('78735')
data.model_data()