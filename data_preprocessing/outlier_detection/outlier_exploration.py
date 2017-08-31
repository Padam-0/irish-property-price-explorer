import pandas as pd

df = pd.read_csv('outliers_test.csv', encoding='latin1', index_col=0)
print(df.columns)
df = df.drop(['desc', 'bed', 'bath', 'latitude', 'longitude', 'condition', 'apt', 'house_name', 'suffix'], axis=1)
outliers = df[df['outlier_2std']=='Yes']
print(outliers.head())
# print(outliers[['address','county']].groupby('county').count())
