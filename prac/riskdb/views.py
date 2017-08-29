from django.shortcuts import render
from .forms import SearchForm
from prac.models import CSORef, SexAgeMarriage, Families, Industries, AgeExt, \
    Housing, PrincStat, SocClass, Occupation
from django.conf import settings
import googlemaps
import matplotlib.path as mplPath
import numpy as np
import json
import operator
from datetime import date
import csv
import re
import pandas as pd
from sklearn.externals import joblib

def geolocate(address_string, data):
    """
    Take address from search bar and return lat & long location if possible.
    :param address_string:
    :return: location, status

    Shorthand for status:
    0 - No search conducted
    1 - Good search results
    2 - Bad / No results
    """
    main_key = 'AIzaSyBFwN-7_erzpXeWWFe3DwMqSPKGoCjj1Hg'
    secondary_key = 'AIzaSyDl2p6S1QgcDxUTypZHk-iR96dBq6uNd-M'

    gmaps = googlemaps.Client(key=secondary_key)
    location = {}
    ed = False

    for feature in data['features']:
        if address_string.lower() == feature['properties']['NAME_TAG'].lower():
            location['lng'] = feature['properties']['LONGITUDE']
            location['lat'] = feature['properties']['LATITUDE']
            ed = True
            status = 1

    if not ed:
        # Add Ireland to search string to remove ambiguity
        address = address_string + ' Ireland'

        # Get results from gmaps API
        geocode_result = gmaps.geocode(address)

        # If a result is returned
        if len(geocode_result) > 0:
            # Set the location as the result
            location = geocode_result[0]['geometry']['location']
            status = 1
        else:
            status = 2

        # Check if location is within east/west boundary of Ireland
        if status is 1:
            if location['lng'] > -10.738539 and location['lng'] < -5.930445:
                pass
            else:
                status = 2

        # Check if location is within north/south boundary of Ireland
        if status is 1:
            if location['lat'] > 51.387652 and location['lat'] < 55.445918:
                pass
            else:
                status = 2

        # If a bad result, set default location
        if status is 2:
            location = {'lng': -6.2603, 'lat': 53.3498}

    return location, status


def check_polygon(polygon, point):

    path = mplPath.Path(polygon)

    inside = path.contains_point(point)

    return inside


def get_ed(location, data):

    point = ([location['lng'], location['lat']])

    for feature in data['features']:

        polygon = np.array(feature['geometry']['coordinates'][0])
        if len(polygon) == 1:
            polygon = polygon[0]
            inside = check_polygon(polygon, point)
        elif len(polygon) <= 10:
            for i in range(len(polygon)):
                subpolygon = polygon[i]
                inside = check_polygon(subpolygon, point)
                if inside == 1:
                    break
        else:
            inside = check_polygon(polygon, point)

        if inside == 1:
            return feature['properties']['NAME_TAG'], feature['properties']['CO_NAME']

    return None


