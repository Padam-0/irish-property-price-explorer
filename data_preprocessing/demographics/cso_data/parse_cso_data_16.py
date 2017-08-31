import pandas as pd
from sqlalchemy import create_engine

# PR is provinces (4)
# ED is electoral districts (3409)
# CTY is counties (34)
# SA is small areas (18488)

def clean_database(tablename):
    # Create engine

    # engine = create_engine('sqlite:///../../prac/db.sqlite3')
    engine = create_engine('postgresql://padams@localhost:5432/prac_db')

    query = "DELETE FROM " + tablename + ";"

    with engine.connect() as con:
        con.execute(query)


def query_database(tablename):
    query = "SELECT COUNT(*) FROM " + tablename + ";"

    # Create engine
    # engine = create_engine('sqlite:///../../prac/db.sqlite3')
    engine = create_engine('postgresql://padams@localhost:5432/prac_db')

    with engine.connect() as con:
        data = con.execute(query).fetchall()

    print(data)



def migrate_dataframe(df, table):
    # Create engine
    # engine = create_engine('sqlite:///../../prac/db.sqlite3', echo=False)
    engine = create_engine('postgresql://padams@localhost:5432/prac_db', echo=False)

    df.to_sql(table, engine, if_exists='append', index=False)
    # Use if_exists='append' when adding new data


