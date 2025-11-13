from SiteScan.Model.Database import Database
from SiteScan.Model.Pandas import PandaDataframe
from SiteScan.Model.Supervised_Model import SupervisedModel

def main():
    print('starting Database.py...')
    database = Database()
    database.API_fetch()
    database.model_data()
    database.save_data()
    print('done\n')
    print('starting Pandas.py...')
    panda = PandaDataframe()
    panda.load_dataframe()
    panda.to_percentages()
    panda.discretize()
    panda.bin_items()
    print('done\n')
    print('starting Supervised_Model.py...')
    model = SupervisedModel()
    model.import_data()
    model.get_slopes()
    model.find_y()
    model.plot_linear_regression()
    print('done\n')
    return
main()