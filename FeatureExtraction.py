import numpy as np
import pandas as pd
import itertools as iter
from tsfresh import select_features
from tsfresh.utilities.dataframe_functions import impute
from tsfresh import extract_relevant_features

from tsfresh import extract_features

#these are the different settings for the functions
from tsfresh.feature_extraction import EfficientFCParameters, MinimalFCParameters, ComprehensiveFCParameters

def getfewFeatures(data, print_feat=False, signal="left_brain_signal"):
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

    return extracted_features

def getallFeatures(mouse, signal='running', slice_min=30, target = "treatment"):
    mouse_ids = {165, 166}
    mouse_map = list(iter.product(mouse_ids, mouse.treatments))
    collected_data = pd.DataFrame()

    for j in mouse_map:
        data_gen = mouse.fetch_mouse_signal(j[0], j[1], signal)
        data = data_gen.sliced_data(time=True, slice_min=slice_min)

        id = np.repeat(str(j[0]) + '_' + str(j[1]), len(data))
        data.insert(0, 'id', id, True)

        #all stacked in rows
        collected_data = pd.concat([collected_data, data], axis=0)

    #extracted_features = extract_features(collected_data[collected_data['treatment'] == 'eth'].drop(['treatment'], axis=1), column_id='mouse_id', column_sort='time_min')

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

    target_map = [(str(x[0]) + '_' + str(x[1])) for x in mouse_map]
    target_y = [x.split("_")[1] for x in target_map]
    y = pd.Series(index=target_map, data=target_y)
    #classify treatment
    if target == 'treatment':
        y[y.values != 'nea'] = 'treat'

    print(y)
    features_filtered_direct = extract_relevant_features(collected_data, y = y, column_id='id', column_sort='time_min', default_fc_parameters=fc_parameters)

    return features_filtered_direct