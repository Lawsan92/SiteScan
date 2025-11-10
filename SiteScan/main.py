from SiteScan.Database import Database
from SiteScan.Pandas import PandaDataframe

def main():
    # this updates ALL csv files

    database = Database()
    database.API_fetch()
    database.model_data()
    database.save_data()
    print('done\n')
    panda = PandaDataframe()
    panda.load_dataframe()
    panda.to_percentages(panda.dataframe)
    panda.fill_discretes()
    panda.filter_cont_cols()
    panda.bin_items()
    panda.save_binned_dataframe()
    panda.readd_keys()
    panda.save_dataframe()
main()

def main_2():
    panda = PandaDataframe()
    panda.load_dataframe()
    panda.to_percentages(panda.dataframe)
    panda.readd_keys()
    panda.save_data()

main_2()