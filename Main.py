import data_scheduler.lib_data_merger as mice_data
from FeatureExtraction import getFeatures

if __name__=='__main__':
    mice_data_dir = r'/Users/lucadisse/ETH/Master/FS20/StatsLab/CSV data files for analysis'
    md = mice_data.MiceDataMerger(mice_data_dir)
    data = md.fetch_mouse_signal(165, 'eth', 'running')
    print(data.get_pandas())
    sliced_data = data.sliced_data(time=True, slice_min=30)

    features = getFeatures(sliced_data, print_feat=True)