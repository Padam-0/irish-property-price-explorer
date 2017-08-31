"""
Migrates sales data from final geocoded and cleaned data into a Postgres or
sqlite3 database as required. Updates cached national average data where
required.

"""

import pandas as pd
from sqlalchemy import create_engine
import sqlite3
import datetime
import numpy as np
import calendar


def clean_database():
    # Create engine for SQLite3
    # engine = create_engine('sqlite:///../prac/db.sqlite3', echo=False)

    # Create engine for postgres
    engine = create_engine('postgresql://padams@localhost:5432/prac_db')

    with engine.connect() as con:
        con.execute("DELETE FROM prac_sale")


def query_database():
    # Create engine for SQLite3
    # engine = create_engine('sqlite:///../prac/db.sqlite3', echo=False)

    # Create engine for postgres
    engine = create_engine('postgresql://padams@localhost:5432/prac_db')

    with engine.connect() as con:
        sales = con.execute("SELECT COUNT(*) FROM prac_sale;").fetchall()

    print(sales)


def migrate_dataframe(df, method):
    # Create engine for SQLite3
    # engine = create_engine('sqlite:///../prac/db.sqlite3', echo=False)

    # Create engine for postgres
    engine = create_engine('postgresql://padams@localhost:5432/prac_db')

    df['sale_date'] = pd.to_datetime(df['sale_date'], dayfirst=True)

    # Write to database
    df.to_sql('prac_sale', engine, if_exists=method, index_label='id')


def compress_list(data, limit):
    # Based on a list of data, bin into bins of width limit between values of
    # 0 and 500000
    a = {}
    k = 0
    for v in range(limit, 5000000, limit):
        count = 0
        for i in data:
            if i > k and i <= v:
                count += 1

        if count != 0:
            a[v - limit/2] = count

        k = v

    # If a bin has less than 5% of the entries of the largest bin, remove it.
    b = {}
    for k, v in a.items():
        if v > max(a.values()) * 0.05:
            b[k] = v

    return b


def retrieve_stats(df):
    # Returns specific statistics calculated from a dataframe

    # Number of entries in the queryset
    count = len(df.index)

    # Median price of the queryset
    med = df['price'].median()

    sale_list = []
    size_list = []

    scatter_data = {'date': [], 'price': []}
    hist_data = []

    for sale in range(count):
        raw_time = calendar.timegm(df.iloc[sale]['sale_date'].timetuple())
        sale_list.append(raw_time)
        scatter_data['date'].append(df.iloc[sale]['sale_date'])
        scatter_data['price'].append(float(df.iloc[sale]['price']))
        hist_data.append(float(df.iloc[sale]['price']))
        if df.iloc[sale]['PSD'] == 'greater than or equal to 38 sq metres ' \
                                   'and less than 125 sq metres':
            size_list.append(81.5)
        elif df.iloc[sale]['PSD'] == 'greater than 125 sq metres':
            size_list.append(125)
        elif df.iloc[sale]['PSD'] == 'less than 38 sq metres':
            size_list.append(38)

    # Average sale date and size of properties in the queryset
    avg_sale = round(np.mean(sale_list) * 1000, 0)
    avg_size = round(np.mean(size_list), 1)

    # Create data frame from scatter data
    scdf = pd.DataFrame(scatter_data, columns=['price'],
                        index=scatter_data['date'])
    scdf.index.names = ['date']

    scdf = scdf.set_index(pd.DatetimeIndex(scdf.index))

    # Group data frame sales to a weekly average
    scdf = scdf.resample('W').mean().dropna(axis=0, how='any')

    # Generate scatterplot data with correct timestamps
    scatter_data = list(map(lambda x, y: [calendar.timegm(
        x.to_pydatetime().timetuple()) * 1000,
        round(float(y), 2)], scdf.index.tolist(), scdf.values))

    compressed_hist_data = compress_list(hist_data, 20000)

    return {'ave_price': round(np.mean(hist_data)),
            'med_price': float(med), 'avg_date': avg_sale,
            'avg_size': avg_size,  'hist_data': compressed_hist_data,
            'scatter_data': scatter_data}


