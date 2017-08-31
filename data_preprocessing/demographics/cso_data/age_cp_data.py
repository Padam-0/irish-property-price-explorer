import pandas as pd
import numpy as np
import operator
from datetime import date, datetime, timedelta
import calendar
import re
import csv
from sklearn.externals import joblib
from tqdm import tqdm

def get_age_risk(apm, apf, anm, anf):
    auc_l = 0
    auc_h = 0

    for i in range(len(anm)):
        l = anm[i]['label']

        if len(l) == 5:
            ma = np.mean([int(l[0]), int(l[-1])]) + 0.5
        elif len(l) == 3:
            ma = 90
        else:
            ma = np.mean([int(l[:2]), int(l[-2:])]) + 0.5

        m_na = anm[i]['value']
        m = apm[i]['value']

        if m_na > m:
            auc_l += (m_na - m) * ma
        else:
            auc_h += (m - m_na) * ma

        f_na = anf[i]['value']
        f = apf[i]['value']

        if f_na > f:
            auc_l += (f_na - f) * ma
        else:
            auc_h += (f - f_na) * ma

    return auc_h, auc_l

def main():
    df = pd.read_csv('eds.csv', encoding='latin1')

    df = df[['OSM_ID', 'NAME_TAG', 'AREA', 'LATITUDE', 'LONGITUDE', 'CO_NAME']]
    # print(df['NAME_TAG'].value_counts())

    with open('./cross_ref_dict.txt') as f:
        cross_ref_dict = eval(f.read())

    #Maps from TL UID to CSO Name
    uid_dict = {}
    ignore_list = []
    #Maps from CSO name to TL UID
    tl_dict = {}
    # print(df[df['NAME_TAG'] == 'Castletown'])
    for i in df.index:
        try:
            uid_dict[df.loc[i, 'OSM_ID']] = cross_ref_dict[df.loc[i, 'NAME_TAG']]
            tl_dict[cross_ref_dict[df.loc[i, 'NAME_TAG']]] = df.loc[i, 'NAME_TAG']
        except:
            ignore_list.append(df.loc[i, 'OSM_ID'])

    cso_ref = pd.read_csv('ed_subset/cso_ref.csv', index_col=0)
    age_ed = pd.read_csv('ed_subset/mf_age_ed.csv', index_col=0)
    age_irl = pd.read_csv('ed_subset/mf_age_irl.csv', index_col=0).iloc[0, 3:39]

    fam_ed = pd.read_csv('ed_subset/fam_stat_ed.csv', index_col=1)[['empty_nest', 'retired', 'fam_total']]
    fam_irl = pd.read_csv('ed_subset/fam_stat_irl.csv').ix[:, 10:]

    ind_ed = pd.read_csv('ed_subset/ind_stat_ed.csv', index_col=1).ix[:,3:]
    ind_irl = pd.read_csv('ed_subset/ind_stat_irl.csv').ix[:,4:]

    job_ed = pd.read_csv('ed_subset/job_stat_ed.csv', index_col=1).ix[:,3:]
    job_irl = pd.read_csv('ed_subset/job_stat_irl.csv').ix[:, 4:]

    prince_ed = pd.read_csv('ed_subset/prince_stat_ed.csv', index_col=1).ix[:,3:]
    prince_irl = pd.read_csv('ed_subset/prince_stat_irl.csv').ix[:, 4:]

    house_ed = pd.read_csv('ed_subset/house_stat_ed.csv', index_col=1).ix[:, 20:]
    house_irl = pd.read_csv('ed_subset/house_stat_irl.csv', index_col=1).ix[:, 20:]

    mort_ed = house_ed.ix[:, :8]
    mort_irl = house_irl.ix[:, :8]
    occu_ed = house_ed.ix[:,-4:]
    occu_irl = house_irl.ix[:, -4:]

    age_scores = {}
    fam_scores = {}
    ind_scores = {}
    job_scores = {}
    prince_scores = {}
    mort_scores = {}
    occu_scores = {}

    pred_scores = {}
    pred_info = []

    for i in tqdm(df.index):
    # for i in tqdm(df.index[575:576]):
        input_data = {}
        lat = df.loc[i, 'LATITUDE']
        lng = df.loc[i, 'LONGITUDE']

        location = {'lng': lat, 'lat': lng}
        county = df.loc[i, 'CO_NAME']

        tl_name = df.loc[i, 'NAME_TAG']
        try:
            cso_name = cross_ref_dict[tl_name]
            cso_id = cso_ref[cso_ref['desc'] == cso_name]['uid'].values[0]
        except:
            continue

        if len(cso_id) != 5 or cso_id[0] != 'E':
            continue

        input_data['address'] = ''
        input_data['type'] = get_common('type', tl_name, county)
        input_data['condition'] = get_common('condition', tl_name, county)
        input_data['bed'] = get_common('beds', tl_name, county)
        input_data['bath'] = get_common('baths', tl_name, county)

        input_data['apt'] = regex_apt(input_data['address'])
        input_data['house_name'] = regex_house(input_data['address'])

        input_data['suffix'] = regex_suffix(input_data['address'])

        start = date(2010, 1, 1)
        today = date.today()
        input_data['date'] = (today - start).days

        input_data['type'] = desc_map(input_data['type'])
        input_data['condition'] = cond_map(input_data['condition'])
        input_data['apt'] = apt_map(input_data['apt'])
        input_data['house_name'] = name_map(input_data['house_name'])
        input_data['suffix'] = suffix_map(input_data['suffix'])
        input_data['ed'] = tl_name

        if str(county) == 'nan':
            pred_scores[tl_name] = 'NEDTMP'
            continue



        model_choice, county = find_model(county, input_data['ed'])
        z = ed_map(input_data['ed'])
        if z == 'NEDTMP':
            pred_scores[cso_id] = z
            continue
        else:
            input_data['ed'] = z

        input_data['county'] = county_map(county)

        prediction = float(full_pred(input_data, location, model_choice)[0])

        baseline = float(ti_pred(input_data, location, model_choice)[0])

        moe = float(get_moe(model_choice))

        if prediction > (baseline + moe):
            pred_scores[cso_id] = (prediction - (baseline + moe)) / 191580.51
        elif prediction < baseline - moe:
            pred_scores[cso_id] = (baseline + moe) - prediction / 191580.51
        else:
            pred_scores[cso_id] = 0

    # price_12m_scores = {}
    # price_24m_scores = {}
    # data_df = pd.read_csv('../good_data_ed.csv', index_col='sale_date')
    #
    # today = datetime.today()
    # m12 = timedelta(weeks=104)
    # m24 = timedelta(weeks=156)
    #
    # for ed in tqdm(cso_ref['uid'].values):
    #     cso_name = cso_ref[cso_ref['uid'] == ed]['desc'].values[0]
    #
    #     try:
    #         tl_name = tl_dict[cso_name]
    #     except:
    #         price_12m_scores[ed] = [0, 0]
    #         price_24m_scores[ed] = [0, 0]
    #     min_df = data_df[data_df['ed'] == tl_name]
    #
    #     min_df = min_df.set_index(pd.DatetimeIndex(min_df.index))
    #     min_df_12m = min_df[min_df.index > today - m12]
    #     min_df_12m = min_df_12m.resample('M').mean().dropna(axis=0, how='any')
    #     min_df_24m = min_df[min_df.index > today - m24]
    #     min_df_24m = min_df_24m.resample('M').mean().dropna(axis=0, how='any')
    #
    #     roc = 0
    #
    #     if len(min_df_12m.index) < 6:
    #         price_12m_scores[ed] = [0, 0]
    #     else:
    #         sales_data = [[calendar.timegm(min_df_12m.index[i].timetuple()), int(min_df_12m.ix[i, 'price'])] for i in range(len(min_df_12m.index))]
    #         p = np.polyfit([i[0] for i in sales_data], [i[1] for i in sales_data], deg=1)
    #         score = float(p[0]) - 0.000176
    #
    #         p1 = min_df_12m.iloc[0, :].price
    #         t2 = calendar.timegm(min_df_12m.index[-1].timetuple())
    #
    #         pred = p[0] * t2 + p[1]
    #         roc = round((pred - p1) / p1 * 100, 2)
    #
    #
    #         if score > 0:
    #             price_12m_scores[ed] = [score / 0.06938963, roc]
    #         else:
    #             price_12m_scores[ed] = [score / 0.21746398, roc]
    #
    #     if len(min_df_24m.index) < 12:
    #         price_24m_scores[ed] = [0, 0]
    #     else:
    #         sales_data = [[calendar.timegm(min_df_24m.index[i].timetuple()), int(min_df_24m.ix[i, 'price'])] for i in range(len(min_df_24m.index))]
    #         p = np.polyfit([i[0] for i in sales_data], [i[1] for i in sales_data], deg=1)
    #
    #         pred = p[0] * t2 + p[1]
    #
    #         roc = round((pred - p1) / p1 * 50, 2)
    #
    #         if score > 0:
    #             price_24m_scores[ed] = [score, roc]
    #         else:
    #             price_24m_scores[ed] = [score, roc]



    for ed in cso_ref['uid'].values:
        age_data = age_ed.ix[ed, 2:38]

        age_males = age_data.iloc[:18].values
        age_females = age_data.iloc[18:].values
        age_na_males = age_irl.iloc[:18].values
        age_na_females = age_irl.iloc[18:].values

        pop_m = sum(age_males)
        pop_f = sum(age_females)
        npop_m = sum(age_na_males)
        npop_f = sum(age_na_females)

        age_labels = ['0 - 4', "5 - 9", "10 - 14", "15 - 19", "20 - 24", "25 - 29",
                      "30 - 34", "35 - 39", "40 - 44", "45 - 49", "50 - 54", "55 - 59",
                      "60 - 64", "65 - 69", "70 - 74", "75 - 79", "80 - 84", "85+"]

        age_profile_males = []
        age_natave_males = []
        age_profile_females = []
        age_natave_females = []

        for i in range(len(age_labels)):
            age_profile_males.append({'label': age_labels[i], 'value': round((age_males[i] / pop_m) * 100, 2)})
            age_natave_males.append({'label': age_labels[i], 'value': round((age_na_males[i] / npop_m) * 100, 2)})
            age_profile_females.append({'label': age_labels[i], 'value': round((age_females[i] / pop_f) * 100, 2)})
            age_natave_females.append({'label': age_labels[i], 'value': round((age_na_females[i] / npop_f) * 100, 2)})

        auc_h, auc_l = get_age_risk(age_profile_males, age_profile_females, age_natave_males, age_natave_females)

        if auc_h > 1150:
            score = (auc_h - 1150) / 3513.3
        elif auc_l > 500:
            score = -(auc_l - 500) / 2564.875
        else:
            score = 0

        age_scores[ed] = score
        score = 0

        fam_data = fam_ed.ix[ed, :]

        enest = fam_data['empty_nest'] / fam_data['fam_total']
        retired = fam_data['retired'] / fam_data['fam_total']
        nat_enest = fam_irl['empty_nest'] / fam_irl['fam_total']
        nat_ret = fam_irl['retired'] / fam_irl['fam_total']

        enest_dif = ((enest - nat_enest[0]) - 0.00969125399499)
        if enest_dif > 0:
            enest_dif *= 6.661
        else:
            enest_dif *= 13.86898

        ret_dif = retired - nat_ret[0] - 0.00767528986966

        if ret_dif > 0:
            ret_dif *= 5.064482
        else:
            ret_dif *= 14.19685

        score = max([ret_dif, enest_dif], key=abs)

        fam_scores[ed] =  score
        score = 0

        ind_data = ind_ed.ix[ed, :]

        ind_data_norm = {}
        for i in ind_data.index[:-1]:
            ind_data_norm[i] = ind_data[i] / ind_data['ind_total']

        ind_conc_lab = max(ind_data_norm.items(), key=operator.itemgetter(1))[0]

        ind_conc = ind_data_norm[ind_conc_lab] - 0.26326761909
        if ind_conc > 0:
            score = ind_conc * 2.69757
        else:
            score = ind_conc * 10.714326

        ind_scores[ed] = score
        score = 0

        job_data = job_ed.ix[ed, :]

        job_data_norm = {}
        for i in job_data.index[:-1]:
            job_data_norm[i] = job_data[i] / job_data['class_total']

        job_conc_lab = \
        max(job_data_norm.items(), key=operator.itemgetter(1))[0]

        job_conc = job_data_norm[job_conc_lab] - 0.297725257914

        if job_conc > 0:
            score = job_conc * 2.3786635
        else:
            score = job_conc * 8.9208851

        job_scores[ed] = score
        score = 0

        prince_data = prince_ed.ix[ed, :]

        work = prince_data['work'] / prince_data['stat_total']
        work_na = (prince_irl['work'] / prince_irl['stat_total'])[0]

        prince_dif = work_na - work - 0.00946905702157
        if prince_dif > 0:
            score = prince_dif * 2.6831456
        else:
            score = prince_dif * 4.627491557

        prince_scores[ed] = score
        score = 0

        mort_data = mort_ed.ix[ed, :]

        mortgage = mort_data['oo_wm'] / mort_data['occu_total_hh']
        mortgage_na = (mort_irl['oo_wm'] / mort_irl['occu_total_hh'])[0]

        mort_dif = mortgage_na - mortgage + 0.00389068168268
        if mort_dif > 0:
            score = mort_dif * 3.15902409
        else:
            score = mort_dif * 3.09185797

        mort_scores[ed] = score
        score = 0

        occu_data = occu_ed.ix[ed, :]
        occu = occu_data['occupied'] / sum(occu_data.values)

        na_occu = (occu_irl['occupied'].values / occu_irl.values.sum())[0]

        occu_dif = na_occu - occu - 0.0287921128283
        if occu_dif > 0:
            score = occu_dif * 1.779594
        else:
            score = occu_dif * 5.661914

        occu_scores[ed] = score


    with open('age_cp_data.js', 'w') as f:
        f.write("var age_ref = ")
        f.write(str(age_scores).replace(' ', ""))
        f.write(';\n\n')
        f.write("var fam_ref = ")
        f.write(str(fam_scores).replace(' ', ""))
        f.write(';')
        f.write(';\n\n')
        f.write("var ind_ref = ")
        f.write(str(ind_scores).replace(' ', ""))
        f.write(';')
        f.write(';\n\n')
        f.write("var job_ref = ")
        f.write(str(job_scores).replace(' ', ""))
        f.write(';')
        f.write(';\n\n')
        f.write("var prince_ref = ")
        f.write(str(prince_scores).replace(' ', ""))
        f.write(';')
        f.write(';\n\n')
        f.write("var mort_ref = ")
        f.write(str(mort_scores).replace(' ', ""))
        f.write(';')
        f.write(';\n\n')
        f.write("var occu_ref = ")
        f.write(str(occu_scores).replace(' ', ""))
        f.write(';\n\n')
        f.write("var pred_ref = ")
        f.write(str(pred_scores).replace(' ', ""))
        f.write(';')

    # with open('../../prac/reporter/static/reporter/js/roc_data.js', 'w') as f:
    #     f.write("var m12_ref = ")
    #     f.write(str(price_12m_scores).replace(' ', ""))
    #     f.write(';\n\n')
    #     f.write("var m24_ref = ")
    #     f.write(str(price_24m_scores).replace(' ', ""))
    #     f.write(';')



