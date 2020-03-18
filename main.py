import pandas as pd
import numpy as np


from importMouse import readSignal, plotSignal
from FeatureExtraction import getFeatures

data_eth = readSignal(slice_time=True).iloc[:,:2]
data_glu = readSignal(treat = "glu", date = "201119", slice_time=True).iloc[:,:2]

extracted_features_eth = getFeatures(data_eth)
extracted_features_glu = getFeatures(data_glu)