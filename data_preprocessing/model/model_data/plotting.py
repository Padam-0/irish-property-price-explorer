import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('model_data_ed.csv', encoding='latin1', index_col=0)

cork = df[df['county']=='Cork']
waterford = df[df['county']=='Waterford']

# group_munster = munster[['time','price']].groupby(munster['time']).mean()

# cork_agg = cork[['ed', 'price']].groupby(cork['ed']).agg(['mean', 'count']).reset_index()
# cork_agg = cork_agg['price'].sort_values('mean', ascending=False)
waterford_agg = waterford[['ed', 'price']].groupby(waterford['ed']).mean().reset_index()
waterford_agg = waterford_agg.sort_values('price', ascending=False)

print(waterford_agg)
plt.hist(waterford_agg.price)
plt.show()