def get_moe(string):
    file_location = '../../prac/predictive_model/models/model_results.csv'

    if string == 'County':
        pstring = 'Rural'
    else:
        pstring = string

    reader = csv.reader(open(file_location, 'r'))
    d = {}
    for row in reader:
        model, moe, _ = row
        d[model] = moe

    return d[pstring.lower()]


def find_model(county, ed):
    county_list = ['Leitrim', 'Mayo', 'Roscommon', 'Kildare', 'Sligo', 'Kilkenny',
                   'Laois', 'Longford', 'Louth', 'Meath', 'Westmeath', 'Offaly',
                   'Wexford', 'Clare', 'Wicklow', 'Kerry', 'Tipperary',
                   'Donegal', 'Cavan', 'Monaghan']

    if county == 'Dublin':
        return 'Dublin', county
    elif county in county_list:
        return 'County', county
    else:
        file_location = '../../prac/predictive_model/mappings/eds_location_split.csv'
        reader = csv.reader(open(file_location, 'r'))
        d = {}
        for row in reader:
            x, i, k, y, v = row
            d[k] = v

        try:
            model = d[ed]
        except:
            return 'County', county + " County"

        if model == "County":
            return model, county + " County"
        else:
            return model, county + " City"


def word_isolation(string):
    keep_words = ['road', 'park', 'avenue', 'court', 'rd', 'street', 'drive', 'st',
                  'grove', 'manor', 'close', 'green', 'view', 'hill', 'house', 'the',
                  'wood', 'terrace', 'heights', 'hall', 'mount', 'grange',
                  'lodge', 'lane', 'main', 'place', 'lawn', 'ave', 'square', 'dr',
                  'estate', 'woodlands', 'harbour', 'quay', 'bay', 'apt', 'sq', 'apartment']
    words = string.split()
    for word in words:
        if word in keep_words:
            return word


