import numpy as np
import pandas as pd
import itertools as iter
from tsfresh import select_features
from tsfresh.utilities.dataframe_functions import impute
from tsfresh import extract_relevant_features

from tsfresh import extract_features
from tsfresh.feature_extraction import EfficientFCParameters, MinimalFCParameters

def getfewFeatures(data, print_feat=False, signal="left_brain_signal"):
    id = np.repeat(1, len(data))
    id[data.iloc[:, 0] < 30] = 0

    data.insert(0, "id", id, True)
    data.columns = ["id", "time", signal]
    extracted_features = extract_features(data, column_id='id', column_sort='time', column_value=signal, default_fc_parameters=MinimalFCParameters())
    if print_feat:
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(extracted_features)

    return extracted_features

def getallFeatures(mouse, signal='running', slice_min=30):
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

    #print(collected_data)
    #extracted_features = extract_features(collected_data[collected_data['treatment'] == 'eth'].drop(['treatment'], axis=1), column_id='mouse_id', column_sort='time_min')
    #features_filtered_direct = extract_relevant_features(collected_data, y = collected_data["treatment",], column_id='mouse_id', column_sort='time_min')

    target_map = [(str(x[0]) + '_' + str(x[1])) for x in mouse_map]
    target_y = [x.split("_")[1] for x in target_map]
    y = pd.Series(index = target_map, data = target_y)

    features_filtered_direct = extract_relevant_features(collected_data, y = y, column_id='id', column_sort='time_min')

    return collected_data