def get_age_stats(engine, ref_id):
    # Retrieve current age statistics from CSO data held in
    # prac_sexagemarriage database

    with engine.connect() as con:
        df = pd.read_sql("SELECT * FROM prac_sexagemarriage WHERE uid = '"
                         + ref_id + "' AND year=2016;", con)

    age_04 = df.age_04[0]
    age_59 = df.age_59[0]
    age_1014 = df.age_1014[0]
    age_1519 = df.age_1519[0]
    age_2024 = df.age_2024[0]
    age_2529 = df.age_2529[0]
    age_3034 = df.age_3034[0]
    age_3539 = df.age_3539[0]
    age_4044 = df.age_4044[0]
    age_4549 = df.age_4549[0]
    age_5054 = df.age_5054[0]
    age_5559 = df.age_5559[0]
    age_6064 = df.age_6064[0]
    age_6569 = df.age_6569[0]
    age_7074 = df.age_7074[0]
    age_7579 = df.age_7579[0]
    age_8084 = df.age_8084[0]
    age_85p = df.age_85p[0]

    # Compute weighted average of distribution
    w_age = sum([age_04 * 2.5, age_59 * 7.5, age_1014 * 12.5,
                 age_1519 * 17.5, age_2024 * 22.5, age_2529 * 27.5,
                 age_3034 * 32.5, age_3539 * 37.5, age_4044 * 42.5,
                 age_4549 * 47.5, age_5054 * 52.5, age_5559 * 57.5,
                 age_6064 * 62.5, age_6569 * 67.5, age_7074 * 72.5,
                 age_7579 * 77.5, age_8084 * 82.5, age_85p * 90])

    # Calculate total population
    pop = sum([age_04, age_59, age_1014, age_1519, age_2024, age_2529,
               age_3034, age_3539, age_4044, age_4549, age_5054, age_5559,
               age_6064, age_6569, age_7074, age_7579, age_8084, age_85p])

    return w_age, pop


def retrieve_cso(data_list, ref_id):
    # Add up to date CSO data from database to data_list dictionary

    # Create engine for SQLite3
    # engine = create_engine('sqlite:///../prac/db.sqlite3', echo=False)

    # Create engine for postgres
    engine = create_engine('postgresql://padams@localhost:5432/prac_db')

    w_age, pop = get_age_stats(engine, ref_id)

    data_list['dem_age'] = round(w_age / pop, 2)

    data_list['population'] = pop

    with engine.connect() as con:
        oc = pd.read_sql("SELECT occupied FROM prac_housing WHERE uid = '" +
                         ref_id + "' AND year=2016;", con)['occupied'][0]
        unoc = pd.read_sql("SELECT unoccupied FROM prac_housing WHERE uid = '"
                           + ref_id +
                           "' AND year=2016;", con)['unoccupied'][0]

    data_list['perc_oc'] = round((oc / (oc + unoc)) * 100, 2)

    return data_list