def word_map(string):
    if string == 'st':
        return 'street'
    elif string == 'rd':
        return 'road'
    elif string == 'ave':
        return 'avenue'
    elif string == 'dr':
        return 'drive'
    elif string == 'apt':
        return 'apartment'
    elif string == 'sq':
        return 'square'
    else:
        return string


def ti_pred(data, location, model_choice):

    if model_choice == 'Dublin':
        model_location = '../../prac/predictive_model/dublin_model_time_independent.pkl'
    elif model_choice == 'Urban':
        model_location = '../../prac/predictive_model/urban_model_time_independent.pkl'
    elif model_choice == 'County':
        model_location = '../../prac/predictive_model/rural_model_time_independent.pkl'
    else:
        model_location = None
        print("Error - No model could be chosen")

    clf = joblib.load(model_location)

    X = np.asarray([data['county'], data['type'], data['bed'],
                    data['bath'], location['lat'], location['lng'],
                    data['condition'], data['apt'], data['house_name'],
                    data['suffix'], data['ed']]).reshape(1, -1)

    prediction = clf.predict(X)

    return prediction


def full_pred(data, location, model_choice):
    # print(data)
    if model_choice == 'Dublin':
        # print("Dublin model chosen")
        model_location = '../../prac/predictive_model/dublin_model.pkl'
    elif model_choice == 'Urban':
        # print("Urban model chosen")
        model_location = '../../prac/predictive_model/urban_model.pkl'
    elif model_choice == 'County':
        # print("Rural model chosen")
        model_location = '../../prac/predictive_model/rural_model.pkl'
    else:
        model_location = None
        print("Error - No model could be chosen")

    clf = joblib.load(model_location)

    X = np.asarray([data['county'], data['type'], data['bed'],
                    data['bath'], location['lat'], location['lng'],
                    data['condition'], data['apt'], data['house_name'],
                    data['suffix'], data['ed'], data['date']]).reshape(1, -1)

    return clf.predict(X)


