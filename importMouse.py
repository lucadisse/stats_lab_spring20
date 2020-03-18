import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def readSignal(id = 165, treat = "eth", signal = "Brain_signal", date = "221019", slice_time = False, cut_min = 30):
    file_name = str(id) + "-" + str(treat) + "-" +"IG" + "-" + str(date) +  "_" + str(signal) + ".csv"
    data = pd.read_csv("/Users/lucadisse/ETH/Master/FS20/StatsLab/CSV data files for analysis/" + file_name)

    if slice_time:
        data = sliceTime(data, cut_min)
    print("Shape of data container:", np.shape(data))
    return data

def plotSignal(time, signal):
    plt.plot(time, signal)
    plt.show()

def sliceTime(data, cut_min = 30):
    data = data.to_numpy()
    data = data[data[:,0] > 30]
    return pd.DataFrame(data)