def refresh_cached_data():
    # Refresh cached national average sales data Dublin County, Leinster,
    # Munster and the Republic of Ireland, with and without unmapped data.

    # Create engine for SQLite3
    # engine = create_engine('sqlite:///../prac/db.sqlite3', echo=False)

    # Create engine for postgres
    engine = create_engine('postgresql://padams@localhost:5432/prac_db')

    with engine.connect() as con:
        df = pd.read_sql("SELECT * FROM prac_sale;", con)

    df = df.ix[:, ['uid', 'sale_date', 'address', 'postcode',
                   'county', 'price', 'nfma', 'vat_ex', 'DoP',
                   'PSD', 'region', 'latitude', 'longitude',
                   'ed', 'quality']]

    df['sale_date'] = pd.to_datetime(df['sale_date'])

    price_low = 0
    price_high = 26500000
    date_low = 1262304000000
    date_high = 1491001200000

    dh = datetime.datetime.fromtimestamp(date_high / 1000)
    dl = datetime.datetime.fromtimestamp(date_low / 1000)

    df = df[df.sale_date <= dh]
    df = df[df.sale_date >= dl]
    df = df[df.price >= price_low]
    df = df[df.price <= price_high]
    df = df[df.nfma == 'No']

    #########################################################################
    # Republic of Ireland with unmapped data

    data_list = retrieve_stats(df)
    data_list['min_price'] = price_low
    data_list['max_price'] = price_high
    data_list['min_date'] = date_low
    data_list['max_date'] = date_high

    data_list = retrieve_cso(data_list, 'I00')

    with open('../prac/homepage/static/homepage/data/country_data.txt',
              'w') as f:
        f.write(str(data_list))

    #########################################################################
    # Republic of Ireland without unmapped data

    df_irl_nbd = df[df.quality == 'good']

    data_list = retrieve_stats(df_irl_nbd)
    data_list['min_price'] = price_low
    data_list['max_price'] = price_high
    data_list['min_date'] = date_low
    data_list['max_date'] = date_high

    data_list = retrieve_cso(data_list, 'I00')

    with open('../prac/homepage/static/homepage/data/country_data_nobad.txt',
              'w') as f:
        f.write(str(data_list))

    #########################################################################
    # Leinster with unmapped data

    df_lein = df[df.region == 'Leinster']

    data_list = retrieve_stats(df_lein)
    data_list['min_price'] = price_low
    data_list['max_price'] = price_high
    data_list['min_date'] = date_low
    data_list['max_date'] = date_high

    data_list = retrieve_cso(data_list, 'P1')

    with open('../prac/homepage/static/homepage/data/leinster_data.txt',
              'w') as f:
        f.write(str(data_list))

    #########################################################################
    # Leinster without unmapped data

    df_lein_nbd = df_lein[df_lein.quality == 'good']

    data_list = retrieve_stats(df_lein_nbd)
    data_list['min_price'] = price_low
    data_list['max_price'] = price_high
    data_list['min_date'] = date_low
    data_list['max_date'] = date_high

    data_list = retrieve_cso(data_list, 'P1')

    with open('../prac/homepage/static/homepage/data/leinster_data_nobad.txt',
              'w') as f:
        f.write(str(data_list))

    #########################################################################
    # Munster with unmapped data

    df_mun = df[df.region == 'Munster']

    data_list = retrieve_stats(df_mun)
    data_list['min_price'] = price_low
    data_list['max_price'] = price_high
    data_list['min_date'] = date_low
    data_list['max_date'] = date_high

    data_list = retrieve_cso(data_list, 'P2')

    with open('../prac/homepage/static/homepage/data/munster_data.txt',
              'w') as f:
        f.write(str(data_list))

    #########################################################################
    # Munster without unmapped data

    df_mun_nbd = df_mun[df_mun.quality == 'good']

    data_list = retrieve_stats(df_mun_nbd)
    data_list['min_price'] = price_low
    data_list['max_price'] = price_high
    data_list['min_date'] = date_low
    data_list['max_date'] = date_high

    data_list = retrieve_cso(data_list, 'P2')

    with open('../prac/homepage/static/homepage/data/munster_data_nobad.txt',
              'w') as f:
        f.write(str(data_list))

    #########################################################################
    # Dublin with unmapped data

    df_dub = df[df.county == 'Dublin']

    data_list = retrieve_stats(df_dub)
    data_list['min_price'] = price_low
    data_list['max_price'] = price_high
    data_list['min_date'] = date_low
    data_list['max_date'] = date_high

    data_list = retrieve_cso(data_list, 'C02')

    with open('../prac/homepage/static/homepage/data/dublin_data.txt',
              'w') as f:
        f.write(str(data_list))

    #########################################################################
    # Dublin without unmapped data

    df_dub_nbd = df_dub[df_dub.quality == 'good']

    data_list = retrieve_stats(df_dub_nbd)
    data_list['min_price'] = price_low
    data_list['max_price'] = price_high
    data_list['min_date'] = date_low
    data_list['max_date'] = date_high

    data_list = retrieve_cso(data_list, 'C02')
    with open('../prac/homepage/static/homepage/data/dublin_data_nobad.txt',
              'w') as f:
        f.write(str(data_list))


def refresh_cached_natave():
    # Updates cached national average data for sales and volume charts on
    # reporting page

    # Create engine for SQLite3
    # engine = create_engine('sqlite:///../prac/db.sqlite3', echo=False)

    # Create engine for postgres
    engine = create_engine('postgresql://padams@localhost:5432/prac_db')

    with engine.connect() as con:
        df = pd.read_sql("SELECT * FROM prac_sale;", con)

    df = df.ix[:, ['uid', 'sale_date', 'address', 'postcode',
                   'county', 'price', 'nfma', 'vat_ex', 'DoP',
                   'PSD', 'region', 'latitude', 'longitude',
                   'ed', 'quality']]

    df['sale_date'] = pd.to_datetime(df['sale_date'])

    price_low = 0
    price_high = 26500000
    date_low = 1262304000000
    date_high = 1491001200000

    dh = datetime.datetime.fromtimestamp(date_high / 1000)
    dl = datetime.datetime.fromtimestamp(date_low / 1000)

    df = df[df.sale_date <= dh]
    df = df[df.sale_date >= dl]
    df = df[df.price >= price_low]
    df = df[df.price <= price_high]
    df = df[df.nfma == 'No']

    na_sales, na_volume, na_hist_data = get_na_data(df)
    with open('../prac/reporter/static/reporter/js/sales_natave.js',
              'w') as f:
        f.write('var na_sales_cached = ')
        f.write(str(na_sales))
        f.write(';\n')
        f.write('var na_volume_cached = ')
        f.write(str(na_volume))
        f.write(';\n')
        f.write('var na_hist_cached = ')
        f.write(str(na_hist_data))
        f.write(';')

    df_bd = df[df.quality == 'good']

    na_sales, na_volume, na_hist_data = get_na_data(df_bd)
    with open('../prac/reporter/static/reporter/js/sales_natave_nbd.js',
              'w') as f:
        f.write('var na_sales_nbd_cached = ')
        f.write(str(na_sales))
        f.write(';\n')
        f.write('var na_volume_nbd_cached = ')
        f.write(str(na_volume))
        f.write(';\n')
        f.write('var na_hist_nbd_cached = ')
        f.write(str(na_hist_data))
        f.write(';')


