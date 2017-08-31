"""
Script to split a data set into smaller chunks of 25000 so it can be processed in parallel

"""

import pandas as pd

# Import data set
df = pd.read_csv('good_data.csv', encoding='latin1', index_col=0)
print(len(df.index))

count = 0

for i in range(0, len(df.index), 25000):
    count += 1
    start_row = i
    if i != 175000:
        end_row = i + 25000
    else:
        end_row = len(df.index)

    df_new = df.iloc[start_row:end_row, :]

    df_new.to_csv('good_data_{}.csv'.format(count))
    print(count)
    print(len(df_new.index))
