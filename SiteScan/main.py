from SiteScan.Database import Database
from SiteScan.Pandas import PandaDataframe

def main():
    database = Database()
    database.API_fetch()
    database.model_data()
    database.print()
    database.save_data()
    print('done\n')
    panda = PandaDataframe()
    panda.load_dataframe()
    panda.to_percentages()
    panda.discretize()
    panda.bin_items()
main()