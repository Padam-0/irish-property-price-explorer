import pandas as pd

df = pd.read_csv('ed_mappings_update_with_location.csv')
df['location'].fillna('County', inplace=True)

cork = pd.read_csv('cork_eds_city.csv', index_col=2)
waterford = pd.read_csv('waterford_eds_city.csv', index_col=2)
galway = pd.read_csv('galway_eds_city.csv', index_col=2)
limerick = pd.read_csv('limerick_eds_city.csv', index_col=2)

for index, row in df.iterrows():
    if row['ed'] in cork.index:
        df.ix[index, 'location'] = 'Urban'
    elif row['ed'] in waterford.index:
        df.ix[index, 'location'] = 'Urban'
    elif row['ed'] in galway.index:
        df.ix[index, 'location'] = 'Urban'
    elif row['ed'] in limerick.index:
        df.ix[index, 'location'] = 'Urban'
    else:
        continue

df.to_csv("eds_location_split.csv")