def county_map(string):
    if string == 'Carlow County' or string == 'Carlow City':
        sstring = 'Carlow'
    else: sstring = string

    county_mapping = {"Carlow":0, "Cavan":1, "Clare":2, "Cork City":3, "Cork County":3, "Donegal":4, "Dublin":5,
                  "Galway City":6, "Galway County":6, "Kerry":7, "Kildare":8, "Kilkenny":9, "Laois":10, "Leitrim":11,
                  "Limerick City":12, "Limerick County":12, "Longford":13, "Louth":14, "Mayo":15, "Meath":16,
                  "Monaghan":17, "Offaly":18, "Roscommon":19, "Sligo":20, "Tipperary":21,
                  "Waterford City":22,"Waterford County":22, "Westmeath":23, "Wexford":24, "Wicklow":25}

    return county_mapping[sstring]


def desc_map(string):
    d = {
        'Semi-Detached House': 0,
        'Detached House': 1,
        'Other': 2,
        'Terraced House': 3
    }
    try:
        return d[string]
    except:
        return 2


def ed_map(string):

    file_location = '../../prac/predictive_model/mappings/eds_location_split.csv'
    reader = csv.reader(open(file_location, 'r'))
    d = {}
    for row in reader:
        _, i, k, v, _ = row
        d[k] = v
    try:
        return d[string]
    except:
        return "NEDTMP"


