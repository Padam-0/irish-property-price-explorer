import pandas as pd


def gen_natave_2011():
    df = pd.read_csv('ed_subset/natave_data_2011.csv', index_col=0)

    age_df = df.ix[:, 2:21]
    age_total = age_df.values[0][-1]
    age_data = list(age_df.values[0] / age_total)[:-1]

    age_labels = ['0 - 4', "5 - 9", "10 - 14", "15 - 19", "20 - 24", "25 - 29",
                  "30 - 34", "35 - 39", "40 - 44", "45 - 49", "50 - 54",
                  "55 - 59",
                  "60 - 64", "65 - 69", "70 - 74", "75 - 79", "80 - 84", "85+"]

    rel_labels = ['Single', 'Married', 'Separated', 'Divorced', 'Widowed']

    rel_df = df.ix[:, 21:27]
    rel_total = rel_df.values[0][-1]
    rel_data = list(rel_df.values[0] / rel_total)[:-1]

    nat_labels = ['Irish', 'United Kingdom', 'Polish', 'Lithuanian',
                  'Other EU',
                  'Rest of World', 'Not Stated']

    nat_df = df.ix[:, 38:46]
    nat_total = nat_df.values[0][-1]
    nat_data = list(nat_df.values[0] / nat_total)[:-1]

    child_labels = ["No Children", "1 Child", "2 Children", "3 Children",
                    "4 Children", "5 or More Children"]

    child_df = df.ix[:, 49:55]
    child_total = sum(child_df.values[0])
    child_data = list(child_df.values[0] / child_total)

    fam_labels = ['Pre-Family', 'Empty Nest', 'Retired', 'Pre-School', 'Early School',
                  'Pre-Teen', 'Teenager', 'Adult']

    fam_df = df.ix[:, 55:64]
    fam_total = fam_df.values[0][-1]
    fam_data = list(fam_df.values[0] / fam_total)[:-1]

    hh_labels = ['One Person Household', 'Two Person Household',
                 'Three Person Household', 'Four Person Household',
                 'Five Person Household', 'Six Person Household',
                 'Seven Person Household', 'More than Eight Person Household']

    hh_df = df.ix[:, 82:91]
    hh_total = hh_df.values[0][-1]
    hh_data = list(hh_df.values[0] / hh_total)[:-1]

    house_type_labels = ['House or Bungalow', 'Flat or Apartment', 'Bed-sit',
                         'Caravan', 'Not Stated']

    house_type_df = df.ix[:, 94:100]
    house_type_total = house_type_df.values[0][-1]
    house_type_data = list(house_type_df.values[0] / house_type_total)[:-1]

    house_age_labels = ['Before 1919', '1919 - 1945', '1946 - 1960',
                        '1961 - 1970', '1971 - 1980', '1981 - 1990',
                        '1991 - 2000',
                        '2001 - 2010', 'After 2011', 'Not Stated']

    house_age_df = df.ix[:, 100:111]
    house_age_total = house_age_df.values[0][-1]
    house_age_data = list(house_age_df.values[0] / house_age_total)[:-1]

    hh_occupancy_labels = ['Owner Occupier with Mortgage',
                           'Owner Occupier without Mortgage',
                           'Rented from Private Landlord',
                           'Rented from Local Authority',
                           'Rented from Voluntary Body', 'Rented Free of Rent',
                           'Not Stated']

    hh_occupancy_df = df.ix[:, 111:119]
    hh_occupancy_total = hh_occupancy_df.values[0][-1]
    hh_occupancy_data = list(hh_occupancy_df.values[0] / hh_occupancy_total)[
                        :-1]

    hh_rooms_labels = ['1 Room', '2 Rooms', '3 Rooms', '4 Rooms', '5 Rooms',
                       '6 Rooms', '7 Rooms', 'More than 8 Rooms', 'Not Stated']

    hh_rooms_df = df.ix[:, 119:129]
    hh_rooms_total = hh_rooms_df.values[0][-1]
    hh_rooms_data = list(hh_rooms_df.values[0] / hh_rooms_total)[:-1]

    hh_occupation_labels = ['Occupied', 'Temporarily Unoccupied',
                            'Unoccupied Holiday Home', 'Unoccupied']

    hh_occupation_df = df.ix[:, 129:133]
    hh_occupation_total = sum(hh_occupation_df.values[0])
    hh_occupation_data = list(hh_occupation_df.values[0] / hh_occupation_total)

    prince_stat_labels = ['Working', 'Looking for First Job', 'Unemployed',
                          'Student', 'Looking After Home/Family', 'Retired',
                          'Sick or Disabled',
                          'Other']

    prince_stat_df = df.ix[:, 136:145]
    prince_stat_total = prince_stat_df.values[0][-1]
    prince_stat_data = list(prince_stat_df.values[0] / prince_stat_total)[:-1]

    socclass_labels = ['Professional Worker', 'Managerial and Technical',
                       'Non-Manual', 'Skilled Manual',
                       'Semi-Skilled', 'Unskilled', 'All Others']

    socclass_df = df.ix[:, 148:156]
    socclass_total = socclass_df.values[0][-1]
    socclass_data = list(socclass_df.values[0] / socclass_total)[:-1]

    education_labels = ['No Formal Education', 'Primary', 'Lower Secondary',
                        'Upper Secondary', 'Technical Vocatation',
                        'Apprenticeship',
                        'Higher Certificate', 'Bachelors Degree',
                        'Bachelors Degree (Hons)',
                        'Postgraduate Degree', 'Doctorate', 'Not Stated']

    education_df = df.ix[:, 159:172]
    education_total = education_df.values[0][-1]
    education_data = list(education_df.values[0] / education_total)[:-1]

    transport_method_labels = ['Walking', 'Cycling', 'Bus', 'Train',
                               'Motorbike', 'Car (Driver)', 'Car (Passenger)',
                               'Van', 'Other', 'Not Stated']

    transport_method_df = df.ix[:, 175:185]
    transport_method_total = sum(transport_method_df.values[0])
    transport_method_data = list(
        transport_method_df.values[0] / transport_method_total)

    transport_time_labels = ['Under 15 minutes', '15 - 30 minutes',
                             '30 - 45 minutes', '45 - 60 minutes',
                             '60 - 90 minutes', 'Over 90 minutes',
                             'Not Stated']

    transport_time_df = df.ix[:, 186:194]
    transport_time_total = transport_time_df.values[0][-1]
    transport_time_data = list(
        transport_time_df.values[0] / transport_time_total)[:-1]

    occupation_labels = ['Managers, Directors and Senior Officials',
                         'Professional Occupations',
                         'Associate Professional and Technical Occupations',
                         'Administrative and Secretarial Occupations',
                         'Skilled Trades Occupations',
                         'Caring, Leisure and Other Service Occupations',
                         'Sales and Customer Service Occupations ',
                         'Process, Plant and Machine Operatives',
                         'Elementary Occupations',
                         'Not Stated']

    occupation_df = df.ix[:, 197:208]
    occupation_total = occupation_df.values[0][-1]
    occupation_data = list(occupation_df.values[0] / occupation_total)[:-1]

    industry_labels = ['Agriculture, Forestry and Fishing',
                       'Building and Construction', 'Manufacturing',
                       'Commerce and Trade',
                       'Transport and Communications ',
                       'Public Administration',
                       'Professional Services', 'Other']

    industry_df = df.ix[:, 211:220]
    industry_total = industry_df.values[0][-1]
    industry_data = list(industry_df.values[0] / industry_total)[:-1]

    age_m_df = df.ix[:, 223:241]
    age_m_total = age_m_df.values[0].sum()
    age_m_data = list(age_m_df.values[0] / age_m_total)

    age_f_df = df.ix[:, 241:259]
    age_f_total = age_f_df.values[0].sum()
    age_f_data = list(age_f_df.values[0] / age_f_total)

    df_list = [[age_labels, age_data, 'age'], [rel_labels, rel_data, 'rel'],
               [nat_labels, nat_data, 'nat'],
               [child_labels, child_data, 'child'],
               [fam_labels, fam_data, 'fam'], [hh_labels, hh_data, 'hh'],
               [house_type_labels, house_type_data, 'house_type'],
               [house_age_labels, house_age_data, 'house_age'],
               [hh_occupancy_labels, hh_occupancy_data, 'hh_occupancy'],
               [hh_rooms_labels, hh_rooms_data, 'hh_rooms'],
               [hh_occupation_labels, hh_occupation_data, 'hh_occupation'],
               [prince_stat_labels, prince_stat_data, 'prince_stat'],
               [socclass_labels, socclass_data, 'socclass'],
               [education_labels, education_data, 'education'],
               [transport_method_labels, transport_method_data,
                'transport_method'],
               [transport_time_labels, transport_time_data, 'transport_time'],
               [occupation_labels, occupation_data, 'occupation'],
               [industry_labels, industry_data, 'ind'],
               [age_labels, age_m_data, 'age_m'],
               [age_labels, age_f_data, 'age_f']]

    dict = {}
    other = {}
    ns = {}
    age_m = {}
    age_f = {}

    for df_group in df_list:
        for i in range(len(df_group[0])):
            if df_group[0][i] == 'Not Stated':
                ns[df_group[2]] = df_group[1][i]
            elif df_group[0][i] == 'Other':
                other[df_group[2]] = df_group[1][i]
            elif df_group[0][i] in age_labels and df_group[2] == 'age_m':
                age_m[df_group[0][i]] = df_group[1][i]
            elif df_group[0][i] in age_labels and df_group[2] == 'age_f':
                age_f[df_group[0][i]] = df_group[1][i]
            else:
                dict[df_group[0][i]] = df_group[1][i]

    dict['Other'] = other
    dict['Not Stated'] = ns
    dict['age_m'] = age_m
    dict['age_f'] = age_f

    return dict