def index(request):
    form = SearchForm()

    location = {'lng': -6.2603, 'lat': 53.3498}
    status = 0
    first = True

    with open(settings.BASE_DIR + '/homepage' + settings.STATIC_URL + 'RRP_timestamp.txt','r') as file:
        lu = file.read()
    with open(settings.BASE_DIR + '/riskdb' + settings.STATIC_URL + 'riskdb/data/cross_ref_dict.txt') as f:
        cross_ref_dict = eval(f.read())
    with open(settings.BASE_DIR + '/riskdb' + settings.STATIC_URL + 'riskdb/data/age_cp_data.txt') as f:
        age_cp_data = eval(f.read())
    with open(settings.BASE_DIR + '/riskdb' + settings.STATIC_URL + 'riskdb/geojson/eds.geojson') as f:
        ed_geojson = json.load(f)

    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            search_address = form.cleaned_data['address']
            location, status = geolocate(search_address, ed_geojson)
            first = False

    if status == 1:
        tl_ed, county = get_ed(location, ed_geojson)
    else:
        tl_ed = None

    if tl_ed == None:
        cso_ed = None
        if first:
            status = 0
        else:
            status = 2
    else:
        try:
            cso_ed = cross_ref_dict[tl_ed]
        except:
            cso_ed = None
            status = 2

    context = {'form': form, 'tl_ed': tl_ed, 'cso_ed': cso_ed, 'status': status}

    if status == 1:
        context['lat'] = location['lat']
        context['lng'] = location['lng']

        ref_id = CSORef.objects.filter(zoom='edist', desc=cso_ed)[0].uid

        context['edist_id'] = ref_id

        t1_data = SexAgeMarriage.objects.filter(uid=ref_id, year=2016)[0]

        age_ext_data = AgeExt.objects.filter(uid=ref_id, year=2016)[0]
        age_ext_natave = AgeExt.objects.filter(zoom='country', year=2016)[0]

        age_males = [
            age_ext_data.age_04_m, age_ext_data.age_59_m, age_ext_data.age_1014_m,
            age_ext_data.age_1519_m, age_ext_data.age_2024_m, age_ext_data.age_2529_m,
            age_ext_data.age_3034_m, age_ext_data.age_3539_m, age_ext_data.age_4044_m,
            age_ext_data.age_4549_m, age_ext_data.age_5054_m, age_ext_data.age_5559_m,
            age_ext_data.age_6064_m, age_ext_data.age_6569_m, age_ext_data.age_7074_m,
            age_ext_data.age_7579_m, age_ext_data.age_8084_m, age_ext_data.age_85p_m
        ]

        age_na_males = [
            age_ext_natave.age_04_m, age_ext_natave.age_59_m, age_ext_natave.age_1014_m,
            age_ext_natave.age_1519_m, age_ext_natave.age_2024_m, age_ext_natave.age_2529_m,
            age_ext_natave.age_3034_m, age_ext_natave.age_3539_m, age_ext_natave.age_4044_m,
            age_ext_natave.age_4549_m, age_ext_natave.age_5054_m, age_ext_natave.age_5559_m,
            age_ext_natave.age_6064_m, age_ext_natave.age_6569_m, age_ext_natave.age_7074_m,
            age_ext_natave.age_7579_m, age_ext_natave.age_8084_m, age_ext_natave.age_85p_m
        ]

        age_females = [
            age_ext_data.age_04_f, age_ext_data.age_59_f, age_ext_data.age_1014_f,
            age_ext_data.age_1519_f, age_ext_data.age_2024_f, age_ext_data.age_2529_f,
            age_ext_data.age_3034_f, age_ext_data.age_3539_f, age_ext_data.age_4044_f,
            age_ext_data.age_4549_f, age_ext_data.age_5054_f, age_ext_data.age_5559_f,
            age_ext_data.age_6064_f, age_ext_data.age_6569_f, age_ext_data.age_7074_f,
            age_ext_data.age_7579_f, age_ext_data.age_8084_f, age_ext_data.age_85p_f
        ]

        age_na_females = [
            age_ext_natave.age_04_f, age_ext_natave.age_59_f, age_ext_natave.age_1014_f,
            age_ext_natave.age_1519_f, age_ext_natave.age_2024_f, age_ext_natave.age_2529_f,
            age_ext_natave.age_3034_f, age_ext_natave.age_3539_f, age_ext_natave.age_4044_f,
            age_ext_natave.age_4549_f, age_ext_natave.age_5054_f, age_ext_natave.age_5559_f,
            age_ext_natave.age_6064_f, age_ext_natave.age_6569_f, age_ext_natave.age_7074_f,
            age_ext_natave.age_7579_f, age_ext_natave.age_8084_f, age_ext_natave.age_85p_f
        ]

        pop = t1_data.pop
        pop_m = sum(age_males)
        pop_f = sum(age_females)

        npop_m = sum(age_na_males)
        npop_f = sum(age_na_females)

        age_data = [
            t1_data.age_04, t1_data.age_59, t1_data.age_1014,
            t1_data.age_1519, t1_data.age_2024, t1_data.age_2529,
            t1_data.age_3034, t1_data.age_3539, t1_data.age_4044,
            t1_data.age_4549, t1_data.age_5054, t1_data.age_5559,
            t1_data.age_6064, t1_data.age_6569, t1_data.age_7074,
            t1_data.age_7579, t1_data.age_8084, t1_data.age_85p
        ]

        age_labels = ['0 - 4', "5 - 9", "10 - 14", "15 - 19", "20 - 24", "25 - 29",
                      "30 - 34", "35 - 39", "40 - 44", "45 - 49", "50 - 54", "55 - 59",
                      "60 - 64", "65 - 69", "70 - 74", "75 - 79", "80 - 84", "85+"
                      ]

        age_profile_males = []
        age_natave_males = []
        age_profile_females = []
        age_natave_females = []
        for i in range(len(age_labels)):
            age_profile_males.append({'label': age_labels[i], 'value': round((age_males[i] / pop_m) * 100, 2)})
            age_natave_males.append({'label': age_labels[i], 'value': round((age_na_males[i] / npop_m) * 100, 2)})
            age_profile_females.append({'label': age_labels[i], 'value': round((age_females[i] / pop_f) * 100, 2)})
            age_natave_females.append({'label': age_labels[i], 'value': round((age_na_females[i] / npop_f) * 100, 2)})


        context['age_males'] = age_profile_males
        context['age_na_males'] = age_natave_males
        context['age_females'] = age_profile_females
        context['age_na_females'] = age_natave_females

        auc_h, auc_l = get_age_risk(age_profile_males, age_profile_females, age_natave_males, age_natave_females)

        if auc_h > 1941:
            context['auc'] = 'High Risk'
        elif auc_l > 884:
            context['auc'] = 'Low Risk'
        else:
            context['auc'] = 'Normal'

        age_scaler = [2.5, 7.5, 12.5, 17.5, 22.5, 27.5, 32.5, 37.5, 42.5,
                      47.5, 52.5, 57.5, 62.5, 67.5, 72.5, 77.5, 82.5, 90]
        w_age = 0
        for i in range(len(age_labels)):
            w_age += age_data[i] * age_scaler[i]

        age_stats = {'population': pop,
                     'average': round(w_age/pop, 2)}

        context['age_stats'] = age_stats

        t4_data = Families.objects.filter(uid=ref_id, year=2016)[0]
        t4_natave = Families.objects.filter(zoom='country', year=2016)[0]

        family_status = [t4_data.adult, t4_data.pre_fam, t4_data.pre_s,
                      t4_data.early_s, t4_data.pre_adol, t4_data.adol,
                      t4_data.empty_nest, t4_data.retired
                      ]

        family_natave = [t4_natave.adult, t4_natave.pre_fam, t4_natave.pre_s,
                      t4_natave.early_s, t4_natave.pre_adol, t4_natave.adol,
                      t4_natave.empty_nest, t4_natave.retired]

        family_labels = ['Adult', 'Pre-Family', 'Pre-School', 'Early School',
                      'Pre-Adoldolescence', 'Adolescence', 'Empty Nest', 'Retired']

        fam_profile = []
        fam_natave = []
        for i in range(len(family_status)):
            fam_profile.append({'label': family_labels[i], 'value': family_status[i]})
            fam_natave.append({'label': family_labels[i], 'value': family_natave[i]})

        context['fam_profile'] = fam_profile
        context['fam_natave'] = fam_natave

        enest_natave = t4_natave.empty_nest/t4_natave.fam_total
        ret_natave = t4_natave.retired / t4_natave.fam_total
        enest_ed = t4_data.empty_nest / t4_data.fam_total
        ret_ed = t4_data.empty_nest / t4_data.fam_total

        enest_dif = enest_ed - enest_natave
        ret_dif = ret_ed - ret_natave

        if enest_dif > 0.04164 or ret_dif > 0.044876:
            context['fam'] = 'High Risk'
        elif enest_dif < -0.01837 or ret_dif < -0.025078:
            context['fam'] = 'Low Risk'
        else:
            context['fam'] = 'Normal'

        t14_data = Industries.objects.filter(uid=ref_id, year=2016)[0]
        t14_natave = Industries.objects.filter(zoom='country', year=2016)[0]

        industry_data = [t14_data.ag_for_fish, t14_data.build_construct,
                         t14_data.manufac, t14_data.comm_trade,
                         t14_data.trans_coms, t14_data.pub_admin,
                         t14_data.prof_ser, t14_data.ind_other]
        industry_natave = [t14_natave.ag_for_fish, t14_natave.build_construct,
                         t14_natave.manufac, t14_natave.comm_trade,
                         t14_natave.trans_coms, t14_natave.pub_admin,
                         t14_natave.prof_ser, t14_natave.ind_other]
        industry_labels = ['Agriculture, Forestry and Fishing',
                           'Building and Construction', 'Manufacturing',
                           'Commerce and Trade',
                           'Transport and Communications',
                           'Public Administration',
                           'Professional Services', 'Other']

        industry_profile = []
        ind_natave =[]
        for i in range(len(industry_data)):
            industry_profile.append({'label': industry_labels[i], 'value': industry_data[i]})
            ind_natave.append({'label': industry_labels[i], 'value': industry_natave[i]})

        context['ind_profile'] = industry_profile
        context['ind_natave'] = ind_natave

        ind_data = {}
        for i in range(len(industry_data)):
            ind_data[industry_labels[i]] = industry_data[i] / t14_data.ind_total

        ind_conc_lab = max(ind_data.items(), key=operator.itemgetter(1))[0]

        ind_conc = ind_data[ind_conc_lab]

        if ind_conc > 0.32:
            if ind_conc_lab == 'Other':
                context['ind'] = 'Moderate Risk'
            else:
                context['ind'] = 'High Risk'
        elif ind_conc < 0.215:
            context['ind'] = 'Low Risk'
        else:
            context['ind'] = 'Normal'

        input_data = {}
        input_data['address'] = search_address
        input_data['type'] = get_common('type', tl_ed, county)
        input_data['condition'] = get_common('condition', tl_ed, county)
        input_data['bed'] = get_common('beds', tl_ed, county)
        input_data['bath'] = get_common('baths', tl_ed, county)

        input_data['apt'] = regex_apt(input_data['address'])
        input_data['house_name'] = regex_house(input_data['address'])

        input_data['suffix'] = regex_suffix(input_data['address'])

        start = date(2010, 1, 1)
        today = date.today()
        print(input_data)
        input_data['date'] = (today - start).days
        input_data['type'] = desc_map(input_data['type'])
        input_data['condition'] = cond_map(input_data['condition'])
        input_data['apt'] = apt_map(input_data['apt'])
        input_data['house_name'] = name_map(input_data['house_name'])
        input_data['suffix'] = suffix_map(input_data['suffix'])

        input_data['ed'] = tl_ed
        model_choice, input_data['county'] = find_model(county, input_data['ed'])
        z = ed_map(input_data['ed'])
        print(model_choice, z)

        if z == 'NEDTMP':
            context['pred_data'] = [0]
            context['ti_price'] = 0
            context['moe'] = 0
            context['pr'] = 'Not Applicable'
        else:
            input_data['ed'] = z
            input_data['county'] = county_map(input_data['county'])
            pred = {}

            clf = None
            pred['price'], clf = full_pred(input_data, location, model_choice, clf)

            time_increase = (date(2010, 1, 1) - date(1970, 1, 1)).days
            millisec = 86400000

            list_with_predictions = [pred['price']]
            times_to_transform = [input_data['date']]

            for i in range(22):
                input_data['date'] = (today - start).days - i * 120
                list_with_predictions.append(full_pred(input_data, location, model_choice, clf)[0])
                times_to_transform.append((today - start).days - i * 120)

            context['moe'] = get_moe(model_choice)

            list_with_times = [((x + time_increase) * millisec) for x in times_to_transform]
            # List to be plotted
            list_to_plot = list(map(lambda x, y: [int(x), int(y)], list_with_times,
                     list_with_predictions))

            context['pred_data'] = list_to_plot

            context['ti_price'] = ti_pred(input_data, location, model_choice)

            if pred['price'] > context['ti_price'] + float(context['moe']):
                context['pr'] = 'Overvalued'
            elif pred['price'] < context['ti_price'] - float(context['moe']):
                context['pr'] = 'Undervalued'
            else:
                context['pr'] = 'Within Margin of Error'

        t6_data = Housing.objects.filter(uid=ref_id, year=2016)[0]
        t6_natave = Housing.objects.filter(zoom='country', year=2016)[0]

        hh_occupancy_data = [t6_data.occupied, t6_data.temp_unoc, t6_data.unoc_hol, t6_data.unoccupied]
        hh_occupancy_na = [t6_natave.occupied, t6_natave.temp_unoc, t6_natave.unoc_hol, t6_natave.unoccupied]

        hh_occupancy_labels =['Occupied', 'Temporarily Vacant', 'Unoccupied Holiday Homes', 'Unoccupied']

        hh_occupancy_profile = []
        hh_occupancy_natave = []
        for i in range(len(hh_occupancy_data)):
            hh_occupancy_profile.append({'label': hh_occupancy_labels[i], 'value': hh_occupancy_data[i]})
            hh_occupancy_natave.append({'label': hh_occupancy_labels[i], 'value': hh_occupancy_na[i]})



        hh_mortgage_data = [t6_data.oo_wm, t6_data.oo_wom, t6_data.rent_pl,
                             t6_data.rent_la, t6_data.rent_vol, t6_data.rent_free,
                             t6_data.occu_ns]

        hh_mortgage_na = [t6_natave.oo_wm, t6_natave.oo_wom, t6_natave.rent_pl,
                             t6_natave.rent_la, t6_natave.rent_vol, t6_natave.rent_free,
                             t6_natave.occu_ns]

        hh_mortgage_labels = ['Owner Occupier with Mortgage', 'Owner Occupier without Mortgage',
                               'Rented from Private Landlord', 'Rented from Local Authority',
                               'Rented from Voluntary Body', 'Rented Free of Rent', 'Not Stated']

        hh_mortgage_profile = []
        hh_mortgage_natave = []
        for i in range(len(hh_mortgage_data)):
            hh_mortgage_profile.append({'label': hh_mortgage_labels[i], 'value': hh_mortgage_data[i]})
            hh_mortgage_natave.append({'label': hh_mortgage_labels[i], 'value': hh_mortgage_na[i]})

        t8_data = PrincStat.objects.filter(uid=ref_id, year=2016)[0]
        t8_natave = PrincStat.objects.filter(zoom='country', year=2016)[0]

        prince_stat_data = [t8_data.work, t8_data.lffj, t8_data.unemployed,
                            t8_data.student, t8_data.home_fam, t8_data.retired,
                            t8_data.sick_dis, t8_data.stat_other]

        prince_stat_na = [t8_natave.work, t8_natave.lffj, t8_natave.unemployed,
                            t8_natave.student, t8_natave.home_fam, t8_natave.retired,
                            t8_natave.sick_dis, t8_natave.stat_other]

        prince_stat_labels = ['Working', 'Looking for First Job', 'Unemployed',
                              'Student', 'Looking After Home/Family', 'Retired',
                              'Sick or Disabled', 'Other']

        prince_stat_profile = []
        prince_stat_natave = []
        for i in range(len(prince_stat_data)):
            prince_stat_profile.append({'label': prince_stat_labels[i], 'value': prince_stat_data[i]})
            prince_stat_natave.append({'label': prince_stat_labels[i], 'value': prince_stat_na[i]})

        t9_data = SocClass.objects.filter(uid=ref_id, year=2016)[0]
        t9_natave = SocClass.objects.filter(zoom='country', year=2016)[0]

        socclass_data = [t9_data.prof_worker, t9_data.manage_tech,
                         t9_data.non_manual, t9_data.skilled_manual,
                         t9_data.semi_skilled, t9_data.unskilled,
                         t9_data.class_other]

        socclass_na = [t9_natave.prof_worker, t9_natave.manage_tech,
                         t9_natave.non_manual, t9_natave.skilled_manual,
                         t9_natave.semi_skilled, t9_natave.unskilled,
                         t9_natave.class_other]

        socclass_labels = ['Professional Worker', 'Managerial and Technical',
                           'Non-Manual', 'Skilled Manual',
                           'Semi-Skilled', 'Unskilled', 'All Others']

        socclass_profile = []
        socclass_natave = []
        for i in range(len(socclass_data)):
            socclass_profile.append({'label': socclass_labels[i], 'value': socclass_data[i]})
            socclass_natave.append({'label': socclass_labels[i], 'value': socclass_na[i]})

        context['job_profile'] = prince_stat_profile
        context['job_natave'] = prince_stat_natave
        context['skills_profile'] = socclass_profile
        context['skills_natave'] = socclass_natave
        context['occu_profile'] = hh_occupancy_profile
        context['occu_natave'] = hh_occupancy_natave
        context['mort_profile'] = hh_mortgage_profile
        context['mort_natave'] = hh_mortgage_natave

        skills_data = {}
        for i in range(len(socclass_data)):
            skills_data[socclass_labels[i]] = socclass_data[i] / t9_data.class_total

        skills_conc_lab = max(skills_data.items(), key=operator.itemgetter(1))[0]

        skills_conc = skills_data[skills_conc_lab]

        if skills_conc > 0.38:
            if ind_conc_lab == 'Other':
                context['skills'] = 'Moderate Risk'
            else:
                context['skills'] = 'High Risk'
        elif skills_conc < 0.23:
            context['skills'] = 'Low Risk'
        else:
            context['skills'] = 'Normal'

        work_conc = prince_stat_data[0] / t8_data.stat_total

        if work_conc > 0.60353:
            context['job'] = 'Low Risk'
        elif work_conc < 0.44026:
            context['job'] = 'High Risk'
        else:
            context['job'] = 'Normal'

        occu_conc = hh_occupancy_data[0] / sum(hh_occupancy_data)

        if occu_conc > 0.92662:
            context['occu'] = 'Low Risk'
        elif occu_conc < 0.684301:
            context['occu'] = 'High Risk'
        else:
            context['occu'] = 'Normal'

        # If proportion of residents with mortgages is high
        # (correlated defaults)
        mort_conc = hh_mortgage_data[0] / sum(hh_mortgage_data)

        if mort_conc > 0.4379:
            context['mort'] = 'High Risk'
        elif mort_conc < 0.194:
            context['mort'] = 'Low Risk'
        else:
            context['mort'] = 'Normal'

        # Generate data to pass to map
        context['age_cp_data'] = age_cp_data
        context['ed_geojson'] = ed_geojson

    return render(request, 'riskdb/index.html', context)


