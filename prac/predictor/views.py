from django.shortcuts import render
from django.http import HttpResponse
import googlemaps
from sklearn.externals import joblib
from django.conf import settings
import numpy as np
import json
import matplotlib.path as mplPath
import re
import csv
from datetime import date
import calendar


def geolocate(address_string, county):
    gmaps = googlemaps.Client(key='AIzaSyBFwN-7_erzpXeWWFe3DwMqSPKGoCjj1Hg')

    address = address_string + ' ' + county + ' Ireland'

    geocode_result = gmaps.geocode(address)

    # If a result is returned
    if len(geocode_result) > 0:
        # Set the location as the result
        location = geocode_result[0]['geometry']['location']

        status = 1
    else:
        location = {'lat': 0, 'lng': 0}
        status = 2

    # Check if location is within east/west boundary of Ireland
    if status is 1:
        if location['lng'] > -10.738539 and location['lng'] < -5.930445:
            pass
        else:
            status = 2

        if location['lat'] > 51.387652 and location['lat'] < 55.445918:
            pass
        else:
            status = 2

    return location, status


def check_polygon(polygon, point):

    path = mplPath.Path(polygon)

    inside = path.contains_point(point)

    return inside


def find_ed(data, latitude, longitude):
    point = ([longitude, latitude])

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
            return feature['properties']['NAME_TAG']

    return None


def word_isolation(string):
    keep_words = ['road', 'park', 'avenue', 'court', 'rd', 'street', 'drive',
                  'st', 'grove', 'manor', 'close', 'green', 'view', 'hill',
                  'house', 'the', 'wood', 'terrace', 'heights', 'hall',
                  'mount', 'grange', 'lodge', 'lane', 'main', 'place', 'lawn',
                  'ave', 'square', 'dr', 'estate', 'woodlands', 'harbour',
                  'quay', 'bay', 'apt', 'sq', 'apartment']

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


def full_pred(data, location, model_choice, clf):
    if clf is None:
        if model_choice == 'Dublin':
            model_location = settings.BASE_DIR + \
                             '/predictive_model/models/dublin_model_full.pkl'
        elif model_choice == 'Urban':
            model_location = settings.BASE_DIR + \
                             '/predictive_model/models/urban_model_full.pkl'
        elif model_choice == 'Rural':
            model_location = settings.BASE_DIR + \
                             '/predictive_model/models/rural_model_full.pkl'
        else:
            model_location = None

        clf = joblib.load(model_location)

    X = np.asarray([data['county'], data['type'], data['bed'],
                    data['bath'], location['lat'], location['lng'],
                    data['condition'], data['apt'], data['house_name'],
                    data['suffix'], data['ed'], data['date']]).reshape(1, -1)

    try:
        prediction = clf.predict(X)
        status = 0
    except:
        prediction, status, _ = partial_pred(data, None)

    return prediction, status, clf


def partial_pred(data, clf):
    # Basically the same thing, but uses fewer features and NAs the rest
    if clf is None:
        if data['model_choice'] == 'Dublin':
            model_location = settings.BASE_DIR + \
                         '/predictive_model/models/dublin_model_partial.pkl'
        elif data['model_choice'] == 'Urban':
            model_location = settings.BASE_DIR + \
                         '/predictive_model/models/urban_model_partial.pkl'
        elif data['model_choice'] == 'Rural':
            model_location = settings.BASE_DIR + \
                         '/predictive_model/models/rural_model_partial.pkl'
        else:
            model_location = None

        clf = joblib.load(model_location)

    X = np.asarray([data['county'], data['type'], data['bed'],
                    data['bath'], data['condition'], data['apt'],
                    data['house_name'], data['suffix'],
                    data['date']]).reshape(1, -1)

    try:
        prediction = clf.predict(X)
        status = 1
    except:
        prediction = 0
        status = 2

    return prediction, status, clf


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
    county_mapping = {"Carlow": 0, "Cavan": 1, "Clare": 2, "Cork City": 3,
                      "Cork County": 3, "Donegal": 4, "Dublin": 5,
                      "Galway City": 6, "Galway County": 6, "Kerry": 7,
                      "Kildare": 8, "Kilkenny": 9, "Laois": 10, "Leitrim": 11,
                      "Limerick City": 12, "Limerick County": 12,
                      "Longford": 13, "Louth": 14, "Mayo": 15, "Meath": 16,
                      "Monaghan": 17, "Offaly": 18, "Roscommon": 19,
                      "Sligo": 20, "Tipperary": 21, "Waterford City": 22,
                      "Waterford County": 22, "Westmeath": 23,
                      "Wexford": 24, "Wicklow": 25}

    return county_mapping[string]


