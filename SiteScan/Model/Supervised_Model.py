import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import base64
from io import BytesIO
import os
from SiteScan.settings import BASE_DIR

class SupervisedModel:
    data = None
    slopes = {}
    y = []
    base_path = os.path.join(BASE_DIR, 'SiteScan/csv/')

    def __init__(self, user_zip=None):
        self.zip = int(user_zip)

    def import_data(self):
        print('importing data...')
        self.data = pd.read_csv(os.path.join(self.base_path, 'grouped_dataset_percentages.csv'), usecols=range(1, 8))

        self.data = self.data[self.data['Zip Code'] == self.zip]
        self.data = self.data.iloc[1:]
        self.data = self.data.reset_index(drop=True)

    def get_slopes(self):
        data = self.data
        x = data['Year']
        y = data['Population_pct_change']

        for key, dataset in data.items():
            if key == 'Year' or key == 'Zip Code':
                continue
            y = dataset
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            self.slopes[key] = slope
        print('fitting linear regression model...')

    def find_y(self):
        print('finding y values...')
        slopes = self.slopes
        y = []
        for key, dataset in self.data.items():
            if key == 'Year' or key == 'Zip Code':
                continue
            for i, item in enumerate(dataset):
                try:
                    y[i] = y[i] + item * slopes[key]
                except IndexError as e:
                    y.append(0)
        self.y = y

    def plot_linear_regression(self):
        print('plotting linear regression...')
        data = self.data
        x = data['Year']
        y = self.y
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        print('plotting linear regression model...')
        plt.scatter(x, y)
        plt.title(f'Store profits for {self.zip}')
        plt.xlabel('Year')
        plt.ylabel('Store profits (%)')
        plt.plot(x, intercept + slope * x, 'r')
        # plt.show()

        buffer_file = BytesIO()
        plt.savefig( buffer_file, format='png')
        graph_buffer_file_base64 = base64.b64encode(buffer_file.getvalue())
        graph_buffer_file_html = graph_buffer_file_base64.decode('utf-8')
        graph_html = '<img src=\'data:image/png;base64,{}\'>'.format(graph_buffer_file_html)
        plt.close()
        return graph_html

    def linear_regression_table(self):
        print('generating linear regression table...')
        x = self.data['Year']
        y = self.y
        col_labels = ['Year', 'Store Profits (%)']

        # Data for the table
        table_data = []

        for index, item in enumerate(y):
            year = x[index]
            item = round(y[index], 2)
            table_data.append([year, item])

        # Create a figure and axes
        fig, ax = plt.subplots(figsize=(6, 3))

        # Hide the axes to display only the table
        ax.axis('off')
        ax.axis('tight')  # Adjust limits to fit the table

        # Create the table fig
        ax.table(cellText=table_data, colLabels=col_labels, loc='center', cellLoc='center')
        ax.set_title(f'Store profits for {self.zip}')

        # convert table fig to html markdown
        table_file = BytesIO()
        fig.savefig(table_file, format='png')
        table_file_encoded = base64.b64encode(table_file.getvalue()).decode('utf-8')
        table_html = '<img src=\'data:image/png;base64,{}\'>'.format(table_file_encoded)
        plt.close()
        return table_html

    def ksi_val(self):
        print('calculating KSI value...')
        y = self.y
        y_sum = 0
        n = len(y)

        for i in y:
            print('i:', i)
            y_sum += i
        return round(y_sum/n, 2)

def main():
    model = SupervisedModel(78735)
    model.import_data()
    model.get_slopes()
    model.find_y()
    model.plot_linear_regression()
    model.linear_regression_table()
    model.ksi_val()
    return

main()