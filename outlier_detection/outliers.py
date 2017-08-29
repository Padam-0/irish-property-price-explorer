import pandas as pd

df = pd.read_csv('model_data.csv', encoding='latin1', index_col=0)

# stats = df[['ed', 'price']].groupby('ed').agg(['mean', 'std'])
stats = pd.read_csv('ed_mean_std.csv', encoding='latin1', index_col=0)

count = 0
counter = 0
for index, row in df.iterrows():
    if row['ed'] in stats.index:

        mean = stats.loc[row['ed'], 'mean']
        std = (stats.loc[row['ed'], 'std']*2)
        std3 = (std*1.5)

        if (row['price'] > (mean+std)) or (row['price'] < (mean-std)):
            df.loc[index, 'outlier_2std'] = 'Yes'
            df.loc[index, 'outlier_3std'] = 'No'
            df.loc[index, 'mean'] = mean
            df.loc[index, 'two_stds'] = std
            df.loc[index, 'three_stds'] = std3
            count += 1
            print('Count - 2 std: ', count)
        elif (row['price'] > (mean+std3)) or (row['price'] < (mean-std3)):
            df.loc[index, 'outlier_2std'] = 'Yes'
            df.loc[index, 'outlier_3std'] = 'Yes'
            df.loc[index, 'mean'] = mean
            df.loc[index, 'two_stds'] = std
            df.loc[index, 'three_stds'] = std3
            counter += 1
            print('Count - 3 std: ', counter)
        else:
            df.loc[index, 'outlier_2std'] = 'No'
            df.loc[index, 'outlier_3std'] = 'No'
            df.loc[index, 'mean'] = mean
            df.loc[index, 'two_stds'] = std
            df.loc[index, 'three_stds'] = std3

    else:
        df.loc[index, 'outlier_2std'] = 'NAN'
        df.loc[index, 'outlier_3std'] = 'NAN'
        df.loc[index, 'mean'] = 0
        df.loc[index, 'two_stds'] = 0
        df.loc[index, 'three_stds'] = 0

print("Total number of outliers (2 std): ", count)
print("Total number of outliers (3 std): ", counter)
print("Total number of rows: ", len(df.index))
df.to_csv('outliers_test.csv')