def get_na_data(df):
    # Calculates national average histogram and scatterplot data of sales
    sale_list = []
    na_hist = []

    scatter_data = {'date': [], 'price': []}

    for sale in range(len(df.index)):
        raw_time = calendar.timegm(df.iloc[sale]['sale_date'].timetuple())
        sale_list.append(raw_time)
        scatter_data['date'].append(df.iloc[sale]['sale_date'])
        scatter_data['price'].append(float(df.iloc[sale]['price']))
        na_hist.append(df.iloc[sale]['price'])

    df = pd.DataFrame(scatter_data, columns=['price'],
                      index=scatter_data['date'])
    df.index.names = ['date']
    df = df.set_index(pd.DatetimeIndex(df.index))

    nasdf = df.resample('M').mean().dropna(axis=0, how='any')
    nasdf = nasdf[nasdf['price'] != 0]
    na_sales = list(map(lambda x, y: [calendar.timegm(
        x.to_pydatetime().timetuple()) * 1000, round(float(y), 2)],
                        nasdf.index.tolist(), nasdf.values))
    navdf = df.resample('M').count().dropna(axis=0, how='any')
    navdf = navdf[navdf['price'] != 0]
    na_volume = list(map(lambda x, y: [calendar.timegm(
        x.to_pydatetime().timetuple()) * 1000, round(float(y), 2)],
                         navdf.index.tolist(), navdf.values))

    na_hist_data = compress_list(na_hist, 1000)

    return na_sales[:-1], na_volume[:-1], na_hist_data


def main():
    gdf = pd.read_csv('./geocoded_data_with_ed.csv')

    gdf['ed'] = gdf['ed'].fillna('None')

    gdf['quality'] = 'good'

    gdf.drop_duplicates(subset=['sale_date', 'address', 'postcode', 'county',
                                'price', 'nfma', 'vat_ex', 'DoP', 'PSD',
                                'region', 'latitude', 'longitude', 'ed',
                                'quality'])

    bdf = pd.read_csv('./nongeocoded_data.csv')

    # 123642, 61783 are probably genuine outliers, add them back in
    # for geobased analysis

    # Remove high price outliers
    good_outliers = [113959, 101265, 233165, 188182, 81789, 74788, 176984,
                     203508, 86798, 244292, 196404, 58447, 81824,
                     90604, 122975, 122974, 122973, 94212, 216638, 61783,
                     138747, 173153, 73751, 109950, 221603, 90602, 124032,
                     38699, 81675, 194674, 136591, 203555, 191689, 98613,
                     67289, 204718, 81786, 232445, 9338, 9339, 9340, 9341,
                     9343, 9345, 158271, 127525, 204372, 134351, 132601,
                     117168, 201182, 204418, 113943, 113944, 113946, 113947,
                     165346, 63758, 112011, 176788, 175578]
    bad_outliers = [232926, 158560, 159693, 123642, 115144, 197684, 136015,
                    183516, 90603, 177643, 117372, 134260, 138716, 74898, 2431,
                    113945, 113948, 113949, 127525, 204372]

    for outlier in good_outliers:
        gdf = gdf[gdf.uid != outlier]

    for outlier in bad_outliers:
        bdf = bdf[bdf.uid != outlier]

    bdf['latitude'] = 0
    bdf['longitude'] = 0
    bdf['ed'] = 'None'
    bdf['quality'] = 'bad'

    # Add geocoded data to database
    migrate_dataframe(gdf, 'replace')
    # Add nongeocoded data to database
    migrate_dataframe(bdf, 'append')
    # Test database length
    query_database()

    refresh_cached_data()

    refresh_cached_natave()


if __name__ == "__main__":
    main()