def get_common(attr, edist, county):
    # Returns the most common attribute for a given county
    df = pd.read_csv(settings.BASE_DIR + '/predictive_model/model_data_ed.csv')

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


def get_age_risk(apm, apf, anm, anf):
    auc_l = 0
    auc_h = 0

    for i in range(len(anm)):
        l = anm[i]['label']

        if len(l) == 5:
            ma = np.mean([int(l[0]), int(l[-1])]) + 0.5
        elif len(l) == 3:
            ma = 90
        elif len(l) == 2:
            ma = 0
        else:
            ma = 0


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


def desc_map(string):
    d = {
        'Semi-Detached House': 0,
        'Detached House': 1,
        'Other': 2,
        'Terraced House': 3
    }

    try:
        a = d[string]
    except:
        a = 2

    return a


def ed_map(string):
    file_location = settings.BASE_DIR + '/predictive_model/mappings/eds_location_split.csv'
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

    file_location = settings.BASE_DIR + '/predictive_model/mappings/suffix_mapping.csv'
    reader = csv.reader(open(file_location, 'r'))
    d = {}
    for row in reader:
        i, k, v = row
        d[k] = v

    return d[string]


def ti_pred(data, location, model_choice):

    if model_choice == 'Dublin':
        model_location = settings.BASE_DIR + '/predictive_model/dublin_model_time_independent.pkl'
    elif model_choice == 'Urban':
        model_location = settings.BASE_DIR + '/predictive_model/urban_model_time_independent.pkl'
    elif model_choice == 'County':
        model_location = settings.BASE_DIR + '/predictive_model/rural_model_time_independent.pkl'
    else:
        model_location = None

    clf = joblib.load(model_location)

    X = np.asarray([data['county'], data['type'], data['bed'],
                    data['bath'], location['lat'], location['lng'],
                    data['condition'], data['apt'], data['house_name'],
                    data['suffix'], data['ed']]).reshape(1, -1)

    prediction = clf.predict(X)

    return prediction


