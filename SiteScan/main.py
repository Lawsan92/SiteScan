from SiteScan.Model.Database import Database
from SiteScan.Model.Pandas import PandaDataframe
from SiteScan.Model.Supervised_Model import SupervisedModel

def main(zip_code):

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
    print(f'zip code: {zip_code}')
    model = SupervisedModel(zip_code)
    model.import_data()
    model.get_slopes()
    model.find_y()
    payload = {
        'dataset': database,
        'linear_model': model.plot_linear_regression(),
        'linear_table': model.linear_regression_table(),
        'ksi': model.ksi_val()
    }
    print('sending linear regression payload to frontend...')
    print('done\n')
    return payload
# main(78735)