import numpy as np
import pandas as pd
import itertools as iter
from tsfresh import extract_relevant_features, extract_features

#these are the different settings for the functions from tsfresh.feature_extraction import EfficientFCParameters, MinimalFCParameters, ComprehensiveFCParameters
class FeatureExtractor:

    fc_parameters = {}
    mouse_data = 0

    def __init__(self, feature_dict, md):
        self.fc_parameters = feature_dict
        self.mouse_data = md


    def getfewFeatures(self, mouse_id=165, signal_type='running', signal_treat='eth', slice_min=0):
        signal = self.mouse_data.fetch_mouse_signal(mouse_id, signal_treat, signal_type)
        signal = signal.sliced_data(slice_min=slice_min)
        signal = signal.get_pandas(time=True)

        id = np.repeat(1, len(signal))
        id[signal.iloc[:, 0] < 30] = 0

        #fc_parameters = MinimalFCParameters()

        signal.insert(0, "id", id, True)
        signal.columns = ["id", "time", signal_type]

        print(3)

        extracted_features = extract_features(signal, column_id='id', column_sort='time', column_value=signal_type, default_fc_parameters=self.fc_parameters)

        return extracted_features


    def getallFeatures(self, signal_type='running', slice_min=30, target = "treatment"):
        mouse_ids = {165, 166}
        mouse_map = list(iter.product(mouse_ids, self.mouse_data.treatments))
        collected_data = pd.DataFrame()

        for j in mouse_map:
            data_gen = self.mouse_data.fetch_mouse_signal(j[0], j[1], signal_type)
            data = data_gen.sliced_data(slice_min=slice_min)
            data = data.get_pandas(time=True)

            id = np.repeat(str(j[0]) + '_' + str(j[1]), len(data))
            data.insert(0, 'id', id, True)

            #all stacked in rows
            collected_data = pd.concat([collected_data, data], axis=0)

        target_map = [(str(x[0]) + '_' + str(x[1])) for x in mouse_map]
        target_y = [x.split("_")[1] for x in target_map]
        y = pd.Series(index=target_map, data=target_y)
        #classify treatment or no treatment
        if target == 'treatment':
            y[y.values != 'nea'] = 'treat'

        features_filtered_direct = extract_relevant_features(collected_data, y = y, column_id='id', column_sort='time_min', default_fc_parameters=self.fc_parameters)

        return features_filtered_direct