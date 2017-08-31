import pandas as pd


def above_x_stds(df, num):
    """
    Following code allows the user to isolate groups of properties above a specified number of
    standard deviations. Human review is required before properties are removed from the data set.

    """

    df = df[df['price'] > (df['mean'] - (df['std']*num))]
    print("Number of properties above {} std: {}".format(num, len(df)))

    # Remove properties listed as not full market price
    df = df[df['nfma'] == 'No']
    print(df.head())

def below_x_stds(df, num):
    """
    Following code allows the user to isolate groups of properties below a specified number of
    standard deviations. Human review is required before properties are removed from the data set.

    """

    df = df[df['price'] < (df['mean'] - (df['std'] * num))]
    print("Number of properties below {} std: {}".format(num, len(df)))

    # Remove properties listed as not full market price
    df = df[df['nfma'] == 'No']
    print(df.head())


def main():
    # Import outlier data
    df = pd.read_csv('outlier_data.csv', index_col=0)

    # Remove null values from electoral division column and drop columns not required
    df['ed_null'] = pd.isnull(df['ed'])
    df = df[df['ed_null'] == False]
    df.drop(['postcode', 'vat_ex', 'DoP', 'PSD', 'region', 'latitude',
             'longitude', 'ed_null'], axis=1, inplace=True)

    # Remove known outliers - If there are any
    try:
        bad_data = pd.read_csv('known_outliers.csv', index_col=0)
        for i, k in df.iterrows():
            if i in bad_data.index:
                df.drop(i, inplace=True)
    except:
        pass

    # Fuctions to look at properties above or below a specified number of standard deviations from the mean
    # Default: 2
    above_x_stds(df, 2)
    below_x_stds(df, 2)


if __name__ == '__main__':
    main()