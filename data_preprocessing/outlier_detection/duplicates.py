import pandas as pd
import numpy as np
import re


def exact_duplicates(df):
    # Removing Exact Duplicates
    df_dups = df[df.duplicated(['sale_date', 'address', 'price'])==True].sort_values(by='address')

    # Exact duplicate IDs isolated
    dups_to_drop = df_dups.index


def address_date_duplicates(df):
    """
    As it is difficult to confidently obtain true duplications of address and price repeats
    none of the properties isolated are removed from the data set. Human review is required
    before properties are removed from the data set.

    """

    # Date column converted to datetime type
    df['sale_date'] = pd.to_datetime(df['sale_date'])

    # Duplicate properties isolated, sorted by address and sale date
    df_dups = df[df.duplicated(['address', 'price'], keep=False) == True].sort_values(by=['address', 'sale_date'])

    # Earliest sale date in the data set isolated
    min_date = df_dups['sale_date'].min()

    # Each sale date converted to integer based on the number of days it is away from min_date
    df_dups['date_int'] = (df_dups['sale_date'] - min_date).dt.days

    # Date delta calculated
    df_dups['date_delta'] = df_dups.groupby(['address'])['date_int'].diff()

    # Lambda function to highlight the properties of interested, based on a maximum delta gap
    # Default: 7 days
    df_dups['duplicates_of_interest'] = df_dups['date_delta'].apply(lambda x: 1 if x < 7 else 0)



def address_price_duplicates(df, stats):
    """
    As it is difficult to confidently obtain true duplications of address and price repeats
    none of the properties isolated are removed from the data set. Human review is required
    before properties are removed from the data set.

    """

    # Dataframe of duplicate addresses and sale dates filtered, sorted by address and price
    df_dups = df[df.duplicated(['address', 'sale_date'], keep=False) == True].sort_values(by=['address', 'price'])

    # Price differences calculated for all duplicate properties
    df_dups['price_delta'] = df_dups.groupby(['address'])['price'].diff()

    # Electoral division mean is added to each property
    for i, x in df_dups.iterrows():
        if x['ed'] in stats.index:
            mean = stats.ix[x['ed'], 'mean']
            df_dups.ix[i, 'ed_mean'] = int(mean)

    # Price delta calculated
    df_dups['price_delta'] = abs(df_dups['price'] - df_dups['ed_mean'])



def date_price_duplicates(df):
    """
    As it is difficult to confidently obtain true duplications of date and price repeats
    none of the properties isolated are removed from the data set. Human review is required
    before properties are removed from the data set.

    """
    # Dataframe of duplicate price, sale dates and electoral division filtered, sorted by sale date and price
    df_dups = df[df.duplicated(['price', 'sale_date', 'ed']) == True].sort_values(by=['sale_date', 'price'])

    # Strip the house/apartment number from the beginning of the address
    df_dups['address_strip'] = df_dups['address'].apply(lambda x: int_strip(x))


def int_strip(s):
    return re.sub(r'\d+', '', s)


def main():
    # Import outlier data
    df = pd.read_csv('outlier_data.csv', index_col=0)

    # Remove known outliers - If there are any
    try:
        bad_data = pd.read_csv('known_outliers.csv', index_col=0)
        for i, k in df.iterrows():
            if i in bad_data.index:
                df.drop(i, inplace=True)
    except:
        pass

    # Import mean and standard deviation information for each electoral division
    stats = pd.read_csv('ed_mean_std.csv', index_col=0)

    # Functions to isolate duplicates
    exact_duplicates(df)
    address_date_duplicates(df)
    address_price_duplicates(df, stats)
    date_price_duplicates(df)


if __name__ == '__main__':
    main()