def gen_natave_2016():
    df = pd.read_csv('ed_subset/natave_data_2016.csv', index_col=0)

    age_df = df.ix[:, 2:21]
    age_total = age_df.values[0][-1]
    age_data = list(age_df.values[0]/age_total)[:-1]

    age_labels = ['0 - 4', "5 - 9", "10 - 14", "15 - 19", "20 - 24", "25 - 29",
                  "30 - 34", "35 - 39", "40 - 44", "45 - 49", "50 - 54", "55 - 59",
                  "60 - 64", "65 - 69", "70 - 74", "75 - 79", "80 - 84", "85+"]

    rel_labels = ['Single', 'Married', 'Separated', 'Divorced', 'Widowed']

    rel_df = df.ix[:, 21:27]
    rel_total = rel_df.values[0][-1]
    rel_data = list(rel_df.values[0]/rel_total)[:-1]

    nat_labels = ['Irish', 'United Kingdom', 'Polish', 'Lithuanian', 'Other EU',
                  'Rest of World', 'Not Stated']

    nat_df = df.ix[:, 38:46]
    nat_total = nat_df.values[0][-1]
    nat_data = list(nat_df.values[0]/nat_total)[:-1]

    child_labels = ["No Children", "1 Child", "2 Children", "3 Children",
                    "4 Children", "5 or More Children"]

    child_df = df.ix[:, 49:55]
    child_total = sum(child_df.values[0])
    child_data = list(child_df.values[0]/child_total)

    fam_labels = ['Pre-Family', 'Empty Nest', 'Retired', 'Pre-School', 'Early School',
                  'Pre-Teen', 'Teenager', 'Adult']

    fam_df = df.ix[:, 55:64]
    fam_total = fam_df.values[0][-1]
    fam_data = list(fam_df.values[0]/fam_total)[:-1]

    hh_labels = ['One Person Household', 'Two Person Household',
                 'Three Person Household', 'Four Person Household',
                 'Five Person Household', 'Six Person Household',
                 'Seven Person Household', 'More than Eight Person Household']

    hh_df = df.ix[:, 82:91]
    hh_total = hh_df.values[0][-1]
    hh_data = list(hh_df.values[0]/hh_total)[:-1]

    house_type_labels = ['House or Bungalow', 'Flat or Apartment', 'Bed-sit',
                         'Caravan', 'Not Stated']

    house_type_df = df.ix[:, 94:100]
    house_type_total = house_type_df.values[0][-1]
    house_type_data = list(house_type_df.values[0]/house_type_total)[:-1]

    house_age_labels = ['Before 1919', '1919 - 1945', '1946 - 1960',
                        '1961 - 1970', '1971 - 1980', '1981 - 1990', '1991 - 2000',
                        '2001 - 2010', 'After 2011', 'Not Stated']

    house_age_df = df.ix[:, 100:111]
    house_age_total = house_age_df.values[0][-1]
    house_age_data = list(house_age_df.values[0]/house_age_total)[:-1]

    hh_occupancy_labels = ['Owner Occupier with Mortgage', 'Owner Occupier without Mortgage',
                           'Rented from Private Landlord', 'Rented from Local Authority',
                           'Rented from Voluntary Body', 'Rented Free of Rent', 'Not Stated']

    hh_occupancy_df = df.ix[:, 111:119]
    hh_occupancy_total = hh_occupancy_df.values[0][-1]
    hh_occupancy_data = list(hh_occupancy_df.values[0]/hh_occupancy_total)[:-1]

    hh_rooms_labels = ['1 Room', '2 Rooms', '3 Rooms', '4 Rooms', '5 Rooms',
                       '6 Rooms', '7 Rooms', 'More than 8 Rooms', 'Not Stated']

    hh_rooms_df = df.ix[:, 119:129]
    hh_rooms_total = hh_rooms_df.values[0][-1]
    hh_rooms_data = list(hh_rooms_df.values[0]/hh_rooms_total)[:-1]

    hh_occupation_labels = ['Occupied', 'Temporarily Unoccupied', 'Unoccupied Holiday Home', 'Unoccupied']

    hh_occupation_df = df.ix[:, 129:133]
    hh_occupation_total = sum(hh_occupation_df.values[0])
    hh_occupation_data = list(hh_occupation_df.values[0]/hh_occupation_total)

    prince_stat_labels = ['Working', 'Looking for First Job', 'Unemployed',
                          'Student', 'Looking After Home/Family', 'Retired', 'Sick or Disabled',
                          'Other']

    prince_stat_df = df.ix[:, 136:145]
    prince_stat_total = prince_stat_df.values[0][-1]
    prince_stat_data = list(prince_stat_df.values[0]/prince_stat_total)[:-1]

    socclass_labels = ['Professional Worker', 'Managerial and Technical',
                       'Non-Manual', 'Skilled Manual',
                       'Semi-Skilled', 'Unskilled', 'All Others']

    socclass_df = df.ix[:, 148:156]
    socclass_total = socclass_df.values[0][-1]
    socclass_data = list(socclass_df.values[0]/socclass_total)[:-1]

    education_labels = ['No Formal Education', 'Primary', 'Lower Secondary',
                        'Upper Secondary', 'Technical Vocatation', 'Apprenticeship',
                        'Higher Certificate', 'Bachelors Degree', 'Bachelors Degree (Hons)',
                        'Postgraduate Degree', 'Doctorate', 'Not Stated']

    education_df = df.ix[:, 159:172]
    education_total = education_df.values[0][-1]
    education_data = list(education_df.values[0]/education_total)[:-1]


    transport_method_labels = ['Walking', 'Cycling', 'Bus', 'Train', 'Motorbike', 'Car (Driver)', 'Car (Passenger)', 'Van', 'Other', 'Not Stated']

    transport_method_df = df.ix[:, 175:185]
    transport_method_total = sum(transport_method_df.values[0])
    transport_method_data = list(transport_method_df.values[0]/transport_method_total)

    transport_time_labels = ['Under 15 minutes', '15 - 30 minutes',
                             '30 - 45 minutes', '45 - 60 minutes',
                             '60 - 90 minutes', 'Over 90 minutes', 'Not Stated']

    transport_time_df = df.ix[:, 186:194]
    transport_time_total = transport_time_df.values[0][-1]
    transport_time_data = list(transport_time_df.values[0]/transport_time_total)[:-1]

    occupation_labels = ['Managers, Directors and Senior Officials', 'Professional Occupations',
                         'Associate Professional and Technical Occupations',
                         'Administrative and Secretarial Occupations',
                         'Skilled Trades Occupations',
                         'Caring, Leisure and Other Service Occupations',
                         'Sales and Customer Service Occupations ',
                         'Process, Plant and Machine Operatives', 'Elementary Occupations',
                         'Not Stated']

    occupation_df = df.ix[:, 197:208]
    occupation_total = occupation_df.values[0][-1]
    occupation_data = list(occupation_df.values[0]/occupation_total)[:-1]

    industry_labels = ['Agriculture, Forestry and Fishing',
                       'Building and Construction', 'Manufacturing', 'Commerce and Trade',
                       'Transport and Communications ', 'Public Administration',
                       'Professional Services', 'Other']

    industry_df = df.ix[:, 211:220]
    industry_total = industry_df.values[0][-1]
    industry_data = list(industry_df.values[0]/industry_total)[:-1]

    age_m_df = df.ix[:, 223:241]
    age_m_total = age_m_df.values[0].sum()
    age_m_data = list(age_m_df.values[0]/age_m_total)

    age_f_df = df.ix[:, 241:259]
    age_f_total = age_f_df.values[0].sum()
    age_f_data = list(age_f_df.values[0]/age_f_total)

    df_list = [[age_labels, age_data, 'age'], [rel_labels, rel_data, 'rel'],
               [nat_labels, nat_data, 'nat'], [child_labels, child_data, 'child'],
               [fam_labels, fam_data, 'fam'], [hh_labels, hh_data, 'hh'],
               [house_type_labels, house_type_data, 'house_type'],
               [house_age_labels, house_age_data, 'house_age'],
               [hh_occupancy_labels, hh_occupancy_data, 'hh_occupancy'],
               [hh_rooms_labels, hh_rooms_data, 'hh_rooms'],
               [hh_occupation_labels, hh_occupation_data, 'hh_occupation'],
               [prince_stat_labels, prince_stat_data, 'prince_stat'],
               [socclass_labels, socclass_data, 'socclass'],
               [education_labels, education_data, 'education'],
               [transport_method_labels, transport_method_data, 'transport_method'],
               [transport_time_labels, transport_time_data, 'transport_time'],
               [occupation_labels, occupation_data, 'occupation'],
               [industry_labels, industry_data, 'ind'], [age_labels, age_m_data, 'age_m'],
               [age_labels, age_f_data, 'age_f']]

    dict = {}
    other = {}
    ns = {}
    age_m = {}
    age_f = {}

    for df_group in df_list:
        for i in range(len(df_group[0])):
            if df_group[0][i] == 'Not Stated':
                ns[df_group[2]] = df_group[1][i]
            elif df_group[0][i] == 'Other':
                other[df_group[2]] = df_group[1][i]
            elif df_group[0][i] in age_labels and df_group[2] == 'age_m':
                age_m[df_group[0][i]] = df_group[1][i]
            elif df_group[0][i] in age_labels and df_group[2] == 'age_f':
                age_f[df_group[0][i]] = df_group[1][i]
            else:
                dict[df_group[0][i]] = df_group[1][i]

    dict['Other'] = other
    dict['Not Stated'] = ns
    dict['age_m'] = age_m
    dict['age_f'] = age_f

    return dict

def main():
    a = gen_natave_2011()
    b = gen_natave_2016()

    with open('natave.js', 'w') as f:
        f.write("var natave11 = ")
        f.write(str(a))
        f.write(';\n')
        f.write("var natave16 = ")
        f.write(str(b))
        f.write(';')

if __name__ == '__main__':
    main()