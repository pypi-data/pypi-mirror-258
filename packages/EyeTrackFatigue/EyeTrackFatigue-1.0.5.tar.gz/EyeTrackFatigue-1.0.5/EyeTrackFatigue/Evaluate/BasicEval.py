from Evaluate.Evaluator import Evaluator
import numpy as np
class BasicEval(Evaluator):
    def __init__(self):
        self.tired = []
        self.fresh = []
        self.corrs = []
    
    def get_name(self):
        return 'Basic'

    def edu(self, train_X, train_Y, test_X, test_Y):
        self.tired = [0] * len(train_X.head(1))
        self.fresh = [0] * len(train_X.head(1))
        tired_count = 0
        fresh_count = 0
        self.corrs = []
        for col in train_X.columns:
            Sum_xy = sum((train_X[col]-train_X[col].mean())*(train_Y[train_Y.columns[0]]-train_Y[train_Y.columns[0]].mean()))
            Sum_x_squared = sum((train_X[col]-train_X[col].mean())**2)
            Sum_y_squared = sum((train_Y[train_Y.columns[0]]-train_Y[train_Y.columns[0]].mean())**2)       
            self.corrs.append(Sum_xy / np.sqrt(Sum_x_squared * Sum_y_squared))
        '''
        for i, row in train_X.iterrows():
            if train_Y.iloc[i][0] == 0:
                tired_count += 1
                self.tired += row.tolist()
            else:
                fresh_count += 1
                self.fresh += row.tolist()
        for i in range(len(self.tired)):
            self.tired[i] /= tired_count
            self.fresh[i] /= fresh_count
        '''

    def evaluate(self, data):
        pred_Y = []
        for _, row in data.iterrows():
            fl = 0
            for i in range(len(row)):
                fl += row[i] * self.corrs[i]
                #fl += 1 if abs(row[i] - self.tired[i]) < abs(row[i] - self.fresh[i]) else -1
            pred_Y.append(0 if fl < 0 else 1)
        return pred_Y
            
