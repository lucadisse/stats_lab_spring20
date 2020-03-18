import numpy as np
import pandas as pd
from tsfresh import select_features
from tsfresh.utilities.dataframe_functions import impute
from tsfresh import extract_relevant_features

from tsfresh import extract_features
from tsfresh.feature_extraction import EfficientFCParameters, MinimalFCParameters

def getFeatures(data):
    # plotSignal(time, left_brain_signal)
    id = np.repeat(1, len(data))
    id[data.iloc[:, 0] < 30] = 0

    data.insert(0, "id", id, True)
    data.columns = ["id", "time", "left_brain_signal"]
    print(data)
    extracted_features = extract_features(data, column_id='id', column_sort='time', column_value="left_brain_signal")#default_fc_parameters=MinimalFCParameters())
    print(np.shape(extracted_features))
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(extracted_features)

    return extracted_features