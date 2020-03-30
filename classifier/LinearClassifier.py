from sklearn import linear_model
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import scale

class LinearClassifier:
    feature_block = pd.DataFrame()
    model = linear_model


    def __init__(self, features, model_type='logistic'):

        self.feature_block = features

        if model_type == 'logistic':
            self.model = linear_model.LogisticRegression(penalty='none')


    def validateClassifier(self,fit, X_test, y_test):
        y_out = fit.predict(X_test)
        out_df = pd.DataFrame({'real_y':y_test, 'predicted_y':y_out})
        print(out_df)


    #def CV_for_chunck_size(self):


    def classify(self):
        X = self.feature_block.iloc[:,1:len(self.feature_block.columns)-1]
        y = self.feature_block.iloc[:, -1]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 13)
        X_train = scale(X_train)
        X_test = scale(X_test)
        fit = self.model.fit(X_train, y_train)

        self.validateClassifier(fit, X_test, y_test)