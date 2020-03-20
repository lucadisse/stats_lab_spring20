import os
import pandas as pd
import re
import numpy


class DataFrame:

    def __init__(self, df, signal_type):
        if df is None:
            raise ValueError('Provided None as data frame is illegal')
        if signal_type is None or signal_type not in MiceDataMerger.signals:
            raise ValueError('{0} was provided as signal type which is illegal type of signal'.format('signal_type'))

        self.df = df
        self.freq = MiceDataMerger.data_freq[signal_type]

    def get_pandas(self, time=True):
        data = self.df
        if not time:
            col_names = list(data.columns)
            col_names.remove('time_min')
            data = data[col_names]

        return data

    def sliced_data(self, time=False, slice_min=0):
        if slice_min < 0:
            raise ValueError('{0} as number of slices is illegal argument'.format(slice_min))

        data = self.df
        if slice_min:
            data = data[data["time_min"] > 30]

        if not time:
            col_names = list(data.columns)
            col_names.remove('time_min')
            data = data[col_names]

        return data


class DataMerger:

    def __init__(self, dir):
        if dir is None:
            raise ValueError('Directory path can not be None')
        if not os.path.isdir(dir):
            raise ValueError('Inexistent directory provided')

        self.dir = dir

    def merge_data(self):
        pass

    def get_data(self, **kwargs):
        pass


class MiceDataMerger(DataMerger):
    treatments = set(['glu', 'eth', 'sal', 'sal'])
    signals = set(['brain_signal', 'running', 'V_O2', 'V_CO2', 'RQ', 'Heat'])

    data_freq = {
        'brain_signal': 10,
        'running': 10,
        'V_O2': 1,
        'V_CO2': 1,
        'RQ': 1,
        'Heat': 1
    }

    col_names = {
        'brain_signal': ['time_min', 'neu_act_1', 'neu_act_2'],
        'running': ['time_min', 'run_cm_s'],
        'V_O2': ['time_min', 'lit_min'],
        'V_CO2': ['time_min', 'lit_min'],
        'RQ': ['time_min', 'exc'],
        'Heat': ['time_min', 'cal_min']
    }

    file_regex = r'([0-9]+)-(glu|eth|res)-IG-[0-9]+_(Brain_signal|Heat|RQ|Running|V_CO2|V_O2).csv'

    def __init__(self, dir):
        super().__init__(dir)
        self.mouse_data_file_map = {}
        self.preprocess_dir()

    def preprocess_dir(self):
        for file in os.listdir(self.dir):
            res = re.match(MiceDataMerger.file_regex, file)
            if res is None or res.group(1) is None:
                continue

            mouse_data_id = (int(res.group(1)), res.group(2), res.group(3).lower())
            if mouse_data_id in self.mouse_data_file_map:
                #TODO
                pass

            self.mouse_data_file_map[mouse_data_id]=os.path.join(self.dir, file)

    def merge_data(self):
        pass

    def fetch_mouse_signal(self, mouse_id, treat, signal):
        if mouse_id is None or treat is None or treat not in MiceDataMerger.treatments \
                or signal is None or signal.lower() not in MiceDataMerger.signals:
            raise ValueError('Invalid (mouse ID, treatment, signal) combination: ({0}, {1}, {2})'.format(mouse_id, treat, signal.lower()))

        signal = signal.lower()
        mouse_signal_file_id = (mouse_id, treat, signal)
        if mouse_signal_file_id not in self.mouse_data_file_map:
            raise ValueError('Invalid (mouse ID, treatment, signal) combination: ({0}, {1}, {2})'.format(mouse_id, treat, signal))

        return DataFrame(pd.read_csv(self.mouse_data_file_map[mouse_signal_file_id], names=MiceDataMerger.col_names[signal]), signal)

    def fetch_mouse_data(self, mouse_id, treat, signals):
        if mouse_id is None or treat is None \
                or treat not in MiceDataMerger.treatments \
                or signals is None or len(signals) <= 0:
            return None

        return self.load_mouse_signal(mouse_id, treat, signals[0])

    def get_data(self, **kwargs):
        """
        :param kwargs:mouse_id,treat,list of signals,split_num,treatment/whole_data/non_treatment
        :return:
        """
        if 'mouse_id' not in kwargs:
            raise ValueError('Mouse ID not provided')
        if 'treat' not in kwargs:
            raise ValueError('Treatment type not provided')
        if 'signals' not in kwargs or kwargs['signals'] is None or len(kwargs['signals']) <= 0:
            raise ValueError('Signal list not provided')

        data = self.fetch_mouse_data(mouse_id=kwargs['mouse_id'],
                                     treat=kwargs['treat'],
                                     signals=kwargs['signals'])
        return data
