import pandas as pd

df = pd.read_csv('model_data_ed.csv', index_col=0)

print(df.head())
cork = df[df['county'] == 'Cork']
galway = df[df['county'] == 'Galway']
waterford = df[df['county'] == 'Waterford']
limerick = df[df['county'] == 'Limerick']

cork = cork.loc[:, ['county', 'ed']].drop_duplicates()
galway = galway.loc[:, ['county', 'ed']].drop_duplicates()
waterford = waterford.loc[:, ['county', 'ed']].drop_duplicates()
limerick = limerick.loc[:, ['county', 'ed']].drop_duplicates()

cork.to_csv('cork_eds')
galway.to_csv('galway_eds')
waterford.to_csv('waterford_eds')
limerick.to_csv('limerick_eds')
