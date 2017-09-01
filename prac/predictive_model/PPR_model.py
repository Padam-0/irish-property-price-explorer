import numpy as np
import pandas as pd
import math
from time import time

from sklearn import ensemble
from sklearn.linear_model import LinearRegression
from sklearn.utils import shuffle
from sklearn.metrics import mean_squared_error, r2_score


def GradientBoost(X_train, y_train, X_test, y_test):
    # Start timing clock
    start = time()

    # Control the parameters of the model
    params = {'n_estimators': 200, 'max_depth': 150, 'min_samples_split': 10, 'min_samples_leaf': 1}

    # Import algorithm and fit to training data
    clf = ensemble.RandomForestRegressor(**params)
    clf.fit(X_train, y_train)

    # The mse of the resulting model is calculated
    mse = mean_squared_error(y_test, clf.predict(X_test))

    # The r2 sore of the resulting model is calculated
    r2 = r2_score(y_test, clf.predict(X_test))

    # Stop timing clock
    end = time()

    # Model results are printed to logfile
    with open('models/RF_params.csv', 'a') as file:
        file.write(str(params['n_estimators']) + ',' + str(params['max_depth']) + ',' +
                   str(params['min_samples_split']) + ',' + str(params['min_samples_leaf']) + ',' +
                   ("%.4f" % math.sqrt(mse)) + ',' + ("%.4f" % r2) + ',' + ("%.4f" % (end - start)))
        file.write('\n')


def Adaboost(X_train, y_train, X_test, y_test):
    # Start timing clock
    start = time()

    # Control the parameters of the model
    params = {'n_estimators': 1000, 'learning_rate': 00.1, 'loss': 'linear'}

    # Import algorithm and fit to training data
    clf = ensemble.AdaBoostRegressor(**params)
    clf.fit(X_train, y_train)

    # The mse of the resulting model is calculated
    mse = mean_squared_error(y_test, clf.predict(X_test))

    # The r2 sore of the resulting model is calculated
    r2 = r2_score(y_test, clf.predict(X_test))

    # Stop timing clock
    end = time()

    # Model results are printed to logfile
    with open('models/RF_params.csv', 'a') as file:
        file.write(str(params['n_estimators']) + ',' + str(params['learning_rate']) + ',' +
                   params['loss'] + ',' + ("%.4f" % math.sqrt(mse)) + ',' +
                   ("%.4f" % r2) + ',' + ("%.4f" % (end - start)))
        file.write('\n')


def RandomForest(X_train, y_train, X_test, y_test):
    # Start timing clock
    start = time()

    # Control the parameters of the model
    params = {'n_estimators':200, 'max_depth':150, 'min_samples_split': 10, 'min_samples_leaf':1}

    # Import algorithm and fit to training data
    clf = ensemble.RandomForestRegressor(**params)
    clf.fit(X_train, y_train)

    # The mse of the resulting model is calculated
    mse = mean_squared_error(y_test, clf.predict(X_test))

    # The r2 sore of the resulting model is calculated
    r2 = r2_score(y_test, clf.predict(X_test))

    # Stop timing clock
    end = time()

    # Model results are printed to logfile
    with open('models/RF_params.csv', 'a') as file:
        file.write(str(params['n_estimators']) + ',' + str(params['max_depth']) + ',' +
                   str(params['min_samples_split']) + ',' + str(params['min_samples_leaf']) + ',' +
                   ("%.4f" % math.sqrt(mse)) + ',' + ("%.4f" % r2) + ',' + ("%.4f" % (end-start)))
        file.write('\n')


def lin_reg(X_train, y_train, X_test, y_test):
    # Start timing clock
    start = time()

    # Import algorithm and fit to training data
    clf = LinearRegression()
    clf.fit(X_train, y_train)

    # The mse of the resulting model is calculated
    mse = mean_squared_error(y_test, clf.predict(X_test))

    # The r2 sore of the resulting model is calculated
    r2 = r2_score(y_test, clf.predict(X_test))

    # Stop timing clock
    end = time()

    # Model results are printed to logfile
    with open('models/LinReg_params.csv', 'a') as file:
        file.write(("%.4f" % math.sqrt(mse)) + ',' + ("%.4f" % r2) + ',' + ("%.4f" % (end-start)))
        file.write('\n')


def main():
    df = pd.read_csv('processed_data/PPR_model_data.csv')

    # Factories categorical data
    df.loc[:, 'desc'] = pd.factorize(df.loc[:, 'desc'])[0]
    df.loc[:, 'county'] = pd.factorize(df.loc[:, 'county'])[0]
    df.loc[:, 'suffix'] = pd.factorize(df.loc[:, 'suffix'])[0]
    df.loc[:, 'apt'] = pd.factorize(df.loc[:, 'apt'])[0]
    df.loc[:, 'ed'] = pd.factorize(df.loc[:, 'ed'])[0]

    # Remove size, new_used and desc from below when there's a better sample
    price = df['price']
    features = df.drop(['price','region', 'address'], axis='columns')

    # Data split into test/training sets
    X, y = shuffle(features, price, random_state=13)
    X = X.astype(np.float32)

    offset = int(X.shape[0] * 0.9)
    X_train, y_train = X[:offset], y[:offset]
    X_test, y_test = X[offset:], y[offset:]

    # The next section runs all/or a subset of algorithms
    LinearRegression(X_train, y_train, X_test, y_test)
    Adaboost(X_train, y_train, X_test, y_test)
    GradientBoost(X_train, y_train, X_test, y_test)
    RandomForest(X_train, y_train, X_test, y_test)






