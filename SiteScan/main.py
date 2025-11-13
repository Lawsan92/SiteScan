from SiteScan.Database import Database
from SiteScan.Pandas import PandaDataframe
from SiteScan.Supervised_Model import SupervisedModel

def main():
    print('starting...')
    database = Database()
    database.API_fetch()
    database.model_data()
    database.save_data()
    print('done\n')
    panda = PandaDataframe()
    panda.load_dataframe()
    panda.to_percentages()
    panda.discretize()
    panda.bin_items()
    print('done\n')
    model = SupervisedModel()
    model.import_data()
    model.get_slopes()
    model.find_y()
    model.plot_linear_regression()
    print('done\n')
    return
main()