def main():
    df_pr = pd.read_csv('data/2016/SAPS2016_PROV.csv', thousands=',')

    df_pr['zoom'] = 'region'
    df_irl = df_pr.groupby('zoom').sum()

    df_irl['uid'] = 'I00'
    df_irl['zoom'] = 'country'
    df_irl['desc'] = 'Ireland'
    df_irl['year'] = 2016

    a = ['uid', 'zoom', 'desc', 'year']
    for i in list(df_irl.columns[:-4]):
        a.append(i)

    df_irl = df_irl.ix[:, a]
    df_irl.index.names = ['']
    df_irl.index = [0]

    df_pr['year'] = 2016
    df_pr['uid'] = df_pr['GEOGID'].apply(lambda x: x[:1] + x[-1:])
    df_pr.loc[3, 'GEOGDESC'] = 'Ulster'
    df_pr['desc'] = df_pr['GEOGDESC']

    a = ['uid', 'zoom', 'desc', 'year']
    for i in list(df_pr.columns[3:-4]):
        a.append(i)

    df_pr = df_pr.ix[:, a]

    df_cty = pd.read_csv('data/2016/SAPS2016_CTY31.csv', thousands=',', encoding='latin1')

    df_cty['zoom'] = 'county'

    df_dub = df_cty.ix[[5, 7, 8, 24],].groupby('zoom').sum()
    df_dub['uid'] = 'C02'
    df_dub['zoom'] = 'county'
    df_dub['desc'] = 'Dublin'

    df_cork = df_cty.ix[[0,2], ].groupby('zoom').sum()
    df_cork['uid'] = 'C17'
    df_cork['zoom'] = 'county'
    df_cork['desc'] = 'Cork'

    df_gal = df_cty.ix[9:11, ].groupby('zoom').sum()
    df_gal['uid'] = 'C26'
    df_gal['zoom'] = 'county'
    df_gal['desc'] = 'Galway'

    a = ['uid', 'zoom', 'desc']

    for i in list(df_dub.columns[:-4]):
        a.append(i)

    df_dub = df_dub.ix[:, a]
    df_dub.index.names = ['']
    df_cork = df_cork.ix[:, a]
    df_cork.index.names = ['']
    df_gal = df_gal.ix[:, a]
    df_gal.index.names = ['']

    df_cty['desc'] = df_cty['GEOGDESC']

    df_cty['uid'] = '00'

    df_cty = pd.concat([df_cty, df_dub, df_cork, df_gal], ignore_index=True)

    df_cty = df_cty.drop([0, 2, 5, 7, 8, 9, 10, 24], axis='rows').sort_values(by='desc')


    df_cty.loc[4, 'uid'] = 'C01'
    df_cty.loc[3, 'uid'] = 'C32'
    df_cty.loc[1, 'uid'] = 'C16'
    df_cty.loc[6, 'uid'] = 'C33'
    df_cty.loc[13, 'uid'] = 'C19'
    df_cty.loc[11, 'uid'] = 'C06'

    df_cty.loc[12, 'uid'] = 'C07'
    df_cty.loc[18, 'uid'] = 'C08'
    df_cty.loc[17, 'uid'] = 'C28'
    df_cty.loc[16, 'desc'] = 'Limerick'
    df_cty.loc[16, 'uid'] = 'C20'
    df_cty.loc[14, 'uid'] = 'C09'
    df_cty.loc[15, 'uid'] = 'C10'
    df_cty.loc[21, 'uid'] = 'C29'

    df_cty.loc[19, 'uid'] = 'C11'
    df_cty.loc[20, 'uid'] = 'C34'
    df_cty.loc[22, 'uid'] = 'C12'
    df_cty.loc[23, 'uid'] = 'C30'
    df_cty.loc[25, 'uid'] = 'C31'
    df_cty.loc[26, 'uid'] = 'C22'
    df_cty.loc[27, 'desc'] = 'Waterford'
    df_cty.loc[27, 'uid'] = 'C24'
    df_cty.loc[28, 'uid'] = 'C13'
    df_cty.loc[30, 'uid'] = 'C14'
    df_cty.loc[29, 'uid'] = 'C15'

    df_cty['year'] = 2016

    a = ['uid', 'zoom', 'desc', 'year']
    for i in list(df_cty.columns[4:-4]):
        a.append(i)

    df_cty = df_cty.ix[:, a]

    df_ed = pd.read_csv('data/2016/SAPS2016_ED3409.csv', thousands=',', encoding='latin1')

    df_ed['uid'] = df_ed['GEOGID'].apply(lambda x: 'E' + x[7:])
    df_ed['zoom'] = 'edist'
    df_ed['year'] = 2016
    df_ed['desc'] = df_ed['GEOGDESC']

    a = ['uid', 'zoom', 'desc', 'year']
    for i in list(df_ed.columns[3:-4]):
        a.append(i)

    df_ed = df_ed.ix[:, a]

    df_list = [df_pr, df_cty, df_ed, df_irl]

    for i in range(len(df_list)):
        df = df_list[i]
        
        table_1_1 = ['uid', 'zoom', 'year']
        table_1_2 = ['uid', 'zoom', 'year']

        table_2_1 = ['uid', 'zoom', 'year']

        table_4_2 = ['uid', 'zoom', 'year']
        table_4_5 = ['uid', 'zoom', 'year']

        table_5_1 = ['uid', 'zoom', 'year']
        table_5_2 = ['uid', 'zoom', 'year']

        table_6_1 = ['uid', 'zoom', 'year']
        table_6_2 = ['uid', 'zoom', 'year']
        table_6_3 = ['uid', 'zoom', 'year']
        table_6_4 = ['uid', 'zoom', 'year']
        table_6_8 = ['uid', 'zoom', 'year']

        table_8_1 = ['uid', 'zoom', 'year']
        table_9_1 = ['uid', 'zoom', 'year']

        table_10_4 = ['uid', 'zoom', 'year']
        table_11_1 = ['uid', 'zoom', 'year']
        table_11_3 = ['uid', 'zoom', 'year']

        table_13_1 = ['uid', 'zoom', 'year']
        table_14_1 = ['uid', 'zoom', 'year']

        for name in list(df.columns):
            if name[:4] == 'T1_1':
                table_1_1.append(name)
            elif name[:4] == 'T1_2':
                table_1_2.append(name)
            elif name[:4] == 'T2_1':
                table_2_1.append(name)
            elif name[:4] == 'T4_2':
                table_4_2.append(name)
            elif name[:4] == 'T4_5':
                table_4_5.append(name)
            elif name[:4] == 'T5_1':
                table_5_1.append(name)
            elif name[:4] == 'T5_2':
                table_5_2.append(name)
            elif name[:4] == 'T6_1':
                table_6_1.append(name)
            elif name[:4] == 'T6_2':
                table_6_2.append(name)
            elif name[:4] == 'T6_3':
                table_6_3.append(name)
            elif name[:4] == 'T6_4':
                table_6_4.append(name)
            elif name[:4] == 'T6_8':
                table_6_8.append(name)
            elif name[:4] == 'T8_1':
                table_8_1.append(name)
            elif name[:4] == 'T9_1':
                table_9_1.append(name)
            elif name[:5] == 'T10_4':
                table_10_4.append(name)
            elif name[:5] == 'T11_1':
                table_11_1.append(name)
            elif name[:5] == 'T11_3':
                table_11_3.append(name)
            elif name[:5] == 'T13_1':
                table_13_1.append(name)
            elif name[:5] == 'T14_1':
                table_14_1.append(name)

        # Population aged 0-19 by sex and year of age, persons aged 20+ by sex and age group
        t1_1 = df.drop([i for i in df.columns if i not in table_1_1],
                       axis='columns')
        # Population by sex and marital status
        t1_2 = df.drop([i for i in df.columns if i not in table_1_2],
                       axis='columns')
        # Usually resident population by place of birth and nationality
        t2_1 = df.drop([i for i in df.columns if i not in table_2_1],
                       axis='columns')
        # Family units with children by size and age of children
        t4_2 = df.drop([i for i in df.columns if i not in table_4_2],
                       axis='columns')
        # Families by family cycle
        t4_5 = df.drop([i for i in df.columns if i not in table_4_5],
                       axis='columns')
        # Private households by type
        t5_1 = df.drop([i for i in df.columns if i not in table_5_1],
                       axis='columns')
        # Private households by size
        t5_2 = df.drop([i for i in df.columns if i not in table_5_2],
                       axis='columns')
        # Private households by type of accommodation
        t6_1 = df.drop([i for i in df.columns if i not in table_6_1],
                       axis='columns')
        # Permanent private households by year built
        t6_2 = df.drop([i for i in df.columns if i not in table_6_2],
                       axis='columns')
        # Permanent private households by type of occupancy
        t6_3 = df.drop([i for i in df.columns if i not in table_6_3],
                       axis='columns')
        # Permanent private households by number of rooms
        t6_4 = df.drop([i for i in df.columns if i not in table_6_4],
                       axis='columns')
        # Occupancy status of permanent dwellings on Census night
        t6_8 = df.drop([i for i in df.columns if i not in table_6_8],
                       axis='columns')
        # Population aged 15 years and over by principal economic status and sex
        t8_1 = df.drop([i for i in df.columns if i not in table_8_1],
                       axis='columns')
        # Population by sex and social class
        t9_1 = df.drop([i for i in df.columns if i not in table_9_1],
                       axis='columns')
        # Population aged 15 years and over by sex and highest level of education completed
        t10_4 = df.drop([i for i in df.columns if i not in table_10_4],
                        axis='columns')
        # Population aged 5 years and over by means of travel to work, school or college
        t11_1 = df.drop([i for i in df.columns if i not in table_11_1],
                        axis='columns')
        # Population aged 5 years and over by journey time to work, school or college
        t11_3 = df.drop([i for i in df.columns if i not in table_11_3],
                        axis='columns')
        # Persons at work or unemployed by occupation and sex
        t13_1 = df.drop([i for i in df.columns if i not in table_13_1],
                        axis='columns')
        # Persons at work by industry and sex
        t14_1 = df.drop([i for i in df.columns if i not in table_14_1],
                        axis='columns')

        drop_cols = ['T1_1AGETM', 'T1_1AGETF', 'T1_1AGE45_49T', 'T1_1AGE50_54T', 'T1_1AGE55_59T', 'T1_1AGE60_64T',
                   'T1_1AGE65_69T', 'T1_1AGE70_74T', 'T1_1AGE75_79T', 'T1_1AGE80_84T',
                   'T1_1AGEGE_85T', 'T1_1AGETT', 'T1_1AGE20_24T', 'T1_1AGE25_29T',
                   'T1_1AGE30_34T', 'T1_1AGE35_39T', 'T1_1AGE40_44T']
        et1 = t1_1.drop([i for i in t1_1.columns if (i in drop_cols)], axis='columns')

        et1['T1_1AGE0_4M'] = et1['T1_1AGE0M'] + et1['T1_1AGE1M'] + et1[
            'T1_1AGE2M'] + et1['T1_1AGE3M'] + et1['T1_1AGE4M']
        et1['T1_1AGE5_9M'] = et1['T1_1AGE5M'] + et1['T1_1AGE6M'] + et1[
            'T1_1AGE7M'] + et1['T1_1AGE8M'] + et1['T1_1AGE9M']
        et1['T1_1AGE10_14M'] = et1['T1_1AGE10M'] + et1['T1_1AGE11M'] + et1[
            'T1_1AGE12M'] + et1['T1_1AGE13M'] + et1['T1_1AGE14M']
        et1['T1_1AGE15_19M'] = et1['T1_1AGE15M'] + et1['T1_1AGE16M'] + et1[
            'T1_1AGE17M'] + et1['T1_1AGE18M'] + et1['T1_1AGE19M']

        et1['T1_1AGE0_4F'] = et1['T1_1AGE0F'] + et1['T1_1AGE1F'] + et1[
            'T1_1AGE2F'] + et1['T1_1AGE3F'] + et1['T1_1AGE4F']
        et1['T1_1AGE5_9F'] = et1['T1_1AGE5F'] + et1['T1_1AGE6F'] + et1[
            'T1_1AGE7F'] + et1['T1_1AGE8F'] + et1['T1_1AGE9F']
        et1['T1_1AGE10_14F'] = et1['T1_1AGE10F'] + et1['T1_1AGE11F'] + et1[
            'T1_1AGE12F'] + et1['T1_1AGE13F'] + et1['T1_1AGE14F']
        et1['T1_1AGE15_19F'] = et1['T1_1AGE15F'] + et1['T1_1AGE16F'] + et1[
            'T1_1AGE17F'] + et1['T1_1AGE18F'] + et1['T1_1AGE19F']

        et1 = et1.drop([i for i in et1.columns if
            (i.count('_') == 1 and i[-1] == 'F')], axis='columns')

        et1 = et1.drop([i for i in et1.columns if
                        (i.count('_') == 1 and i[-1] == 'M')], axis='columns')

        et1 = et1.ix[:,
               ['uid', 'zoom', 'year', 'T1_1AGE0_4M', 'T1_1AGE5_9M', 'T1_1AGE10_14M',
               'T1_1AGE15_19M', 'T1_1AGE20_24M', 'T1_1AGE25_29M', 'T1_1AGE30_34M',
               'T1_1AGE35_39M', 'T1_1AGE40_44M', 'T1_1AGE45_49M', 'T1_1AGE50_54M',
               'T1_1AGE55_59M', 'T1_1AGE60_64M', 'T1_1AGE65_69M', 'T1_1AGE70_74M',
               'T1_1AGE75_79M', 'T1_1AGE80_84M', 'T1_1AGEGE_85M', 'T1_1AGE0_4F',
               'T1_1AGE5_9F', 'T1_1AGE10_14F', 'T1_1AGE15_19F', 'T1_1AGE20_24F',
               'T1_1AGE25_29F', 'T1_1AGE30_34F', 'T1_1AGE35_39F', 'T1_1AGE40_44F',
               'T1_1AGE45_49F', 'T1_1AGE50_54F', 'T1_1AGE55_59F', 'T1_1AGE60_64F',
               'T1_1AGE65_69F', 'T1_1AGE70_74F', 'T1_1AGE75_79F', 'T1_1AGE80_84F',
               'T1_1AGEGE_85F', 'T1_1AGE0T', 'T1_1AGE1T', 'T1_1AGE2T', 'T1_1AGE3T',
               'T1_1AGE4T', 'T1_1AGE5T', 'T1_1AGE6T', 'T1_1AGE7T', 'T1_1AGE8T',
               'T1_1AGE9T', 'T1_1AGE10T', 'T1_1AGE11T', 'T1_1AGE12T', 'T1_1AGE13T',
               'T1_1AGE14T', 'T1_1AGE15T', 'T1_1AGE16T', 'T1_1AGE17T', 'T1_1AGE18T',
               'T1_1AGE19T']]

        et1.columns = ['uid', 'zoom', 'year', 'age_04_m', 'age_59_m', 'age_1014_m',
                       'age_1519_m', 'age_2024_m', 'age_2529_m', 'age_3034_m',
                       'age_3539_m', 'age_4044_m', 'age_4549_m', 'age_5054_m',
                       'age_5559_m', 'age_6064_m', 'age_6569_m', 'age_7074_m',
                       'age_7579_m', 'age_8084_m', 'age_85p_m', 'age_04_f',
                       'age_59_f', 'age_1014_f', 'age_1519_f', 'age_2024_f',
                       'age_2529_f', 'age_3034_f', 'age_3539_f', 'age_4044_f',
                       'age_4549_f', 'age_5054_f', 'age_5559_f', 'age_6064_f',
                       'age_6569_f', 'age_7074_f', 'age_7579_f', 'age_8084_f',
                       'age_85p_f', 'age_0', 'age_1', 'age_2', 'age_3', 'age_4',
                       'age_5', 'age_6', 'age_7', 'age_8', 'age_9', 'age_10',
                       'age_11', 'age_12', 'age_13', 'age_14', 'age_15',
                       'age_16', 'age_17', 'age_18', 'age_19']


        t1_1 = t1_1.drop(
            [i for i in t1_1.columns if (i[-1] != 'T' and i not in ['uid', 'zoom', 'year'])],
            axis='columns')
        t1_1['T1_1AGE0_4T'] = t1_1['T1_1AGE0T'] + t1_1['T1_1AGE1T'] + t1_1[
            'T1_1AGE2T'] + t1_1['T1_1AGE3T'] + t1_1['T1_1AGE4T']
        t1_1['T1_1AGE5_9T'] = t1_1['T1_1AGE5T'] + t1_1['T1_1AGE6T'] + t1_1[
            'T1_1AGE7T'] + t1_1['T1_1AGE8T'] + t1_1['T1_1AGE9T']
        t1_1['T1_1AGE10_14T'] = t1_1['T1_1AGE10T'] + t1_1['T1_1AGE11T'] + t1_1[
            'T1_1AGE12T'] + t1_1['T1_1AGE13T'] + t1_1['T1_1AGE14T']
        t1_1['T1_1AGE15_19T'] = t1_1['T1_1AGE15T'] + t1_1['T1_1AGE16T'] + t1_1[
            'T1_1AGE17T'] + t1_1['T1_1AGE18T'] + t1_1['T1_1AGE19T']
        t1_1 = t1_1.drop([i for i in t1_1.columns if
                          (i.count('_') == 1 and i not in ['uid', 'zoom', 'year'] and i[-2] != 'T')],
                         axis='columns')

        t1_1 = t1_1.ix[:, ['uid', 'zoom', 'year', 'T1_1AGE0_4T', 'T1_1AGE5_9T',
                           'T1_1AGE10_14T', 'T1_1AGE15_19T', 'T1_1AGE20_24T',
                           'T1_1AGE25_29T', 'T1_1AGE30_34T', 'T1_1AGE35_39T',
                           'T1_1AGE40_44T', 'T1_1AGE45_49T', 'T1_1AGE50_54T',
                           'T1_1AGE55_59T', 'T1_1AGE60_64T', 'T1_1AGE65_69T',
                           'T1_1AGE70_74T', 'T1_1AGE75_79T', 'T1_1AGE80_84T',
                           'T1_1AGEGE_85T', 'T1_1AGETT']]

        t1_1.columns = ['uid', 'zoom', 'year', 'age_04', 'age_59', 'age_1014',
                        'age_1519', 'age_2024', 'age_2529', 'age_3034',
                        'age_3539', 'age_4044', 'age_4549', 'age_5054',
                        'age_5559', 'age_6064', 'age_6569', 'age_7074',
                        'age_7579', 'age_8084', 'age_85p', 'pop']

        t1_2 = t1_2.drop(
            [i for i in t1_2.columns if (i[-1] != 'T' and i not in ['uid', 'zoom', 'year'])],
            axis='columns')

        t1_2 = t1_2.ix[:, ['uid', 'zoom', 'year', 'T1_2SGLT', 'T1_2MART', 'T1_2SEPT', 'T1_2DIVT', 'T1_2WIDT', 'T1_2T']]

        t1_2.columns = ['uid', 'zoom', 'year', 'single', 'married', 'separated', 'divorced', 'widowed', 'mar_total']

        t1 = t1_1.join(t1_2, rsuffix='test')
        t1 = t1.drop([i for i in t1.columns if i[-4:] == 'test'],
                     axis='columns')

        t2_1 = t2_1.ix[:, ['uid', 'zoom', 'year', 'T2_1IEBP', 'T2_1UKBP', 'T2_1PLBP', 'T2_1LTBP',
                'T2_1EUBP', 'T2_1RWBP', 'T2_1NSBP', 'T2_1TBP', 'T2_1IEN', 'T2_1UKN',
                'T2_1PLN', 'T2_1LTN', 'T2_1EUN', 'T2_1RWN', 'T2_1NSN', 'T2_1TN']]

        t2_1.columns = ['uid', 'zoom', 'year', 'pob_ire', 'pob_uk', 'pob_pol',
                        'pob_lit', 'pob_oeu', 'pob_row', 'pob_ns', 'pob_tot',
                        'nat_ire', 'nat_uk', 'nat_pol', 'nat_lit', 'nat_oeu',
                        'nat_row', 'nat_ns', 'nat_tot']

        t4_2 = t4_2.drop(
            [i for i in t4_2.columns if (i[-1] != 'T' and i not in ['uid', 'zoom', 'year'])],
            axis='columns')
        t4_2 = t4_2.ix[:, ['uid', 'zoom', 'year', 'T4_2_NCT', 'T4_2_1CT', 'T4_2_2CT',
                'T4_2_3CT', 'T4_2_4CT', 'T4_2_GE5CT']]

        t4_5 = t4_5.drop(
            [i for i in t4_5.columns if (i[-1] != 'P' and i not in ['uid', 'zoom', 'year'])],
            axis='columns')
        t4_5 = t4_5.ix[:, ['uid', 'zoom', 'year', 'T4_5PFP', 'T4_5ENP', 'T4_5RP', 'T4_5PSP', 'T4_5ESP', 'T4_5PAP',
                           'T4_5ADOP', 'T4_5ADUP', 'T4_5TP']]

        t4 = t4_2.join(t4_5, rsuffix='test')
        t4 = t4.drop([i for i in t4.columns if i[-4:] == 'test'],
                     axis='columns')

        t4.columns = ['uid', 'zoom', 'year', 'child_0', 'child_1', 'child_2',
                      'child_3', 'child_4', 'child_ge5', 'pre_fam',
                      'empty_nest', 'retired', 'pre_s', 'early_s', 'pre_adol',
                      'adol', 'adult', 'fam_total']

        t5_1 = t5_1.drop(
            [i for i in t5_1.columns if (i[-1] != 'H' and i not in ['uid', 'zoom', 'year'])],
            axis='columns')
        t5_1 = t5_1.ix[:, ['uid', 'zoom', 'year', 'T5_1OP_H', 'T5_1MC_H', 'T5_1CC_H', 'T5_1MCC_H',
                'T5_1CCC_H', 'T5_1OPFC_H', 'T5_1OPMC_H', 'T5_1CO_H', 'T5_1CCO_H',
                'T5_1OPFCO_H', 'T5_1OPMCO_H', 'T5_1GETFU_H', 'T5_1NHR_H', 'T5_1GENP_H', 'T5_1T_H']]

        t5_2 = t5_2.drop(
            [i for i in t5_2.columns if (i[-1] != 'H' and i not in ['uid', 'zoom', 'year'])],
            axis='columns')

        t5 = t5_1.join(t5_2, rsuffix='test')
        t5 = t5.drop([i for i in t5.columns if i[-4:] == 'test'],
                     axis='columns')

        t5.columns = ['uid', 'zoom', 'year', 'one_p', 'married',
                      'cohab_couple',
                      'married_kids', 'cohab_couple_kids', 'father_kids',
                      'mother_kids', 'couple_others', 'couple_kids_others',
                      'father_kids_others', 'mother_kids_others',
                      'two_or_more_fu', 'non_fam_hh', 'two_or_more_nrp',
                      'hstat_total', 'one_phh', 'two_phh', 'three_phh',
                      'four_phh',
                      'five_phh', 'six_phh', 'seven_phh', 'ge_eight_phh',
                      'phh_total_hh']

        t6_1 = t6_1.drop(
            [i for i in t6_1.columns if (i[-1] != 'H' and i not in ['uid', 'zoom', 'year'])],
            axis='columns')

        t6_1 = t6_1.ix[:,
               ['uid', 'zoom', 'year', 'T6_1_HB_H', 'T6_1_FA_H', 'T6_1_BS_H',
                'T6_1_CM_H', 'T6_1_NS_H', 'T6_1_TH']]

        t6_2 = t6_2.drop(
            [i for i in t6_2.columns if (i[-1] != 'H' and i not in ['uid', 'zoom', 'year'])],
            axis='columns')

        t6_2 = t6_2.ix[:,
               ['uid', 'zoom', 'year', 'T6_2_PRE19H', 'T6_2_19_45H', 'T6_2_46_60H', 'T6_2_61_70H',
                'T6_2_71_80H', 'T6_2_81_90H', 'T6_2_91_00H', 'T6_2_01_10H', 'T6_2_11LH', 'T6_2_NSH', 'T6_2_TH']]

        t6_3 = t6_3.drop(
            [i for i in t6_3.columns if (i[-1] != 'H' and i not in ['uid', 'zoom', 'year'])],
            axis='columns')
        t6_4 = t6_4.drop(
            [i for i in t6_4.columns if (i[-1] != 'H' and i not in ['uid', 'zoom', 'year'])],
            axis='columns')
        t6_8 = t6_8.drop(
            [i for i in t6_8.columns if (i[-1] == 'T' and i not in ['uid', 'zoom', 'year'])],
            axis='columns')

        t6 = t6_1.join(t6_2, rsuffix='test').join(t6_3, rsuffix='test').join(
            t6_4, rsuffix='test').join(t6_8, rsuffix='test')
        t6 = t6.drop([i for i in t6.columns if i[-4:] == 'test'],
                     axis='columns')

        t6.columns = ['uid', 'zoom', 'year', 'house_bung', 'apart', 'bedsit',
                      'caravan', 'type_ns', 'type_total_hh', 'l1919',
                      'b19_45', 'b46_60', 'b61_70', 'b71_80', 'b81_90',
                      'b91_00', 'b01_10', 'g11', 'h_age_ns', 'h_age_total_hh',
                      'oo_wm', 'oo_wom', 'rent_pl', 'rent_la', 'rent_vol',
                      'rent_free', 'occu_ns', 'occu_total_hh', 'rooms_1',
                      'rooms_2', 'rooms_3', 'rooms_4', 'rooms_5', 'rooms_6', 'rooms_7',
                      'rooms_ge8', 'rooms_ns', 'rooms_total_hh', 'occupied',
                      'temp_unoc', 'unoc_hol', 'unoccupied']

        t8_1 = t8_1.drop(
            [i for i in t8_1.columns if (i[-1] != 'T' and i not in ['uid', 'zoom', 'year'])],
            axis='columns')

        t8_1 = t8_1.ix[:,
               ['uid', 'zoom', 'year', 'T8_1_WT', 'T8_1_LFFJT', 'T8_1_ULGUPJT',
                'T8_1_ST', 'T8_1_LAHFT', 'T8_1_RT', 'T8_1_UTWSDT', 'T8_1_OTHT',
                'T8_1_TT']]

        t8_1.columns = ['uid', 'zoom', 'year', 'work', 'lffj', 'unemployed',
                        'student', 'home_fam', 'retired', 'sick_dis',
                        'stat_other',
                        'stat_total']

        t9_1 = t9_1.drop(
            [i for i in t9_1.columns if (i[-1] != 'T' and i not in ['uid', 'zoom', 'year'])],
            axis='columns')

        t9_1 = t9_1.ix[:,
               ['uid', 'zoom', 'year', 'T9_1_PWT', 'T9_1_MTT', 'T9_1_NMT',
                'T9_1_ST',
                'T9_1_SST', 'T9_1_UST', 'T9_1_OTHGEUT', 'T9_1_TT']]

        t9_1.columns = ['uid', 'zoom', 'year', 'prof_worker', 'manage_tech',
                        'non_manual', 'skilled_manual', 'semi_skilled',
                        'unskilled', 'class_other', 'class_total']

        t10_4 = t10_4.drop(
            [i for i in t10_4.columns if (i[-1] != 'T' and i not in ['uid', 'zoom', 'year'])],
            axis='columns')

        t10_4 = t10_4.ix[:,
                ['uid', 'zoom', 'year', 'T10_4_NFT', 'T10_4_PT', 'T10_4_LST',
                 'T10_4_UST',
                 'T10_4_TVT', 'T10_4_ACCAT', 'T10_4_HCT', 'T10_4_ODNDT',
                 'T10_4_HDPQT',
                 'T10_4_PDT', 'T10_4_DT', 'T10_4_NST', 'T10_4_TT']]

        t10_4.columns = ['uid', 'zoom', 'year', 'nfe', 'primary',
                         'l_secondary',
                         'u_secondary', 'tech_vocat', 'apprentice',
                         'high_cert', 'bach', 'bach_hons', 'postgrad',
                         'doctorate', 'ed_ns', 'ed_total']

        t11_1 = t11_1.ix[:, ['uid', 'zoom', 'year', 'T11_1_FT', 'T11_1_BIT', 'T11_1_BUT',
                 'T11_1_TDLT',
                 'T11_1_MT', 'T11_1_CDT', 'T11_1_CPT', 'T11_1_VT',
                 'T11_1_OTHT', 'T11_1_NST',
                 'T11_1_TT']]

        t11 = t11_1.join(t11_3, rsuffix='test')
        t11 = t11.drop([i for i in t11.columns if i[-4:] == 'test'],
                       axis='columns')

        t11.columns = ['uid', 'zoom', 'year', 'foot', 'bike', 'bus', 'train',
                       'mbike', 'car_d', 'car_p', 'van', 'other', 'method_ns',
                       'method_total', 'u15m', 'b15_30m', 'b30_45m',
                       'b45_60m', 'b60_90m', 'o90m', 'time_ns', 'time_total']

        t13_1 = t13_1.drop(
            [i for i in t13_1.columns if (i[-1] != 'T' and i not in ['uid', 'zoom', 'year'])],
            axis='columns')

        t13_1 = t13_1.ix[:, ['uid', 'zoom', 'year', 'T13_1_MDSOT', 'T13_1_POT',
                             'T13_1_APTOT',
                             'T13_1_ASOT', 'T13_1_STOT', 'T13_1_CLOSOT',
                             'T13_1_SCSOT',
                             'T13_1_PPMOT', 'T13_1_EOT', 'T13_1_NST',
                             'T13_1_TT']]

        t13_1.columns = ['uid', 'zoom', 'year', 'man_dir_sos', 'prof_oc',
                         'assoc_prof_tech', 'admin_sec', 'skilled_trade',
                         'caring_leisure', 'sales_cs', 'process_plant',
                         'elementary', 'occ_ns', 'occ_total']

        t14_1['T14_1_AFFT'] = t14_1['T14_1_AFFM'] + t14_1['T14_1_AFFF']
        t14_1['T14_1_BCT'] = t14_1['T14_1_BCM'] + t14_1['T14_1_BCF']
        t14_1['T14_1_MIT'] = t14_1['T14_1_MIM'] + t14_1['T14_1_MIF']
        t14_1['T14_1_CTT'] = t14_1['T14_1_CTM'] + t14_1['T14_1_CTF']
        t14_1['T14_1_TCT'] = t14_1['T14_1_TCM'] + t14_1['T14_1_TCF']
        t14_1['T14_1_PAT'] = t14_1['T14_1_PAM'] + t14_1['T14_1_PAF']
        t14_1['T14_1_PST'] = t14_1['T14_1_PSM'] + t14_1['T14_1_PSF']
        t14_1['T14_1_OTHT'] = t14_1['T14_1_OTHM'] + t14_1['T14_1_OTHF']
        t14_1['T14_1_TT'] = t14_1['T14_1_TM'] + t14_1['T14_1_TF']
        t14_1 = t14_1.drop(
            [i for i in t14_1.columns if (i[-1] != 'T' and i not in ['uid', 'zoom', 'year'])],
            axis='columns')

        t14_1 = t14_1.ix[:, ['uid', 'zoom', 'year', 'T14_1_AFFT', 'T14_1_BCT', 'T14_1_MIT',
                               'T14_1_CTT', 'T14_1_TCT', 'T14_1_PAT', 'T14_1_PST', 'T14_1_OTHT',
                               'T14_1_TT']]

        t14_1.columns = ['uid', 'zoom', 'year', 'ag_for_fish', 'build_construct',
                         'manufac', 'comm_trade', 'trans_coms', 'pub_admin',
                         'prof_ser', 'ind_other', 'ind_total']

        if i == 2:
            tt1 = []
            tt2_1 = []
            tt4 = []
            tt5 = []
            tt6 = []
            tt8_1 = []
            tt9_1 = []
            tt10_4 = []
            tt11 = []
            tt13_1 = []
            tt14_1 = []
            tet1 = []
            for i in t1.index:
                if '/' in t1.loc[i, 'uid']:
                    it1 = t1.loc[i, :].values
                    it2_1 = t2_1.loc[i, :].values
                    it4 = t4.loc[i, :].values
                    it5 = t5.loc[i, :].values
                    it6 = t6.loc[i, :].values
                    it8_1 = t8_1.loc[i, :].values
                    it9_1 = t9_1.loc[i, :].values
                    it10_4 = t10_4.loc[i, :].values
                    it11 = t11.loc[i, :].values
                    it13_1 = t13_1.loc[i, :].values
                    it14_1 = t14_1.loc[i, :].values
                    iet1 = et1.loc[i, :].values

                    ed_uid_1, ed_uid_2 = it1[0].split('/')

                    t1.loc[i, 'uid'] = ed_uid_1
                    t2_1.loc[i, 'uid'] = ed_uid_1
                    t4.loc[i, 'uid'] = ed_uid_1
                    t5.loc[i, 'uid'] = ed_uid_1
                    t6.loc[i, 'uid'] = ed_uid_1
                    t8_1.loc[i, 'uid'] = ed_uid_1
                    t9_1.loc[i, 'uid'] = ed_uid_1
                    t10_4.loc[i, 'uid'] = ed_uid_1
                    t11.loc[i, 'uid'] = ed_uid_1
                    t13_1.loc[i, 'uid'] = ed_uid_1
                    t14_1.loc[i, 'uid'] = ed_uid_1
                    et1.loc[i, 'uid'] = ed_uid_1

                    tt1.append(['E' + ed_uid_2, 'edist'] + list(it1[2:]))
                    tt2_1.append(['E' + ed_uid_2, 'edist'] + list(it2_1[2:]))
                    tt4.append(['E' + ed_uid_2, 'edist'] + list(it4[2:]))
                    tt5.append(['E' + ed_uid_2, 'edist'] + list(it5[2:]))
                    tt6.append(['E' + ed_uid_2, 'edist'] + list(it6[2:]))
                    tt8_1.append(['E' + ed_uid_2, 'edist'] + list(it8_1[2:]))
                    tt9_1.append(['E' + ed_uid_2, 'edist'] + list(it9_1[2:]))
                    tt10_4.append(['E' + ed_uid_2, 'edist'] + list(it10_4[2:]))
                    tt11.append(['E' + ed_uid_2, 'edist'] + list(it11[2:]))
                    tt13_1.append(['E' + ed_uid_2, 'edist'] + list(it13_1[2:]))
                    tt14_1.append(['E' + ed_uid_2, 'edist'] + list(it14_1[2:]))
                    tet1.append(['E' + ed_uid_2, 'edist'] + list(iet1[2:]))

            t1_df = pd.DataFrame(tt1, columns=t1.columns)
            t2_1_df = pd.DataFrame(tt2_1, columns=t2_1.columns)
            t4_df = pd.DataFrame(tt4, columns=t4.columns)
            t5_df = pd.DataFrame(tt5, columns=t5.columns)
            t6_df = pd.DataFrame(tt6, columns=t6.columns)
            t8_1_df = pd.DataFrame(tt8_1, columns=t8_1.columns)
            t9_1_df = pd.DataFrame(tt9_1, columns=t9_1.columns)
            t10_4_df = pd.DataFrame(tt10_4, columns=t10_4.columns)
            t11_df = pd.DataFrame(tt11, columns=t11.columns)
            t13_1_df = pd.DataFrame(tt13_1, columns=t13_1.columns)
            t14_1_df = pd.DataFrame(tt14_1, columns=t14_1.columns)
            et1_df = pd.DataFrame(tet1, columns=et1.columns)

            t1 = t1.append(t1_df, ignore_index=True)
            t2_1 = t2_1.append(t2_1_df, ignore_index=True)
            t4 = t4.append(t4_df, ignore_index=True)
            t5 = t5.append(t5_df, ignore_index=True)
            t6 = t6.append(t6_df, ignore_index=True)
            t8_1 = t8_1.append(t8_1_df, ignore_index=True)
            t9_1 = t9_1.append(t9_1_df, ignore_index=True)
            t10_4 = t10_4.append(t10_4_df, ignore_index=True)
            t11 = t11.append(t11_df, ignore_index=True)
            t13_1 = t13_1.append(t13_1_df, ignore_index=True)
            t14_1 = t14_1.append(t14_1_df, ignore_index=True)
            et1 = et1.append(et1_df, ignore_index=True)

            et1.to_csv('ed_subset/mf_age_ed.csv', index=False)
            t4.to_csv('ed_subset/fam_stat_ed.csv')
            t6.to_csv('ed_subset/house_stat_ed.csv')
            t8_1.to_csv('ed_subset/prince_stat_ed.csv')
            t9_1.to_csv('ed_subset/job_stat_ed.csv')
            t14_1.to_csv('ed_subset/ind_stat_ed.csv')
        elif i == 3:
            et1.to_csv('ed_subset/mf_age_irl.csv')
            t4.to_csv('ed_subset/fam_stat_irl.csv')
            t6.to_csv('ed_subset/house_stat_irl.csv')
            t8_1.to_csv('ed_subset/prince_stat_irl.csv')
            t9_1.to_csv('ed_subset/job_stat_irl.csv')
            t14_1.to_csv('ed_subset/ind_stat_irl.csv')

            natave_df = pd.concat([t1, t2_1, t4, t5, t6, t8_1, t9_1, t10_4, t11, t13_1, t14_1, et1], axis=1)

            natave_df.to_csv('ed_subset/natave_data_2016.csv', index=False)

        migrate_dataframe(t1, 'prac_sexagemarriage')
        migrate_dataframe(t2_1, 'prac_pobnat')
        migrate_dataframe(t4, 'prac_families')
        migrate_dataframe(t5, 'prac_privhh')
        migrate_dataframe(t6, 'prac_housing')
        migrate_dataframe(t8_1, 'prac_princstat')
        migrate_dataframe(t9_1, 'prac_socclass')
        migrate_dataframe(t10_4, 'prac_education')
        migrate_dataframe(t11, 'prac_commuting')
        migrate_dataframe(t13_1, 'prac_occupation')
        migrate_dataframe(t14_1, 'prac_industries')
        migrate_dataframe(et1, 'prac_ageext')


    query_database('prac_csoref')
    query_database('prac_sexagemarriage')
    query_database('prac_pobnat')
    query_database('prac_families')
    query_database('prac_privhh')
    query_database('prac_housing')
    query_database('prac_princstat')
    query_database('prac_socclass')
    query_database('prac_education')
    query_database('prac_commuting')
    query_database('prac_occupation')
    query_database('prac_industries')
    query_database('prac_ageext')

if __name__ == "__main__":
    main()