import os
import pandas as pd
import re


class DataFrame:

    def __init__(self, df, signal_type, chunks = None):
        if df is None:
            raise ValueError('Provided None as data frame is illegal')
        if signal_type is None or signal_type not in MiceDataMerger.signals:
            raise ValueError('{0} was provided as signal type which is illegal type of signal'.format('signal_type'))
        if chunks is None:
            chunks = [(df['time_min'].min(), df['time_min'].max())]

        self.df = df
        self.freq = MiceDataMerger.data_freq[signal_type]
        self.chunks = chunks
        self.signal_type = signal_type

    def get_pandas(self, time=True):
        data = self.df
        if not time:
            col_names = list(data.columns)
            col_names.remove('time_min')
            data = data[col_names]

        return data

    def sliced_data(self, slice_min=0):
        if slice_min < 0:
            raise ValueError('{0} as number of slices is illegal argument'.format(slice_min))

        data = self.df
        if slice_min:
            data = data[data["time_min"] >= slice_min]

        i = 0
        while i < len(self.chunks) and self.chunks[i][1] < slice_min:
            i+=1
        new_chunks = self.chunks[i:]
        new_chunks[0] = (max(new_chunks[0][0], slice_min), new_chunks[0][1])

        return DataFrame(data, self.signal_type, chunks=new_chunks)

    def leave_out_chunk(self, time_tuple):
        if time_tuple is None:
            raise ValueError('Leave out chunk is not supposed to be None value')

        start_time, end_time = time_tuple
        if start_time is None or end_time is None:
            raise ValueError('None values provided as time stamps')

        if start_time > end_time:
            start_time, end_time = end_time, start_time

        data = self.df
        data = data[(data['time_min'] <= start_time) | (data['time_min'] >= end_time)]

        new_chunks = []
        for i in range(0, len(self.chunks)):
            s, e = self.chunks[i]
            if s >= start_time and e <= end_time:
                continue
            elif start_time > s and end_time < e:
                s1, e1 = s, start_time
                s2, e2 = end_time, e
                new_chunks.append((s1, e1))
                new_chunks.append((s2, e2))
                continue
            elif start_time >= s:
                e = min(start_time, e)
            elif end_time <= e:
                s = max(s, end_time)

            new_chunks.append((s, e))

        return DataFrame(data, self.signal_type, chunks=new_chunks)

    def leave_out_chunks(self, leave_out):
        if leave_out is None or len(leave_out) <=0:
            raise ValueError('Provided invalid array of leave_out chunks')

        df = self
        for leave_out_int in leave_out:
              df = df.leave_out_chunk(leave_out_int)

        return df

    def partition_data(self, part_last, remove_shorter = False):
        if part_last <=0:
            raise ValueError('{0} as partition lasting time is not legal value'.format(part_last))
        if 'time_min' not in list(self.df):
            raise ValueError('Can not partition data frame by time because there is not time column in it')

        chunked_data = []
        for chunk in self.chunks:
            start, end = chunk

            s = start
            while s+part_last <= end:
                chunked_data.append(DataFrame(self.df[(self.df['time_min'] >= s) & (self.df['time_min'] < s+part_last)], self.signal_type, [(s, s+part_last)]))
                s+=part_last

            if not remove_shorter:
                chunked_data.append(DataFrame(self.df[(self.df['time_min'] >= s) & (self.df['time_min'] < end)], self.signal_type, [(s, end)]))

        return chunked_data

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
    treatments = set(['glu', 'eth', 'sal', 'nea'])
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

    file_regex = r'([0-9]+)-(glu|eth|nea|sal)-IG-[0-9]+_(Brain_signal|Heat|RQ|Running|V_CO2|V_O2).csv'
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
