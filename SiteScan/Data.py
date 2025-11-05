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

        # draw the line graph
        plt.figure(figsize=(10, 6))
        plt.title('Population of 78735')
        plt.xlabel('Year')
        plt.ylabel('Population (in thousands)')
        plt.plot(year_list, population_list, color='blue')

        # convert graph to base64 image and inject in html <img> template
        graph_file = BytesIO()
        plt.savefig(graph_file, format='png')
        graph_file_encoded = base64.b64encode(graph_file.getvalue()).decode('utf-8')

        graph_html = '<html>' + '<img src=\'data:image/png;base64,{}\'>'.format(graph_file_encoded) + '</html>'
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

        table_html = '<html>' + '<img src=\'data:image/png;base64,{}\'>'.format(table_file_encoded) + '</html>'

        return table_html
