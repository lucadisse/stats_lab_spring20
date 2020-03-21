import data_scheduler.lib_data_merger as mice_data
from FeatureExtraction import getFeatures
from compareFeatures import plotFeatures

if __name__=='__main__':
    mice_data_dir = r'/Users/lucadisse/ETH/Master/FS20/StatsLab/CSV data files for analysis'
    md = mice_data.MiceDataMerger(mice_data_dir)
    data_eth_run = md.fetch_mouse_signal(166, 'eth', 'running')
    #print(data_eth_run.get_pandas())
    data_eth_run = data_eth_run.sliced_data(time=True, slice_min=30)


    #data_glu_run = md.fetch_mouse_signal(165, 'sal', 'running')
    #data_sal_run = md.fetch_mouse_signal(165, 'nea', 'running')

    #features = getFeatures(data_eth_run, print_feat=True)
    #print(features.shape[1])

    plotFeatures(md)

