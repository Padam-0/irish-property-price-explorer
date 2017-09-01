import numpy as np
import pandas as pd
import math
import calendar
from time import time

from sklearn import ensemble
from sklearn.linear_model import LinearRegression
from sklearn.utils import shuffle
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.externals import joblib


def GradientBoost(X_train, y_train, X_test, y_test, model, model_type, old_df):
    # Start timing clock
    start = time()

    # Control the parameters of the model
    params = {'n_estimators':1200, 'max_depth':12, 'min_samples_leaf':12, 'learning_rate':0.025, 'loss':'huber'}

    # Import algorithm and fit to training data
    clf = ensemble.GradientBoostingRegressor(**params)
    clf.fit(X_train, y_train)

    # The mse of the resulting model is calculated
    mse = mean_squared_error(y_test, clf.predict(X_test))

    # The r2 sore of the resulting model is calculated
    y_pred = clf.predict(X_test)
    r2 = r2_score(y_test, y_pred)

    # Stop timing clock
    end = time()

    # Model results are printed to logfile
    with open('models/final_good_params_updated.csv', 'a') as file:
        file.write(str(params['n_estimators']) + ',' + str(params['max_depth']) + ',' +
                   str(params['min_samples_leaf']) + ',' + str(params['learning_rate']) + ',' +
                   params['loss'] + ',' + ("%.2f" % math.sqrt(mse)) + ',' + ("%.2f" % r2) + ',' +
                   ("%.2f" % (end - start)) + ',' + model)
        file.write('\n')

    # Export models as pickle files into models folder
    joblib.dump(clf, 'models/{}_model_{}_updated.pkl'.format(model.lower(), model_type.lower()))


def RandomForest(X_train, y_train, X_test, y_test, model, model_type):
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
                   ("%.4f" % math.sqrt(mse)) + ',' + ("%.4f" % r2) + ',' + ("%.4f" % (end-start))
                   + ',' + model + ',' + model_type)
        file.write('\n')


def lin_reg(X_train, y_train, X_test, y_test, model, model_type):
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
        file.write(("%.4f" % math.sqrt(mse)) + ',' + ("%.4f" % r2) + ',' + ("%.4f" % (end-start))
                   + ',' + model + ',' + model_type)
        file.write('\n')


# This function takes an integer and returns 5 is the integer is larger than 5
def room_transform(x):
    if x >=5:
        return 5
    else:
        return x


# This function manages the complete predictive model process
# The data set used, is not available in this repo
def main():
    # Import data
    df = pd.read_csv('model_data.csv', encoding='latin1', index_col=0)
    old_df = df

    # Reduce all bed/bath values into a 5+ bucket
    df['bed'] = df['bed'].apply(lambda x: room_transform(x))
    df['bath'] = df['bath'].apply(lambda x: room_transform(x))

    # Remove outliers
    df = df[df.price < 900000]
    df = df[df.price > 10000]

    # Data set is split into three seperate models
    models = ['Dublin', 'City', 'Rural']

    for model in models:
        new_df = df[df['model'] == model]

        # Transform categorical features to integer scale
        new_df.loc[:, 'county'] = pd.factorize(new_df.loc[:, 'county'])[0]
        new_df.loc[:, 'desc'] = pd.factorize(new_df.loc[:, 'desc'])[0]
        new_df.loc[:, 'condition'] = pd.factorize(new_df.loc[:, 'condition'])[0]
        new_df.loc[:, 'size'] = pd.factorize(new_df.loc[:, 'size'])[0]
        new_df.loc[:, 'region'] = pd.factorize(new_df.loc[:, 'region'])[0]
        new_df.loc[:, 'apt'] = pd.factorize(new_df.loc[:, 'apt'])[0]
        new_df.loc[:, 'house_name'] = pd.factorize(new_df.loc[:, 'house_name'])[0]
        new_df.loc[:, 'suffix'] = pd.factorize(new_df.loc[:, 'suffix'])[0]
        new_df.loc[:, 'ed'] = pd.factorize(new_df.loc[:, 'ed'])[0]

        # Transform date parameter
        new_df['sale_date'] = new_df['sale_date'].apply(pd.to_datetime)
        new_df['date'] = new_df['sale_date'].apply(lambda x: calendar.timegm(x.timetuple()))
        min_date = 1262304000
        new_df['date'] = new_df['date'].apply(lambda x: int((x - min_date)/86400))


        # Crate standalone target price dataframe
        price = new_df['price']

        # Unused features removed
        features = new_df.drop(['size', 'sale_date', 'price', 'address', 'region', 'model'
                            ], axis='columns')

        # Additional long/lat/ed features removed to build partial model
        features_partial = new_df.drop(['size', 'sale_date', 'price', 'address', 'region', 'model',
                                    'latitude', 'longitude', 'ed'], axis='columns')

        # Additional data feature removed to build time independent model
        features_ti = new_df.drop(['size', 'sale_date', 'price', 'address', 'region', 'model',
                                    'date'], axis='columns')

        # Additional long/lat/ed/date features removed to build partial model
        features_ti_part = new_df.drop(['size', 'sale_date', 'price', 'address', 'region', 'model',
                               'date', 'latitude', 'longitude', 'ed'], axis='columns')


        # The next section runs all/or a subset of algorithms

        ### Full Model ###

        # Data split into test/training sets
        X, y = shuffle(features, price, random_state=13)
        X = X.astype(np.float32)

        offset = int(X.shape[0] * 0.9)
        X_train, y_train = X[:offset], y[:offset]
        X_test, y_test = X[offset:], y[offset:]

        model_type = 'full'
        lin_reg(X_train, y_train, X_test, y_test, model, model_type)
        GradientBoost(X_train, y_train, X_test, y_test, model, model_type)
        RandomForest(X_train, y_train, X_test, y_test, model, model_type)

        ### Partial model ###

        # Data split into test/training sets
        X, y = shuffle(features_partial, price, random_state=13)
        X = X.astype(np.float32)

        offset = int(X.shape[0] * 0.9)
        X_train, y_train = X[:offset], y[:offset]
        X_test, y_test = X[offset:], y[offset:]

        model_type = 'partial'
        lin_reg(X_train, y_train, X_test, y_test, model, model_type)
        GradientBoost(X_train, y_train, X_test, y_test, model, model_type)
        RandomForest(X_train, y_train, X_test, y_test, model, model_type)

        ### Time Independent Model ###

        # Data split into test/training sets
        X, y = shuffle(features_ti, price, random_state=13)
        X = X.astype(np.float32)

        offset = int(X.shape[0] * 0.9)
        X_train, y_train = X[:offset], y[:offset]
        X_test, y_test = X[offset:], y[offset:]

        model_type = 'ti'
        lin_reg(X_train, y_train, X_test, y_test, model, model_type)
        GradientBoost(X_train, y_train, X_test, y_test, model, model_type, old_df)
        RandomForest(X_train, y_train, X_test, y_test, model, model_type)

        ### Partial Time Independent Model ###

        # Data split into test/training sets
        X, y = shuffle(features_ti_part, price, random_state=13)
        X = X.astype(np.float32)

        offset = int(X.shape[0] * 0.9)
        X_train, y_train = X[:offset], y[:offset]
        X_test, y_test = X[offset:], y[offset:]

        model_type = 'ti_part'
        lin_reg(X_train, y_train, X_test, y_test, model, model_type)
        GradientBoost(X_train, y_train, X_test, y_test, model, model_type)
        RandomForest(X_train, y_train, X_test, y_test, model, model_type)


if __name__ == '__main__':
    main()
