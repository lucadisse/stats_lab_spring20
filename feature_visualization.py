import data_scheduler.lib_data_merger as mice_data
from FeatureExtraction import getfewFeatures, getallFeatures
from compareFeatures import plotFeatures
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tsfresh import extract_features

fc_parameters = {
    "large_standard_deviation": [{"r": 0.05}, {"r": 0.1}],
    "abs_energy": None,
    "autocorrelation": [{"lag": 3}],
    "variance": None,
    "number_peaks": [{"n": 10}],
    "count_above_mean": None,
    "longest_strike_below_mean": None,
    "mean": None,
    "maximum": None,
    "median": None,
    "variance": None
}

def plotFeatures(mouse, signal_type, brain_half = 'left', mouse_ids = [165, 166], treatments = ['glu', 'eth', 'sal', 'nea']):
    feature_data = dataPreparation(mouse, signal_type, brain_half, mouse_ids, treatments)
    print(feature_data)

def dataPreparation(mouse, signal_type, brain_half, mouse_ids, treatments):
    if brain_half == 'right':
        column_value = md.col_names[signal_type][2]
    else:
        column_value = md.col_names[signal_type][1]
    mouse_ids = mouse_ids
    helper = []
    for j in mouse_ids:
        for i in treatments:
            signal = mouse.fetch_mouse_signal(j, i, signal_type)
            chunks = signal.partition_data(part_last=30, remove_shorter = True)
            n = 1
            id = []
            for chunk in chunks:
                df = chunk.get_pandas(time=True)
                if n < 10:
                    chunk_id = str(j)+'.'+str(treatments.index(i)+1)+'.0'+str(n)
                else:
                    chunk_id = str(j)+'.'+str(treatments.index(i)+1)+'.'+str(n)
                n += 1
                chunk_id = np.repeat(chunk_id, len(df))
                id = np.append(id,chunk_id)
            chunk_data = signal.get_pandas()[0:len(id)]
            chunk_data.insert(0, "id", id, True)
            extracted_features = extract_features(chunk_data, column_id='id', column_sort='time_min',
                                                  column_value= column_value,
                                                  default_fc_parameters=fc_parameters)
            helper.append(extracted_features)
    feature_data = pd.concat(helper)
    return(feature_data)



'''for i in colnames:
     helper.append(extracted_features.iloc[:,i])'''
# feature_dataframe[i] = extracted_features.iloc[:,colnames.index(i)] #helper.append(extracted_features.iloc[:,colnames.index(i)])
# print(feature_dataframe)
# feature_dataframe.append(extracted_features)
# colnames = list(extracted_features.columns)
if __name__=='__main__':
    mice_data_dir = r'C:\Users\marce\OneDrive - ETHZ\Education\ETH\Spring 2020\Statslab\Project_Neuroscience\dataset'
    md = mice_data.MiceDataMerger(mice_data_dir)
    plotFeatures(md, 'brain_signal')
#print(len(data_eth.get_pandas()))
    '''id = np.repeat(1, len(data_eth.get_pandas()))
    id[data_eth.get_pandas().iloc[:, 0] < 30] = 0
    #print(id)
    data_eth.get_pandas().insert(0, "id", id, True)
    data_eth.get_pandas().columns = ["id", "time", 'neu_act_1', 'neu_act_2']
    extracted_features = extract_features(data_eth.get_pandas(), column_id='id', column_sort='time', column_value='neu_act_1',
                                          default_fc_parameters=fc_parameters)
    print(extracted_features)'''
'''    signal = md.fetch_mouse_signal(165, 'eth', 'brain_signal')
    signal = signal.sliced_data(29.997)
    chunks = signal.partition_data(part_last=5, remove_shorter = True)
    n = 1
    id = []
    for chunk in chunks:
        df = chunk.get_pandas(time=True)
        if n < 10:
            chunk_id = str(1)+'.'+str(1)+'.0'+str(n)
        else:
            chunk_id = str(1)+'.'+str(1) + '.' + str(n)
        n += 1
        chunk_id = np.repeat(chunk_id, len(df))
        id = np.append(id,chunk_id)
    signal = signal.get_pandas()[0:len(id)]
    signal.insert(0, "id", id, True)
    names = md.col_names['brain_signal']
    names.insert(0, 'id')
    signal.columns = names
    extracted_features = extract_features(signal, column_id='id', column_sort='time_min',
                                          column_value='neu_act_1',
                                          default_fc_parameters=fc_parameters)
    print(extracted_features)'''



'''def getfewFeatures(data, print_feat=False, signal="neu_act_1"):
    id = np.repeat(1, len(data))
    id[data.iloc[:, 0] < 30] = 0

    #fc_parameters = MinimalFCParameters()
    fc_parameters = {
        "large_standard_deviation": [{"r": 0.05}, {"r": 0.1}],
        "abs_energy": None,
        "autocorrelation": [{"lag" : 3}],
        "variance": None,
        "number_peaks": [{"n" : 10}],
        "count_above_mean": None,
        "longest_strike_below_mean": None,
        "mean": None,
        "maximum": None,
        "median": None,
        "variance" : None
    }

    data.insert(0, "id", id, True)
    data.columns = ["id", "time", signal]
    extracted_features = extract_features(data, column_id='id', column_sort='time', column_value=signal, default_fc_parameters=fc_parameters)
    if print_feat:
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(extracted_features)

    return extracted_features'''