def desc_map(string):
    file_location = settings.BASE_DIR + \
                    '/predictive_model/mappings/desc_mapping.csv'
    reader = csv.reader(open(file_location, 'r'))
    d = {}
    for row in reader:
        i, k, v = row
        d[k] = v

    return d[string]


def ed_map(string):
    file_location = settings.BASE_DIR + \
                    '/predictive_model/mappings/eds_location_split.csv'
    reader = csv.reader(open(file_location, 'r'))
    d = {}
    for row in reader:
        _, i, k, v, _ = row
        d[k] = v

    return d[string]


def cond_map(string):
    cond = {"Second-Hand House / Apartment": 0, "New House / Apartment": 1}
    return cond[string]


def apt_map(string):
    apt = {"No": 0, "Yes": 1}
    return apt[string]


def name_map(string):
    name = {"No": 0, "Yes": 1}
    return name[string]


def suffix_map(string):
    if string is None:
        string = "None"

    file_location = settings.BASE_DIR + \
        '/predictive_model/mappings/suffix_mapping.csv'
    reader = csv.reader(open(file_location, 'r'))
    d = {}
    for row in reader:
        i, k, v = row
        d[k] = v

    return d[string]


def find_model(string):
    file_location = settings.BASE_DIR + \
                    '/predictive_model/mappings/eds_location_split.csv'
    reader = csv.reader(open(file_location, 'r'))
    d = {}
    for row in reader:
        x, i, k, y, v = row
        d[k] = v

    return d[string]


def plotting_data(list_with_times, list_with_preds):
    data = list(map(lambda x, y: [int(x), int(y)], list_with_times,
                    list_with_preds))
    return data


def index(request):
    context = {}

    return render(request, 'predictor/index.html', context)


