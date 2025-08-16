import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score
import pickle

class SVMModel:
    def __init__(self, dataset_path='diabetes.csv'):
        self.dataset = pd.read_csv(dataset_path)
        self.model = None
        self.scaler = StandardScaler()

    def train(self):
        X = self.dataset.drop(columns='Outcome', axis=1)
        Y = self.dataset['Outcome']
        self.scaler.fit(X)
        X = self.scaler.transform(X)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, stratify=Y, random_state=2)
        self.model = svm.SVC(kernel='linear')
        self.model.fit(X_train, Y_train)
        train_accuracy = accuracy_score(Y_train, self.model.predict(X_train))
        test_accuracy = accuracy_score(Y_test, self.model.predict(X_test))
        print(f'Training Accuracy: {train_accuracy}')
        print(f'Test Accuracy: {test_accuracy}')
        with open('svm_model.pkl', 'wb') as f:
            pickle.dump((self.model, self.scaler), f)

if __name__ == "__main__":
    svm_model = SVMModel()
    svm_model.train()
