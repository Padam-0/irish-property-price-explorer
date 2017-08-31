import pandas as pd
import numpy as np


def exact_duplicates(df):
    # Removing Exact Duplicates
    df_dups = df[df.duplicated(['sale_date', 'address', 'price'])==True].sort_values(by='address')
    print(df_dups.iloc[0:5,:])

    dups_to_drop = df_dups.index

    print(dups_to_drop)
    print(type(dups_to_drop))


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


if __name__ == '__main__':
    main()