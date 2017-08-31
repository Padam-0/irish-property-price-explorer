import pandas as pd

# Import Dataset
df = pd.read_csv('<>.csv', encoding='latin1', index_col=0)

# Properties grouped by electoral division and the mean and standard deviation
# of each is calculated
stats = df[['ed', 'price']].groupby('ed').agg(['mean', 'std'])

# Mean and standard deviation info added to each property
for index, row in df.iterrows():
    if row['ed'] in stats.index:
        mean = stats.loc[row['ed'], 'mean']
        std = stats.loc[row['ed'], 'std']

        df.loc[index, 'mean'] = mean
        df.loc[index, 'std'] = std
    else:
        df.loc[index, 'mean'] = 'NaN'
        df.loc[index, 'two_stds'] = 'NaN'

# Updated data exported to CSV
df.to_csv('outlier_data.csv')

# Mean and standard deviation information exported to CSV
stats.to_csv('ed_mean_std.csv')