def predict(request):
    input_data = {}

    pred = {'status': 0, 'price': 0}

    input_data['address'] = request.POST['address']
    input_data['county'] = request.POST['county']
    input_data['type'] = request.POST['dop']
    input_data['condition'] = request.POST['condition']
    if (request.POST['beds']) == '5+':
        input_data['bed'] = 5
    else:
        input_data['bed'] = int(request.POST['beds'])
    if (request.POST['baths']) == '5+':
        input_data['bath'] = 5
    else:
        input_data['bath'] = int(request.POST['baths'])

    input_data['apt'] = regex_apt(input_data['address'])
    input_data['house_name'] = regex_house(input_data['address'])
    input_data['suffix'] = regex_suffix(input_data['address'])

    # Date feature
    start = date(2010, 1, 1)
    today = date.today()
    input_data['date'] = (today - start).days

    # Transform time variables for plotting
    time_increase = (date(2010, 1, 1) - date(1970, 1, 1)).days
    millisec = 86400000

    # Lat, Long generation
    loc, stat = geolocate(input_data['address'], input_data['county'])

    # Feature mapping - Mapping categorical data to integer scale
    input_data['model_choice'] = model_selection(input_data['county'])
    input_data['county'] = county_map(input_data['county'])
    input_data['type'] = desc_map(input_data['type'])
    input_data['condition'] = cond_map(input_data['condition'])
    input_data['apt'] = apt_map(input_data['apt'])
    input_data['house_name'] = name_map(input_data['house_name'])
    input_data['suffix'] = suffix_map(input_data['suffix'])

    clf = None
    if stat == 2:
        pred['price'], pred['status'], clf = partial_pred(input_data, clf)
        model_choice = input_data['model_choice'] + 'p'

        list_with_predictions = [pred['price']]
        times_to_transform = [input_data['date']]

        for i in range(22):
            input_data['date'] = (today - start).days - i * 120
            list_with_predictions.append(partial_pred(input_data, clf)[0])
            times_to_transform.append((today - start).days - i * 120)

        pred['moe'] = get_moe(model_choice)

    else:
        eds_location = settings.BASE_DIR + '/predictive_model/eds.geojson'
        with open(eds_location) as f:
            file = json.load(f)
        input_data['ed'] = find_ed(file, loc['lat'], loc['lng'])
        model_choice = input_data['model_choice']
        input_data['ed'] = ed_map(input_data['ed'])

        pred['price'], pred['status'], clf = full_pred(input_data, loc,
                                                       model_choice, clf)
        list_with_predictions = [pred['price']]
        times_to_transform = [input_data['date']]

        for i in range(22):
            input_data['date'] = (today - start).days - i * 120
            list_with_predictions.append(full_pred(input_data, loc,
                                                   model_choice, clf)[0])
            times_to_transform.append((today - start).days - i * 120)

        pred['moe'] = get_moe(model_choice)

    list_with_times = [((x + time_increase) * millisec) for x in
                       times_to_transform]
    list_to_plot = plotting_data(list_with_times, list_with_predictions)

    pred['ti_data'] = int(ti_pred(input_data, loc, model_choice))

    pred['price'] = int(pred['price'])
    pred['date'] = str(today.day) + '-' + \
        str(calendar.month_name[today.month]) + '-' + \
        str(today.year)

    pred['plotdata'] = list_to_plot

    return HttpResponse(json.dumps(pred))


def ti_pred(data, location, model_choice):
    if model_choice == 'Dublin':
        model_location = settings.BASE_DIR + \
                         '/predictive_model/models/dublin_model_ti.pkl'
    elif model_choice == 'Dublinp':
        model_location = settings.BASE_DIR + \
                         '/predictive_model/models/dublin_model_ti_part.pkl'
    elif model_choice == 'Urban':
        model_location = settings.BASE_DIR + \
                         '/predictive_model/models/urban_model_ti.pkl'
    elif model_choice == 'Urbanp':
        model_location = settings.BASE_DIR + \
                         '/predictive_model/models/urban_model_ti_part.pkl'
    elif model_choice == 'Rural':
        model_location = settings.BASE_DIR + \
                         '/predictive_model/models/rural_model_ti.pkl'
    elif model_choice == 'Ruralp':
        model_location = settings.BASE_DIR + \
                         '/predictive_model/models/rural_model_ti_part.pkl'
    else:
        model_location = None

    clf = joblib.load(model_location)

    if model_choice[-1] == 'p':
        X = np.asarray([data['county'], data['type'], data['bed'],
                        data['bath'], data['condition'], data['apt'],
                        data['house_name'], data['suffix']]).reshape(1, -1)
    else:
        X = np.asarray([data['county'], data['type'], data['bed'],
                        data['bath'], location['lat'], location['lng'],
                        data['condition'], data['apt'], data['house_name'],
                        data['suffix'], data['ed']]).reshape(1, -1)

    prediction = clf.predict(X)

    return prediction


def get_moe(string):
    file_location = settings.BASE_DIR + \
                    '/predictive_model/models/model_results.csv'
    reader = csv.reader(open(file_location, 'r'))
    d = {}
    for row in reader:
        model, moe, _ = row
        d[model] = moe

    return d[string.lower()]


def model_selection(string):
    urban = ['Cork City', 'Waterford City', 'Limerick City', 'Waterford City']
    if string in urban:
        return 'Urban'
    elif string == 'Dublin':
        return 'Dublin'
    else:
        return 'Rural'