def full_pred(data, location, model_choice, clf):
    if clf == None:
        if model_choice == 'Dublin':
            model_location = settings.BASE_DIR + '/predictive_model/dublin_model.pkl'
        elif model_choice == 'Urban':
            model_location = settings.BASE_DIR + '/predictive_model/urban_model.pkl'
        elif model_choice == 'County':
            model_location = settings.BASE_DIR + '/predictive_model/rural_model.pkl'
        else:
            model_location = None

        clf = joblib.load(model_location)

    X = np.asarray([data['county'], data['type'], data['bed'],
                    data['bath'], location['lat'], location['lng'],
                    data['condition'], data['apt'], data['house_name'],
                    data['suffix'], data['ed'], data['date']]).reshape(1, -1)

    prediction = clf.predict(X)

    return prediction, clf


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


def county_map(string):
    if string == 'Carlow County' or string == 'Carlow City':
        sstring = 'Carlow'
    else:
        sstring = string

    county_mapping = {"Carlow":0, "Cavan":1, "Clare":2, "Cork City":3, "Cork County":3, "Donegal":4, "Dublin":5,
                  "Galway City":6, "Galway County":6, "Kerry":7, "Kildare":8, "Kilkenny":9, "Laois":10, "Leitrim":11,
                  "Limerick City":12, "Limerick County":12, "Longford":13, "Louth":14, "Mayo":15, "Meath":16,
                  "Monaghan":17, "Offaly":18, "Roscommon":19, "Sligo":20, "Tipperary":21,
                  "Waterford City":22,"Waterford County":22, "Westmeath":23, "Wexford":24, "Wicklow":25}

    return county_mapping[sstring]


def get_moe(string):
    file_location = settings.BASE_DIR + '/predictive_model/models/model_results.csv'
    reader = csv.reader(open(file_location, 'r'))
    d = {}
    for row in reader:
        model, moe, _ = row
        d[model] = moe
    if string.lower() == 'county':
        return d['rural']
    else:
        return d[string.lower()]

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
        file_location = settings.BASE_DIR + '/predictive_model/mappings/eds_location_split.csv'
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