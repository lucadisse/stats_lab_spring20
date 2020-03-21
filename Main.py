import data_scheduler.lib_data_merger as mice_data
from FeatureExtraction import getfewFeatures, getallFeatures
from compareFeatures import plotFeatures
import matplotlib.pyplot as plt

if __name__=='__main__':
    mice_data_dir = r'/Users/lucadisse/ETH/Master/FS20/StatsLab/CSV data files for analysis'
    md = mice_data.MiceDataMerger(mice_data_dir)
    data_eth_run = md.fetch_mouse_signal(166, 'eth', 'running')
    #print(data_eth_run.get_pandas())
    data_eth_run = data_eth_run.sliced_data(time=True, slice_min=30)


    #data_glu_run = md.fetch_mouse_signal(165, 'sal', 'running')
    #data_sal_run = md.fetch_mouse_signal(165, 'nea', 'running')

    #features = getfewFeatures(data_eth_run, print_feat=True)
    #print(features.shape[1])

    #plotFeatures(md)

    features = getallFeatures(md, signal='running', slice_min=30)
    #features[features['treatment'] == "glu"].plot(subplots=True, sharex=True, figsize=(10, 10))
    #plt.show()
    #print(features.columns)