def cond_map(string):
    cond = {"Second-Hand Dwelling house /Apartment": 0, "New Dwelling house /Apartment": 1}
    return cond[string]


def apt_map(string):
    apt = {"No": 0, "Yes": 1}
    return apt[string]


def name_map(string):
    name = {"No": 0, "Yes": 1}
    return name[string]


def suffix_map(string):
    if string == None:
        string = "None"

    file_location = '../../prac/predictive_model/mappings/suffix_mapping.csv'
    reader = csv.reader(open(file_location, 'r'))
    d = {}
    for row in reader:
        i, k, v = row
        d[k] = v

    return d[string]


def regex_apt(string):
    apt_pattern = re.compile(r'\b[Aa]pt\.?\b|\b[Aa]partment\b')
    if len(re.findall(apt_pattern, string)) > 0:
        return "Yes"
    else:
        return "No"


def regex_house(string):
    hn_pattern = re.compile(r'[0-9]+')
    if len(re.findall(hn_pattern, string)) == 0:
        return 'Yes'
    else:
        return 'No'


def regex_suffix(string):
    string = string.replace('\d+', '').lower().replace(',', '')
    suffix = word_map(word_isolation(string))
    return suffix

def get_common(attr, edist, county):
    # Returns the most common attribute for a given county
    df = pd.read_csv('../../prac/predictive_model/model_data_ed.csv')

    try:
        df = df[df['ed'] == edist]
        if attr == 'type':
            return df['desc'].value_counts().idxmax()
        elif attr == 'condition':
            return df['condition'].value_counts().idxmax()
        elif attr == 'beds':
            return df['bed'].value_counts().idxmax()
        elif attr == 'baths':
            return df['bath'].value_counts().idxmax()
    except:
        try:
            df = df[df['county'] == county]
            if attr == 'type':
                return df['desc'].value_counts().idxmax()
            elif attr == 'condition':
                return df['condition'].value_counts().idxmax()
            elif attr == 'beds':
                return df['bed'].value_counts().idxmax()
            elif attr == 'baths':
                return df['bath'].value_counts().idxmax()
        except:
            if attr == 'type':
                return 'Semi-Detached House'
            elif attr == 'condition':
                return 'Second-Hand Dwelling house /Apartment'
            elif attr == 'beds':
                return 3
            elif attr == 'baths':
                return 1



if __name__ == '__main__':
    main()