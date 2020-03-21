import numpy as np
import pandas as pd
from tsfresh import select_features
from tsfresh.utilities.dataframe_functions import impute
from tsfresh import extract_relevant_features

from tsfresh import extract_features
from tsfresh.feature_extraction import EfficientFCParameters, MinimalFCParameters

def getFeatures(data, print_feat=False):
    id = np.repeat(1, len(data))
    id[data.iloc[:, 0] < 30] = 0

    data.insert(0, "id", id, True)
    data.columns = ["id", "time", "left_brain_signal"]
    extracted_features = extract_features(data, column_id='id', column_sort='time', column_value="left_brain_signal", default_fc_parameters=MinimalFCParameters())
    if print_feat:
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(extracted_features)

    return extracted_features

#def getallFeatures(mouse, signal='running'):
#    mouse_ids = [165, 166, 67]#
#
#    for i in mouse.treatments:
#        for j in mouse_ids:
#            data_gen = mouse.fetch_mouse_signal(mouse_id, i, signal)
#            data = data_gen.sliced_data(time=True, slice_min=30)
#            features = getFeatures(data)
#            features["treatment"] = i
#            features["mouse_id"] = j
#            general_features = pd.concat([general_features, features], axis=0)
