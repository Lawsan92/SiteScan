import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats

class SupervisedModel:
    data = None
    slopes = {}
    y = []

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

        print('slopes:', self.slopes)
        print('fitting linear regression model...')



    def plot_linear_regression(self):
        data = self.data
        x = data['Year']
        y = self.y
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        print('plotting linear regression model...')
        plt.scatter(x, y)
        plt.plot(x, intercept + slope * x, 'r')
        plt.xlabel('Store profits')
        plt.ylabel('Year')
        plt.title('Store profits vs. Year')
        plt.savefig('csv/linear_regression_model.png')
        plt.show()

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
        print('y values:', self.y)

        return

    def import_data(self):
        print('importing data...')
        self.data = pd.read_csv('csv/grouped_dataset_percentages.csv', skiprows=[1], usecols=range(1, 8))

# def main():
#     model = SupervisedModel()
#     model.import_data()
#     model.get_slopes()
#     model.find_y()
#     model.plot_linear_regression()
#     return
#
# main()