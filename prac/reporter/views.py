from django.shortcuts import render, HttpResponse
from prac.models import Sale, SexAgeMarriage, CSORef, PoBNat, Families, \
    PrivHH, Housing, PrincStat, SocClass, Education, Commuting, Occupation,\
    Industries, AgeExt
from django.db.models import Avg, Max, Min, Count

import math
import calendar
import datetime
import pandas as pd
import numpy as np
import json
from django.conf import settings

# Create your views here.
def index(request):

    cookies = request.COOKIES

    date_max = int(cookies.get('max_date'))
    date_min = int(cookies.get('min_date'))
    price_max = float(cookies.get('max_price'))
    price_min = float(cookies.get('min_price'))
    left = float(cookies.get('left'))
    right = float(cookies.get('right'))
    top = float(cookies.get('top'))
    bottom = float(cookies.get('bottom'))
    calcArea = cookies.get('areaMain')
    area = cookies.get('areaSecond')
    radius = float(cookies.get('radius'))
    bad_data = cookies.get('bad_data_inc')

    with open(settings.BASE_DIR + '/homepage' + settings.STATIC_URL + 'RRP_timestamp.txt', 'r') as file:
        lu = file.read()

    datalist = Sale.objects.aggregate(Max('price'))
    maxp = datalist['price__max']

    context = {'last_update': lu, 'maxp': maxp}

    if (date_max == 1491001200000 and date_min == 1262304000000 and price_max == 26500000 and price_min == 0):
        use_cached_natave = True
        context['cache'] = 'true'
    else:
        use_cached_natave = False
        context['cache'] = 'false'

    dh = datetime.datetime.fromtimestamp(date_max / 1000)
    dl = datetime.datetime.fromtimestamp(date_min / 1000)

    ed_list = []
    points = []

    if calcArea == 'map':
        data = Sale.objects.filter(quality='good', nfma='No').filter(
            latitude__gte=bottom, latitude__lte=top, longitude__gte=left,
            longitude__lte=right, price__lte=price_max, price__gte=price_min,
            sale_date__gte=dl, sale_date__lte=dh)

        if len(data) == 0:
            context['enoughdata'] = 'false'
            context['dom_ed'] = 'Not Applicable'
            context['n_ed'] = 0

            return render(request, 'reporter/index.html', context)

        for sale in data:
            points.append([float(sale.latitude), float(sale.longitude)])

        sales_data, hist_data, volume_data, new_data, avg_size = retrieve_stats(data)

        ag_data = data.aggregate(Avg('price'), Min('price'), Max('price'), Count('price'))

        count = ag_data['price__count']
        avg_price = ag_data['price__avg']
        min_price = ag_data['price__min']
        max_price = ag_data['price__max']

        values = data.values_list('price', flat=True).order_by('price')

        if count % 2 == 1:
            med = values[int(round(count / 2 - 0.5))]
        else:
            med = sum(values[count / 2 - 0.5: count / 2 + 0.5]) / 2

        ed_data = Sale.objects.filter(quality='good', nfma='No').filter(
            latitude__gte=bottom, latitude__lte=top, longitude__gte=left,
            longitude__lte=right)

        if len(ed_data) == 0:
            context['dom_ed'] = 'Not Applicable'
            context['n_ed'] = 0
        else:
            ed_count = {}
            for sale in ed_data:
                if sale.ed in ed_count.keys():
                    ed_count[sale.ed] += 1
                else:
                    ed_count[sale.ed] = 1

            eds_to_use = []

            for k, v in ed_count.items():
                if v > max(ed_count.values()) / 3:
                    eds_to_use.append([k, v])

            for ed in eds_to_use:
                try:
                    ref = CSORef.objects.filter(desc=ed[0])[0].uid
                    ed_list.append([ref, ed[1]])
                except:
                    continue

            context['dom_ed'] = max(ed_count, key=ed_count.get)
            context['n_ed'] = len(ed_count)

        if len(ed_data) == 0 or len(ed_list) == 0:
            context['enoughdata'] = 'false'
            context['dom_ed'] = 'Not Applicable'
            context['n_ed'] = 0

            return render(request, 'reporter/index.html', context)
    elif calcArea == 'radius':
        c_lat = (top - bottom)/2 + bottom
        c_lng = (left - right)/2 + right

        right = latlng(c_lat, c_lng, radius, 'E')[1]
        left = latlng(c_lat, c_lng, radius, 'W')[1]
        top = latlng(c_lat, c_lng, radius, 'N')[0]
        bottom = latlng(c_lat, c_lng, radius, 'S')[0]

        data = Sale.objects.filter(quality='good', nfma='No').filter(
            latitude__gte=bottom, latitude__lte=top, longitude__gte=left,
            longitude__lte=right, price__lte=price_max, price__gte=price_min,
            sale_date__gte=dl, sale_date__lte=dh)

        if len(data) == 0:
            context['enoughdata'] = 'false'
            context['dom_ed'] = 'Not Applicable'
            context['n_ed'] = 0

            return render(request, 'reporter/index.html', context)

        sale_list = []
        size_list = []
        hist_data = []
        price_list = []

        scatter_data = {'date': [], 'price': []}
        new_data = {'date': [], 'new': [], 'used': []}

        ed_count = {}

        for sale in data:
            lat = float(sale.latitude)
            lng = float(sale.longitude)

            if distance(c_lat, c_lng, lat, lng) <= radius:
                raw_time = calendar.timegm(sale.sale_date.timetuple())
                points.append([lat, lng])
                sale_list.append(raw_time)
                price_list.append(float(sale.price))
                scatter_data['date'].append(sale.sale_date)
                scatter_data['price'].append(float(sale.price))
                hist_data.append(float(sale.price))

                if sale.PSD == 'greater than or equal to 38 sq metres and less than 125 sq metres':
                    size_list.append(81.5)
                elif sale.PSD == 'greater than 125 sq metres':
                    size_list.append(125)
                elif sale.PSD == 'less than 38 sq metres':
                    size_list.append(38)

                if sale.DoP == 'Second-Hand Dwelling house /Apartment':
                    new_data['date'].append(sale.sale_date)
                    new_data['new'].append(0)
                    new_data['used'].append(float(sale.price))
                else:
                    new_data['date'].append(sale.sale_date)
                    new_data['new'].append(float(sale.price))
                    new_data['used'].append(0)

                if sale.ed in ed_count.keys():
                    ed_count[sale.ed] += 1
                else:
                    ed_count[sale.ed] = 1

        if len(price_list) == 0:
            context['enoughdata'] = 'false'
            context['dom_ed'] = 'Not Applicable'
            context['n_ed'] = 0

            return render(request, 'reporter/index.html', context)

        avg_size = round(np.mean(size_list), 1)
        avg_price = round(np.mean(price_list), 0)
        min_price = round(min(price_list), 0)
        max_price = round(max(price_list), 0)
        count = len(price_list)

        med = np.median(price_list)

        df = pd.DataFrame(scatter_data, columns=['price'],
                          index=scatter_data['date'])
        new_df = pd.DataFrame(new_data, columns=['new', 'used'],index=new_data['date'])
        df.index.names = ['date']
        new_df.index.names = ['date']

        df = df.set_index(pd.DatetimeIndex(df.index))
        new_df = new_df.set_index(pd.DatetimeIndex(new_df.index))
        sdf = df.resample('W').mean().dropna(axis=0, how='any')
        sdf = sdf[sdf['price'] != 0]
        vdf = df.resample('W').count().dropna(axis=0, how='any')
        vdf = vdf[vdf['price'] != 0]
        ndf = new_df[new_df['new'] != 0]['new']
        ndf = ndf.resample('W').count().dropna(axis=0, how='any')
        udf = new_df[new_df['used'] != 0]['used']
        udf = udf.resample('W').count().dropna(axis=0, how='any')
        idf = new_df.resample('W').count().dropna(axis=0, how='any')

        sales_data = list(map(lambda x, y: [
            calendar.timegm(x.to_pydatetime().timetuple()) * 1000,
            round(float(y), 2)], sdf.index.tolist(), sdf.values))
        volume_data = list(map(lambda x, y: [
            calendar.timegm(x.to_pydatetime().timetuple()) * 1000,
            round(float(y), 2)], vdf.index.tolist(), vdf.values))
        new_data = list(map(lambda x, y, z: [calendar.timegm(x.to_pydatetime().timetuple()) * 1000, round(float(y), 2), round(float(z), 2)], idf.index.tolist(), udf.tolist(), ndf.tolist()))

        ed_data = Sale.objects.filter(quality='good', nfma='No').filter(
            latitude__gte=bottom, latitude__lte=top, longitude__gte=left,
            longitude__lte=right)

        if len(ed_data) == 0:
            context['dom_ed'] = 'Not Applicable'
            context['n_ed'] = 0
        else:
            for sale in ed_data:
                lat = float(sale.latitude)
                lng = float(sale.longitude)

                if distance(c_lat, c_lng, lat, lng) <= radius:
                    if sale.ed in ed_count.keys():
                        ed_count[sale.ed] += 1
                    else:
                        ed_count[sale.ed] = 1

            eds_to_use = []
            for k, v in ed_count.items():
                if v > max(ed_count.values()) / 3:
                    eds_to_use.append([k, v])
            for ed in eds_to_use:
                try:
                    ref = CSORef.objects.filter(desc=ed[0])[0].uid
                    ed_list.append([ref, ed[1]])
                except:
                    continue

            context['dom_ed'] = max(ed_count, key=ed_count.get)
            context['n_ed'] = len(ed_count)

        if len(ed_data) == 0 or len(ed_list) == 0:
            context['enoughdata'] = 'false'
            context['dom_ed'] = 'Not Applicable'
            context['n_ed'] = 0

            return render(request, 'reporter/index.html', context)

        compressed_hist_data = compress_list(hist_data, 25000)

        if max(compressed_hist_data.keys()) / 20 < 25000:
            compressed_hist_data = compress_list(hist_data, 20000)
            if max(compressed_hist_data.keys()) / 20 < 20000:
                compressed_hist_data = compress_list(hist_data, 15000)
                if max(compressed_hist_data.keys()) / 20 < 15000:
                    compressed_hist_data = compress_list(hist_data, 10000)

        hist_data = compressed_hist_data
    elif calcArea == 'county':
        ref_id = CSORef.objects.filter(zoom=calcArea, desc=area)[0].uid

        if bad_data == 'true':
            data = Sale.objects.filter(nfma='No', price__lte=price_max, price__gte=price_min,
                                       sale_date__gte=dl, sale_date__lte=dh, county=area)
        else:
            data = Sale.objects.filter(quality='good', nfma='No', price__lte=price_max, price__gte=price_min,
                                       sale_date__gte=dl, sale_date__lte=dh, county=area)

        if len(data) == 0:
            context['enoughdata'] = 'false'
            context['dom_ed'] = 'Not Applicable'
            context['n_ed'] = 0

            return render(request, 'reporter/index.html', context)

        for sale in data:
            points.append([float(sale.latitude), float(sale.longitude)])

        sales_data, hist_data, volume_data, new_data, avg_size = retrieve_stats(data)

        ag_data = data.aggregate(Avg('price'), Min('price'), Max('price'),
                                 Count('price'))

        count = ag_data['price__count']
        avg_price = ag_data['price__avg']
        min_price = ag_data['price__min']
        max_price = ag_data['price__max']

        values = data.values_list('price', flat=True).order_by('price')

        if count % 2 == 1:
            med = values[int(round(count / 2 - 0.5))]
        else:
            med = sum(values[count / 2 - 0.5: count / 2 + 0.5]) / 2
    elif calcArea == 'region':
        ref_id = CSORef.objects.filter(zoom=calcArea, desc=area)[0].uid

        if bad_data == 'true':
            data = Sale.objects.filter(nfma='No', price__lte=price_max, price__gte=price_min,
                                       sale_date__gte=dl, sale_date__lte=dh, region=area)
        else:
            data = Sale.objects.filter(quality='good', nfma='No', price__lte=price_max, price__gte=price_min,
                                       sale_date__gte=dl, sale_date__lte=dh, region=area)

        if len(data) == 0:
            context['enoughdata'] = 'false'
            context['dom_ed'] = 'Not Applicable'
            context['n_ed'] = 0

            return render(request, 'reporter/index.html', context)

        sales_data, hist_data, volume_data, new_data, avg_size = retrieve_stats(data)

        ag_data = data.aggregate(Avg('price'), Min('price'), Max('price'),
                                 Count('price'))

        count = ag_data['price__count']
        avg_price = ag_data['price__avg']
        min_price = ag_data['price__min']
        max_price = ag_data['price__max']

        values = data.values_list('price', flat=True).order_by('price')

        if count % 2 == 1:
            med = values[int(round(count / 2 - 0.5))]
        else:
            med = sum(values[count / 2 - 0.5: count / 2 + 0.5]) / 2
    elif calcArea == 'country':
        ref_id = CSORef.objects.filter(zoom=calcArea)[0].uid
        if bad_data == 'true':
            data = Sale.objects.filter(nfma='No', price__lte=price_max, price__gte=price_min,
                                       sale_date__gte=dl, sale_date__lte=dh)
        else:
            data = Sale.objects.filter(quality='good', nfma='No', price__lte=price_max, price__gte=price_min,
                                       sale_date__gte=dl, sale_date__lte=dh)

        if len(data) == 0:
            context['enoughdata'] = 'false'
            context['dom_ed'] = 'Not Applicable'
            context['n_ed'] = 0

            return render(request, 'reporter/index.html', context)

        sales_data, hist_data, volume_data, new_data, avg_size = retrieve_stats(data)

        ag_data = data.aggregate(Avg('price'), Min('price'), Max('price'),
                                 Count('price'))

        count = ag_data['price__count']
        avg_price = ag_data['price__avg']
        min_price = ag_data['price__min']
        max_price = ag_data['price__max']

        values = data.values_list('price', flat=True).order_by('price')

        if count % 2 == 1:
            med = values[int(round(count / 2 - 0.5))]
        else:
            med = sum(values[count / 2 - 0.5: count / 2 + 0.5]) / 2

        if not use_cached_natave:
            na_sales, na_volume_scaled, na_hist_scaled = get_na_data(True,
                 bad_data, price_max, price_min, dl, dh, volume_data, hist_data, data=data)

            context['na_sales'] = na_sales
            context['na_volume'] = na_volume_scaled
            context['na_hist'] = na_hist_scaled

    context['sales_data'] = sales_data
    context['hist_data'] = hist_data
    context['volume_data'] = volume_data
    context['new_data'] = new_data
    context['avg_size'] = avg_size

    context['med_price'] = float(med)
    context['volume'] = count
    context['max_price'] = max_price
    context['min_price'] = min_price
    context['avg_price'] = avg_price
    context['current_points'] = points

    price_lobf = [float(i) for i in
                 list(np.polyfit([i[0] for i in sales_data],
                                 [i[1] for i in sales_data],
                                 deg=3))]

    vol_lobf = [float(i) for i in
                  list(np.polyfit([i[0] for i in volume_data],
                                  [i[1] for i in volume_data],
                                  deg=3))]

    context['price_lobf'] = price_lobf
    context['vol_lobf'] = vol_lobf

    if len(ed_list) > 0:
        cso_dict = get_cso(ed_list, 2016, 'weightedave')
    else:
        cso_dict = get_cso(ref_id, 2016, 'normal')

    cso_dict = normalise_ages(cso_dict)

    context['demo'] = cso_dict

    if calcArea != 'country' and use_cached_natave == False:
        na_sales, na_volume_scaled, na_hist_scaled = get_na_data(False, bad_data,
                     price_max, price_min, dl, dh, volume_data, hist_data, data=None)

        context['na_sales'] = na_sales
        context['na_volume'] = na_volume_scaled
        context['na_hist'] = na_hist_scaled

    context['enoughdata'] = 'true'

    return render(request, 'reporter/index.html', context)


def get_na_data(country, bad_data, price_max, price_min, dl, dh, volume_data, hist_data, data=None):
    if country:
        na_data = data
    elif bad_data == 'true':
        na_data = Sale.objects.filter(nfma='No', price__lte=price_max,
                                   price__gte=price_min, sale_date__gte=dl, sale_date__lte=dh)
    else:
        na_data = Sale.objects.filter(quality='good', nfma='No',
                                   price__lte=price_max, price__gte=price_min,
                                   sale_date__gte=dl, sale_date__lte=dh)

    na_sales, na_volume, na_hist = retrieve_na_stats(na_data)

    na_total = sum(i[1] for i in na_volume)
    total = sum(i[1] for i in volume_data)
    na_volume_scaled = [[i[0], total * (i[1] / na_total) / 4] for i in na_volume]

    na_hist_data = compress_list(na_hist, 10000)

    na_hist_total = sum(na_hist_data.values())
    hist_total = sum(hist_data.values())
    na_hist_scaled = {}

    for k, v in na_hist_data.items():
        na_hist_scaled[k] = (na_hist_data[k] / na_hist_total) * hist_total

    return na_sales, na_volume_scaled, na_hist_scaled


def normalise_ages(data):
    pop_m = 0
    nat_pop_m = 0
    pop_f = 0
    nat_pop_f = 0
    for i in data['age_males']:
        pop_m += i['value']
    for i in data['age_na_males']:
        nat_pop_m += i['value']
    for i in data['age_females']:
        pop_f += i['value']
    for i in data['age_na_females']:
        nat_pop_f += i['value']

    for i in data['age_males']:
        i['value'] = round((i['value']/pop_m) * 100, 2)
    for i in data['age_na_males']:
        i['value'] = round((i['value'] / nat_pop_m) * 100, 2)
    for i in data['age_females']:
        i['value'] = round((i['value'] / pop_f) * 100, 2)
    for i in data['age_na_females']:
        i['value'] = round((i['value'] / nat_pop_f) * 100, 2)

    return data


def get_cso(id, year, mode):
    context = {}

    if mode == 'weightedave':
        cumulative_dict = cycle_cso(id[0][0], year, {})

        count = id[0][1]

        for ed in id[1:]:
            a = cycle_cso(ed[0], year, {})

            count += ed[1]

            for k, v in cumulative_dict.items():

                for i in range(len(v)):
                    addin = a[k][i]['value']
                    cumulative_dict[k][i]['value'] += addin * ed[1]

        for k, v in cumulative_dict.items():
            for i in v:
                i['value'] = int(i['value'] / count)

        context = cumulative_dict
    else:
        context = cycle_cso(id, year, context)

    return context


def cycle_cso(ref_id, year, context):
    t1_data = SexAgeMarriage.objects.filter(uid=ref_id, year=year)[0]
    t2_data = PoBNat.objects.filter(uid=ref_id, year=year)[0]
    t4_data = Families.objects.filter(uid=ref_id, year=year)[0]
    t5_data = PrivHH.objects.filter(uid=ref_id, year=year)[0]
    t6_data = Housing.objects.filter(uid=ref_id, year=year)[0]
    t8_data = PrincStat.objects.filter(uid=ref_id, year=year)[0]
    t9_data = SocClass.objects.filter(uid=ref_id, year=year)[0]
    t10_data = Education.objects.filter(uid=ref_id, year=year)[0]
    t11_data = Commuting.objects.filter(uid=ref_id, year=year)[0]
    t13_data = Occupation.objects.filter(uid=ref_id, year=year)[0]
    t14_data = Industries.objects.filter(uid=ref_id, year=year)[0]
    age_ext_data = AgeExt.objects.filter(uid=ref_id, year=year)[0]
    age_ext_natave = AgeExt.objects.filter(zoom='country', year=year)[0]

    age_males = [
        age_ext_data.age_04_m, age_ext_data.age_59_m, age_ext_data.age_1014_m,
        age_ext_data.age_1519_m, age_ext_data.age_2024_m,
        age_ext_data.age_2529_m,
        age_ext_data.age_3034_m, age_ext_data.age_3539_m,
        age_ext_data.age_4044_m,
        age_ext_data.age_4549_m, age_ext_data.age_5054_m,
        age_ext_data.age_5559_m,
        age_ext_data.age_6064_m, age_ext_data.age_6569_m,
        age_ext_data.age_7074_m,
        age_ext_data.age_7579_m, age_ext_data.age_8084_m,
        age_ext_data.age_85p_m
    ]

    age_na_males = [
        age_ext_natave.age_04_m, age_ext_natave.age_59_m,
        age_ext_natave.age_1014_m,
        age_ext_natave.age_1519_m, age_ext_natave.age_2024_m,
        age_ext_natave.age_2529_m,
        age_ext_natave.age_3034_m, age_ext_natave.age_3539_m,
        age_ext_natave.age_4044_m,
        age_ext_natave.age_4549_m, age_ext_natave.age_5054_m,
        age_ext_natave.age_5559_m,
        age_ext_natave.age_6064_m, age_ext_natave.age_6569_m,
        age_ext_natave.age_7074_m,
        age_ext_natave.age_7579_m, age_ext_natave.age_8084_m,
        age_ext_natave.age_85p_m
    ]

    age_females = [
        age_ext_data.age_04_f, age_ext_data.age_59_f, age_ext_data.age_1014_f,
        age_ext_data.age_1519_f, age_ext_data.age_2024_f,
        age_ext_data.age_2529_f,
        age_ext_data.age_3034_f, age_ext_data.age_3539_f,
        age_ext_data.age_4044_f,
        age_ext_data.age_4549_f, age_ext_data.age_5054_f,
        age_ext_data.age_5559_f,
        age_ext_data.age_6064_f, age_ext_data.age_6569_f,
        age_ext_data.age_7074_f,
        age_ext_data.age_7579_f, age_ext_data.age_8084_f,
        age_ext_data.age_85p_f
    ]

    age_na_females = [
        age_ext_natave.age_04_f, age_ext_natave.age_59_f,
        age_ext_natave.age_1014_f,
        age_ext_natave.age_1519_f, age_ext_natave.age_2024_f,
        age_ext_natave.age_2529_f,
        age_ext_natave.age_3034_f, age_ext_natave.age_3539_f,
        age_ext_natave.age_4044_f,
        age_ext_natave.age_4549_f, age_ext_natave.age_5054_f,
        age_ext_natave.age_5559_f,
        age_ext_natave.age_6064_f, age_ext_natave.age_6569_f,
        age_ext_natave.age_7074_f,
        age_ext_natave.age_7579_f, age_ext_natave.age_8084_f,
        age_ext_natave.age_85p_f]

    age_labels = ['0 - 4', "5 - 9", "10 - 14", "15 - 19", "20 - 24", "25 - 29",
                  "30 - 34", "35 - 39", "40 - 44", "45 - 49", "50 - 54", "55 - 59",
                  "60 - 64", "65 - 69", "70 - 74", "75 - 79", "80 - 84", "85+"]

    age_profile_males = []
    age_natave_males = []
    age_profile_females = []
    age_natave_females = []
    for i in range(len(age_labels)):
        age_profile_males.append({'label': age_labels[i], 'value': age_males[i]})
        age_profile_females.append({'label': age_labels[i], 'value': age_females[i]})
        age_natave_males.append({'label': age_labels[i], 'value': age_na_males[i]})
        age_natave_females.append({'label': age_labels[i], 'value': age_na_females[i]})

    age_data = [
        t1_data.age_04, t1_data.age_59, t1_data.age_1014,
        t1_data.age_1519, t1_data.age_2024, t1_data.age_2529,
        t1_data.age_3034, t1_data.age_3539, t1_data.age_4044,
        t1_data.age_4549, t1_data.age_5054, t1_data.age_5559,
        t1_data.age_6064, t1_data.age_6569, t1_data.age_7074,
        t1_data.age_7579, t1_data.age_8084, t1_data.age_85p
    ]

    age_labels = ['0 - 4', "5 - 9", "10 - 14", "15 - 19", "20 - 24", "25 - 29",
                  "30 - 34", "35 - 39", "40 - 44", "45 - 49", "50 - 54",
                  "55 - 59",
                  "60 - 64", "65 - 69", "70 - 74", "75 - 79", "80 - 84", "85+"
                  ]

    age_profile = []
    for i in range(len(age_data)):
        age_profile.append({'label': age_labels[i], 'value': age_data[i]})

    rel_status = [
        t1_data.single, t1_data.married, t1_data.separated,
        t1_data.divorced, t1_data.widowed
    ]

    rel_labels = [
        'Single', 'Married', 'Separated', 'Divorced', 'Widowed'
    ]

    rel_profile = []
    for i in range(len(rel_status)):
        rel_profile.append({'label': rel_labels[i], 'value': rel_status[i]})

    nat_status = [
        t2_data.nat_ire, t2_data.nat_uk, t2_data.nat_pol, t2_data.nat_lit,
        t2_data.nat_oeu, t2_data.nat_row, t2_data.nat_ns
    ]

    nat_labels = [
        'Irish', 'United Kingdom', 'Polish', 'Lithuanian', 'Other EU',
        'Rest of World', 'Not Stated'
    ]

    nat_profile = []
    for i in range(len(nat_status)):
        nat_profile.append({'label': nat_labels[i], 'value': nat_status[i]})

    child_status = [t4_data.child_0, t4_data.child_1, t4_data.child_2,
                    t4_data.child_3, t4_data.child_4, t4_data.child_ge5]

    child_labels = ["No Children", "1 Child", "2 Children", "3 Children",
                    "4 Children", "5 or More Children"]

    child_profile = []
    for i in range(len(child_status)):
        child_profile.append(
            {'label': child_labels[i], 'value': child_status[i]})

    fam_status = [t4_data.adult, t4_data.pre_fam, t4_data.pre_s,
                  t4_data.early_s, t4_data.pre_adol, t4_data.adol,
                  t4_data.empty_nest, t4_data.retired
                  ]

    fam_labels = ['Adult', 'Pre-Family', 'Pre-School', 'Early School',
                  'Pre-Teen', 'Teenager', 'Empty Nest', 'Retired']

    fam_profile = []
    for i in range(len(fam_status)):
        fam_profile.append({'label': fam_labels[i], 'value': fam_status[i]})

    hh_size = [t5_data.one_phh, t5_data.two_phh, t5_data.three_phh,
               t5_data.four_phh, t5_data.five_phh, t5_data.six_phh,
               t5_data.seven_phh, t5_data.ge_eight_phh]

    hh_labels = ['One Person Household', 'Two Person Household',
                 'Three Person Household', 'Four Person Household',
                 'Five Person Household', 'Six Person Household',
                 'Seven Person Household', 'More than Eight Person Household']

    hh_size_profile = []
    for i in range(len(hh_size)):
        hh_size_profile.append({'label': hh_labels[i], 'value': hh_size[i]})

    house_type_data = [t6_data.house_bung, t6_data.apart, t6_data.bedsit,
                       t6_data.caravan, t6_data.type_ns
                       ]

    house_type_labels = ['House or Bungalow', 'Flat or Apartment', 'Bed-sit',
                         'Caravan', 'Not Stated'
                         ]

    house_type_profile = []
    for i in range(len(house_type_data)):
        house_type_profile.append(
            {'label': house_type_labels[i], 'value': house_type_data[i]})

    house_age_data = [t6_data.l1919, t6_data.b19_45, t6_data.b46_60,
                      t6_data.b61_70, t6_data.b71_80, t6_data.b81_90,
                      t6_data.b91_00,
                      t6_data.b01_10, t6_data.g11, t6_data.h_age_ns
                      ]
    house_age_labels = ['Before 1919', '1919 - 1945', '1946 - 1960',
                        '1961 - 1970', '1971 - 1980', '1981 - 1990',
                        '1991 - 2000',
                        '2001 - 2010', 'After 2011', 'Not Stated'
                        ]

    house_age_profile = []
    for i in range(len(house_age_data)):
        house_age_profile.append(
            {'label': house_age_labels[i], 'value': house_age_data[i]})

    hh_occupancy_data = [t6_data.oo_wm, t6_data.oo_wom, t6_data.rent_pl,
                         t6_data.rent_la, t6_data.rent_vol, t6_data.rent_free,
                         t6_data.occu_ns
                         ]

    hh_occupancy_labels = ['Owner Occupier with Mortgage',
                           'Owner Occupier without Mortgage',
                           'Rented from Private Landlord',
                           'Rented from Local Authority',
                           'Rented from Voluntary Body',
                           'Rented Free of Rent',
                           'Not Stated'
                           ]

    hh_occupancy_profile = []
    for i in range(len(hh_occupancy_data)):
        hh_occupancy_profile.append(
            {'label': hh_occupancy_labels[i], 'value': hh_occupancy_data[i]})

    hh_rooms_data = [t6_data.rooms_1, t6_data.rooms_2, t6_data.rooms_3,
                     t6_data.rooms_4, t6_data.rooms_5, t6_data.rooms_6,
                     t6_data.rooms_7, t6_data.rooms_ge8, t6_data.rooms_ns
                     ]

    hh_rooms_labels = ['1 Room', '2 Rooms', '3 Rooms', '4 Rooms', '5 Rooms',
                       '6 Rooms', '7 Rooms', 'More than 8 Rooms', 'Not Stated'
                       ]

    hh_rooms_profile = []
    for i in range(len(hh_rooms_data)):
        hh_rooms_profile.append(
            {'label': hh_rooms_labels[i], 'value': hh_rooms_data[i]})

    hh_occupation_data = [t6_data.occupied, t6_data.temp_unoc,
                          t6_data.unoc_hol, t6_data.unoccupied]

    hh_occupation_labels = ['Occupied', 'Temporarily Unoccupied',
                            'Unoccupied Holiday Home', 'Unoccupied']

    hh_occupation_profile = []
    for i in range(len(hh_occupation_data)):
        hh_occupation_profile.append(
            {'label': hh_occupation_labels[i], 'value': hh_occupation_data[i]})

    prince_stat_data = [t8_data.work, t8_data.lffj, t8_data.unemployed,
                        t8_data.student, t8_data.home_fam, t8_data.retired,
                        t8_data.sick_dis,
                        t8_data.stat_other
                        ]

    prince_stat_labels = ['Working', 'Looking for First Job', 'Unemployed',
                          'Student', 'Looking After Home/Family', 'Retired',
                          'Sick or Disabled',
                          'Other'
                          ]

    prince_stat_profile = []
    for i in range(len(prince_stat_data)):
        prince_stat_profile.append(
            {'label': prince_stat_labels[i], 'value': prince_stat_data[i]})

    socclass_data = [t9_data.prof_worker, t9_data.manage_tech,
                     t9_data.non_manual, t9_data.skilled_manual,
                     t9_data.semi_skilled, t9_data.unskilled,
                     t9_data.class_other
                     ]

    socclass_labels = ['Professional Worker', 'Managerial and Technical',
                       'Non-Manual', 'Skilled Manual',
                       'Semi-Skilled', 'Unskilled', 'All Others']

    socclass_profile = []
    for i in range(len(socclass_data)):
        socclass_profile.append(
            {'label': socclass_labels[i], 'value': socclass_data[i]})

    education_data = [t10_data.nfe, t10_data.primary, t10_data.l_secondary,
                      t10_data.u_secondary, t10_data.tech_vocat,
                      t10_data.apprentice,
                      t10_data.high_cert, t10_data.bach, t10_data.bach_hons,
                      t10_data.postgrad, t10_data.doctorate, t10_data.ed_ns
                      ]

    education_labels = ['No Formal Education', 'Primary', 'Lower Secondary',
                        'Upper Secondary', 'Technical Vocatation',
                        'Apprenticeship',
                        'Higher Certificate', 'Bachelors Degree',
                        'Bachelors Degree (Hons)',
                        'Postgraduate Degree', 'Doctorate', 'Not Stated'
                        ]

    education_profile = []
    for i in range(len(education_data)):
        education_profile.append(
            {'label': education_labels[i], 'value': education_data[i]})

    transport_method_data = [t11_data.foot, t11_data.bike, t11_data.bus,
                             t11_data.train, t11_data.mbike, t11_data.car_d,
                             t11_data.car_p,
                             t11_data.van, t11_data.other, t11_data.method_ns
                             ]

    transport_method_labels = ['Walking', 'Cycling', 'Bus', 'Train',
                               'Motorbike', 'Car (Driver)', 'Car (Passenger)',
                               'Van', 'Other', 'Not Stated'
                               ]

    transport_method_profile = []
    for i in range(len(transport_method_data)):
        transport_method_profile.append({'label': transport_method_labels[i],
                                         'value': transport_method_data[i]})

    transport_time_data = [t11_data.u15m, t11_data.b15_30m, t11_data.b30_45m,
                           t11_data.b45_60m, t11_data.b60_90m, t11_data.o90m,
                           t11_data.time_ns
                           ]

    transport_time_labels = ['Under 15 minutes', '15 - 30 minutes',
                             '30 - 45 minutes', '45 - 60 minutes',
                             '60 - 90 minutes', 'Over 90 minutes', 'Not Stated'
                             ]

    transport_time_profile = []
    for i in range(len(transport_time_data)):
        transport_time_profile.append({'label': transport_time_labels[i],
                                       'value': transport_time_data[i]})

    occupation_data = [t13_data.man_dir_sos, t13_data.prof_oc,
                       t13_data.assoc_prof_tech, t13_data.admin_sec,
                       t13_data.skilled_trade,
                       t13_data.caring_leisure, t13_data.sales_cs,
                       t13_data.process_plant,
                       t13_data.elementary, t13_data.occ_ns
                       ]

    occupation_labels = [
        'Managers, Directors and Senior Officials', 'Professional Occupations',
        'Associate Professional and Technical Occupations',
        'Administrative and Secretarial Occupations',
        'Skilled Trades Occupations',
        'Caring, Leisure and Other Service Occupations',
        'Sales and Customer Service Occupations ',
        'Process, Plant and Machine Operatives', 'Elementary Occupations',
        'Not Stated'
    ]

    occupation_profile = []
    for i in range(len(occupation_data)):
        occupation_profile.append(
            {'label': occupation_labels[i], 'value': occupation_data[i]})

    industry_data = [t14_data.ag_for_fish, t14_data.build_construct,
                     t14_data.manufac, t14_data.comm_trade,
                     t14_data.trans_coms, t14_data.pub_admin,
                     t14_data.prof_ser, t14_data.ind_other]

    industry_labels = ['Agriculture, Forestry and Fishing',
                       'Building and Construction', 'Manufacturing',
                       'Commerce and Trade',
                       'Transport and Communications ',
                       'Public Administration',
                       'Professional Services', 'Other']

    industry_profile = []
    for i in range(len(industry_data)):
        industry_profile.append(
            {'label': industry_labels[i], 'value': industry_data[i]})

    context['age_males'] = age_profile_males
    context['age_na_males'] = age_natave_males
    context['age_females'] = age_profile_females
    context['age_na_females'] = age_natave_females
    context['age_profile'] = age_profile
    context['rel_profile'] = rel_profile
    context['nat_profile'] = nat_profile
    context['child_profile'] = child_profile
    context['fam_profile'] = fam_profile
    context['hh_size_profile'] = hh_size_profile
    context['house_type_profile'] = house_type_profile
    context['house_age_profile'] = house_age_profile
    context['hh_occupancy_profile'] = hh_occupancy_profile
    context['hh_rooms_profile'] = hh_rooms_profile
    context['hh_occupation_profile'] = hh_occupation_profile
    context['prince_stat_profile'] = prince_stat_profile
    context['socclass_profile'] = socclass_profile
    context['education_profile'] = education_profile
    context['transport_method_profile'] = transport_method_profile
    context['transport_time_profile'] = transport_time_profile
    context['occupation_profile'] = occupation_profile
    context['industry_profile'] = industry_profile

    return context


def latlng(clat, clng, d, dir):
    R = 6378.1
    if dir == 'N':
        brng = 0
    elif dir == 'E':
        brng = 1.57
    elif dir == 'S':
        brng = 3.14
    elif dir == 'W':
        brng = 4.71
    else:
        brng = 0

    lat1 = (clat / 180) * math.pi
    lng1 = (clng / 180) * math.pi

    lat2 = math.asin(math.sin(lat1) * math.cos(d / R) + math.cos(lat1)
                     * math.sin(d / R) * math.cos(brng))
    lng2 = lng1 + math.atan2(math.sin(brng) * math.sin(d / R) * math
                             .cos(lat1),
                             math.cos(d / R) - math.sin(lat1) * math
                             .sin(lat2))

    return [lat2 * (180 / math.pi), lng2 * (180 / math.pi)]


def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - math.cos((lat2 - lat1) * p) / 2 + math.cos(lat1 * p) * math.cos(lat2 * p) * (1 - math.cos((lon2 - lon1) * p)) / 2

    return 12742 * math.asin(math.sqrt(a))


def retrieve_stats(queryset):

    sale_list = []
    size_list = []
    hist_data = []

    scatter_data = {'date': [], 'price': []}
    new_data = {'date': [], 'new': [], 'used': []}

    for sale in queryset:
        raw_time = calendar.timegm(sale.sale_date.timetuple())
        sale_list.append(raw_time)
        scatter_data['date'].append(sale.sale_date)
        scatter_data['price'].append(float(sale.price))
        hist_data.append(float(sale.price))

        if sale.PSD == 'greater than or equal to 38 sq metres and less than 125 sq metres':
            size_list.append(81.5)
        elif sale.PSD == 'greater than 125 sq metres':
            size_list.append(125)
        elif sale.PSD == 'less than 38 sq metres':
            size_list.append(38)

        if sale.DoP == 'Second-Hand Dwelling house /Apartment':
            new_data['date'].append(sale.sale_date)
            new_data['new'].append(0)
            new_data['used'].append(float(sale.price))
        else:
            new_data['date'].append(sale.sale_date)
            new_data['new'].append(float(sale.price))
            new_data['used'].append(0)

    compressed_hist_data = compress_list(hist_data, 25000)

    if max(compressed_hist_data.keys()) / 25 < 25000:
        compressed_hist_data = compress_list(hist_data, 20000)
        if max(compressed_hist_data.keys()) / 25 < 20000:
            compressed_hist_data = compress_list(hist_data, 15000)
            if max(compressed_hist_data.keys()) / 25 < 15000:
                compressed_hist_data = compress_list(hist_data, 10000)

    avg_size = round(np.mean(size_list), 1)

    df = pd.DataFrame(scatter_data, columns=['price'], index=scatter_data['date'])
    new_df = pd.DataFrame(new_data, columns=['new', 'used'], index=new_data['date'])

    df.index.names = ['date']
    new_df.index.names = ['date']

    df = df.set_index(pd.DatetimeIndex(df.index))
    new_df = new_df.set_index(pd.DatetimeIndex(new_df.index))
    sdf = df.resample('W').mean().dropna(axis=0, how='any')
    sdf = sdf[sdf['price'] != 0]
    vdf = df.resample('W').count().dropna(axis=0, how='any')
    vdf = vdf[vdf['price'] != 0]

    ndf = new_df[new_df['new'] != 0]['new']
    ndf = ndf.resample('W').count().dropna(axis=0, how='any')
    udf = new_df[new_df['used'] != 0]['used']
    udf = udf.resample('W').count().dropna(axis=0, how='any')
    idf = new_df.resample('W').count().dropna(axis=0, how='any')

    scatter_data = list(map(lambda x, y: [calendar.timegm(x.to_pydatetime().timetuple()) * 1000,
                      round(float(y), 2)], sdf.index.tolist(), sdf.values))
    volume_data = list(map(lambda x, y: [calendar.timegm(x.to_pydatetime().timetuple()) * 1000,
                      round(float(y), 2)], vdf.index.tolist(), vdf.values))

    new_scatter_data = list(map(
        lambda x, y, z: [calendar.timegm(x.to_pydatetime().timetuple()) * 1000,
                         round(float(y), 2), round(float(z), 2)],
        idf.index.tolist(), udf.tolist(), ndf.tolist()))

    return scatter_data, compressed_hist_data, volume_data, new_scatter_data, avg_size


def compress_list(data, limit):
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

    b = {}
    for k, v in a.items():
        if v > max(a.values()) * 0.05:
            b[k] = v

    return b


def retrieve_na_stats(queryset):
    sale_list = []
    hist_data = []

    scatter_data = {'date': [], 'price': []}

    for sale in queryset:
        raw_time = calendar.timegm(sale.sale_date.timetuple())
        sale_list.append(raw_time)
        scatter_data['date'].append(sale.sale_date)
        scatter_data['price'].append(float(sale.price))
        hist_data.append(float(sale.price))

    df = pd.DataFrame(scatter_data, columns=['price'],
                      index=scatter_data['date'])
    df.index.names = ['date']
    df = df.set_index(pd.DatetimeIndex(df.index))

    nasdf = df.resample('M').mean().dropna(axis=0, how='any')
    nasdf = nasdf[nasdf['price'] != 0]
    na_scatter_data = list(map(lambda x, y: [calendar.timegm(x.to_pydatetime().timetuple()) * 1000,
                      round(float(y), 2)], nasdf.index.tolist(), nasdf.values))
    navdf = df.resample('M').count().dropna(axis=0, how='any')
    navdf = navdf[navdf['price'] != 0]
    na_volume_data = list(map(lambda x, y: [calendar.timegm(x.to_pydatetime().timetuple()) * 1000,
                      round(float(y), 2)], navdf.index.tolist(), navdf.values))

    return na_scatter_data, na_volume_data, hist_data


def ajax_response_chart(request):
    cookies = request.COOKIES

    date_max = int(cookies.get('max_date', 1491001200000))
    date_min = int(cookies.get('min_date', 1262304000000))
    price_max = float(cookies.get('max_price', 0))
    price_min = float(cookies.get('min_price', 10000000))
    left = float(cookies.get('left', -6.30896600036624))
    right = float(cookies.get('right', -6.211633999633818))
    top = float(cookies.get('top', 53.368906276426856))
    bottom = float(cookies.get('bottom', 53.330685156427386))
    calcArea = cookies.get('areaMain', 'country')
    area = cookies.get('areaSecond', 'Dublin')
    radius = float(cookies.get('radius', 1))
    bad_data = cookies.get('bad_data_inc', 'true')

    dh = datetime.datetime.fromtimestamp(date_max / 1000)

    time = request.GET['time']

    if time == '1 Month':
        d = 31
    elif time == '3 Months':
        d = 91
    elif time == '6 Months':
        d = 183
    elif time == '1 Year':
        d = 365
    elif time == '2 Years':
        d = 365 * 2
    elif time == '5 Years':
        d = 365 * 5

    if time != 'All':
        date_min = date_max - (d * 60 * 60 * 24 * 1000)

    dl = datetime.datetime.fromtimestamp(date_min / 1000)

    if calcArea == 'map':

        data = Sale.objects.filter(quality='good', nfma='No').filter(
            latitude__gte=bottom, latitude__lte=top, longitude__gte=left,
            longitude__lte=right, price__lte=price_max, price__gte=price_min,
            sale_date__gte=dl, sale_date__lte=dh)

    elif calcArea == 'radius':

        c_lat = (top - bottom) / 2 + bottom
        c_lng = (left - right) / 2 + right

        right = latlng(c_lat, c_lng, radius, 'E')[1]
        left = latlng(c_lat, c_lng, radius, 'W')[1]
        top = latlng(c_lat, c_lng, radius, 'N')[0]
        bottom = latlng(c_lat, c_lng, radius, 'S')[0]

        data = Sale.objects.filter(quality='good', nfma='No').filter(
            latitude__gte=bottom, latitude__lte=top, longitude__gte=left,
            longitude__lte=right, price__lte=price_max, price__gte=price_min,
            sale_date__gte=dl, sale_date__lte=dh)

        rad_list = []

        for sale in data:
            lat = float(sale.latitude)
            lng = float(sale.longitude)

            if distance(c_lat, c_lng, lat, lng) <= radius:
                rad_list.append(sale)

        data = rad_list

    elif calcArea == 'county':
        if bad_data == 'true':
            data = Sale.objects.filter(nfma='No', price__lte=price_max, price__gte=price_min,
                                       sale_date__gte=dl, sale_date__lte=dh, county=area)
        else:
            data = Sale.objects.filter(quality='good', nfma='No', price__lte=price_max, price__gte=price_min,
                                       sale_date__gte=dl, sale_date__lte=dh, county=area)
    elif calcArea == 'region':
        if bad_data == 'true':
            data = Sale.objects.filter(nfma='No', price__lte=price_max, price__gte=price_min,
                                       sale_date__gte=dl, sale_date__lte=dh, region=area)
        else:
            data = Sale.objects.filter(quality='good', nfma='No', price__lte=price_max, price__gte=price_min,
                                       sale_date__gte=dl, sale_date__lte=dh, region=area)
    elif calcArea == 'country':
        if bad_data == 'true':
            data = Sale.objects.filter(nfma='No', price__lte=price_max, price__gte=price_min,
                                       sale_date__gte=dl, sale_date__lte=dh)
        else:
            data = Sale.objects.filter(quality='good', nfma='No', price__lte=price_max, price__gte=price_min,
                                       sale_date__gte=dl, sale_date__lte=dh)

    if request.GET['chart'] == 'hist':
        hist_data = []
        for sale in data:
            hist_data.append(float(sale.price))

        compressed_hist_data = compress_list(hist_data, 25000)

        if max(compressed_hist_data.keys()) / 25 < 25000:
            compressed_hist_data = compress_list(hist_data, 20000)
            if max(compressed_hist_data.keys()) / 25 < 20000:
                compressed_hist_data = compress_list(hist_data, 15000)
                if max(compressed_hist_data.keys()) / 25 < 15000:
                    compressed_hist_data = compress_list(hist_data, 10000)

        hist_total = sum(compressed_hist_data.values())

        if calcArea != 'country':
            if bad_data == 'true':
                data = Sale.objects.filter(nfma='No', price__lte=price_max,
                                              price__gte=price_min,
                                              sale_date__gte=dl, sale_date__lte=dh)
            else:
                data = Sale.objects.filter(quality='good', nfma='No',
                                              price__lte=price_max,
                                              price__gte=price_min,
                                              sale_date__gte=dl, sale_date__lte=dh)

            hist_data = []

            for sale in data:
                hist_data.append(float(sale.price))

        na_hist_data = compress_list(hist_data, 10000)
        na_hist_total = sum(na_hist_data.values())
        na_hist_scaled = {}

        for k, v in na_hist_data.items():
            na_hist_scaled[k] = (na_hist_data[k] / na_hist_total) * hist_total

        data_dict = {'hist_data': compressed_hist_data, 'na_hist': na_hist_scaled}

    elif request.GET['chart'] == 'scatter':
        agg = request.GET['agg']

        cid = int(request.GET['chart_id'])

        if cid == 1 or cid == 2:
            scatter_data = {'date': [], 'price': []}

            for sale in data:
                scatter_data['date'].append(sale.sale_date)
                scatter_data['price'].append(float(sale.price))

            df = pd.DataFrame(scatter_data, columns=['price'], index=scatter_data['date'])
            df.index.names = ['date']
            df = df.set_index(pd.DatetimeIndex(df.index))

            if cid == 1:

                sdf = df.resample(agg).mean().dropna(axis=0, how='any')
                sdf = sdf[sdf['price'] != 0]

                scatter_data = list(map(lambda x, y: [calendar.timegm(x.to_pydatetime().timetuple()) * 1000,
                    round(float(y), 2)], sdf.index.tolist(), sdf.values))

                data_dict = {'scatter_data': scatter_data, 'agg': agg}
            else:
                vdf = df.resample(agg).count().dropna(axis=0, how='any')
                vdf = vdf[vdf['price'] != 0]

                volume_data = list(map(lambda x, y: [calendar.timegm(x.to_pydatetime().timetuple()) * 1000,
                    round(float(y), 2)], vdf.index.tolist(), vdf.values))

                data_dict = {'scatter_data': volume_data, 'agg': agg}

            lobf_coef = [float(i) for i in
                         list(np.polyfit([i[0] for i in data_dict['scatter_data']],
                                         [i[1] for i in data_dict['scatter_data']],
                                         deg=3))]
            data_dict['lobf_coef'] = lobf_coef


        elif cid == 3:
            new_data = {'date': [], 'used': [], 'new': []}

            for sale in data:
                if sale.DoP == 'Second-Hand Dwelling house /Apartment':
                    new_data['date'].append(sale.sale_date)
                    new_data['used'].append(float(sale.price))
                    new_data['new'].append(0)
                else:
                    new_data['date'].append(sale.sale_date)
                    new_data['used'].append(0)
                    new_data['new'].append(float(sale.price))

            new_df = pd.DataFrame(new_data, columns=['new', 'used'], index=new_data['date'])
            new_df.index.names = ['date']

            new_df = new_df.set_index(pd.DatetimeIndex(new_df.index))
            ndf = new_df[new_df['new'] != 0]['new']
            ndf = ndf.resample(agg).count().dropna(axis=0, how='any')
            udf = new_df[new_df['used'] != 0]['used']
            udf = udf.resample(agg).count().dropna(axis=0, how='any')
            idf = new_df.resample(agg).count().dropna(axis=0, how='any')

            new_scatter_data = list(map(
                lambda x, y, z: [calendar.timegm(x.to_pydatetime().timetuple()) * 1000, round(float(y), 2), round(float(z), 2)], idf.index.tolist(), udf.tolist(), ndf.tolist()))


            data_dict = {'scatter_data': new_scatter_data, 'agg': agg}


    return HttpResponse(json.dumps(data_dict))


def ajax_response_pie(request):
    cookies = request.COOKIES

    left = float(cookies.get('left', -6.30896600036624))
    right = float(cookies.get('right', -6.211633999633818))
    top = float(cookies.get('top', 53.368906276426856))
    bottom = float(cookies.get('bottom', 53.330685156427386))
    calcArea = cookies.get('areaMain', 'country')
    area = cookies.get('areaSecond', 'Dublin')
    radius = float(cookies.get('radius', 1))
    
    year = int(request.GET['year'])
    chartname = request.GET['chartname']

    if calcArea == 'map':
        ed_list = []
        ed_count = {}
        data = Sale.objects.filter(quality='good', nfma='No').filter(
            latitude__gte=bottom, latitude__lte=top, longitude__gte=left,
            longitude__lte=right)

        for sale in data:
            if sale.ed in ed_count.keys():
                ed_count[sale.ed] += 1
            else:
                ed_count[sale.ed] = 1

        eds_to_use = []
        for k, v in ed_count.items():
            if v > max(ed_count.values()) / 3:
                eds_to_use.append([k, v])
        for ed in eds_to_use:
            try:
                ref = CSORef.objects.filter(desc=ed[0])[0].uid
                ed_list.append([ref, ed[1]])
            except:
                continue

        cumulative_dict = get_cso_light(chartname, ed_list[0][0], year)

        count = ed_list[0][1]

        for ed in ed_list[1:]:
            a = get_cso_light(chartname, ed[0], year)

            count += ed[1]

            for k, v in cumulative_dict.items():

                for i in range(len(v)):
                    addin = a[k][i]['value']
                    cumulative_dict[k][i]['value'] += addin * ed[1]

        for k, v in cumulative_dict.items():
            for i in v:
                i['value'] = int(i['value'] / count)

        final_data = cumulative_dict[chartname]

    elif calcArea == 'radius':

        c_lat = (top - bottom) / 2 + bottom
        c_lng = (left - right) / 2 + right

        right = latlng(c_lat, c_lng, radius, 'E')[1]
        left = latlng(c_lat, c_lng, radius, 'W')[1]
        top = latlng(c_lat, c_lng, radius, 'N')[0]
        bottom = latlng(c_lat, c_lng, radius, 'S')[0]

        data = Sale.objects.filter(quality='good', nfma='No').filter(
            latitude__gte=bottom, latitude__lte=top, longitude__gte=left,
            longitude__lte=right)
        ed_list = []
        ed_count = {}

        c_lat = (top - bottom) / 2 + bottom
        c_lng = (left - right) / 2 + right

        for sale in data:
            lat = float(sale.latitude)
            lng = float(sale.longitude)

            if distance(c_lat, c_lng, lat, lng) <= radius:
                if sale.ed in ed_count.keys():
                    ed_count[sale.ed] += 1
                else:
                    ed_count[sale.ed] = 1

        eds_to_use = []
        for k, v in ed_count.items():
            if v > max(ed_count.values()) / 3:
                eds_to_use.append([k, v])
        for ed in eds_to_use:
            try:
                ref = CSORef.objects.filter(desc=ed[0])[0].uid
                ed_list.append([ref, ed[1]])
            except:
                continue

        cumulative_dict = get_cso_light(chartname, ed_list[0][0], year)

        count = ed_list[0][1]

        for ed in ed_list[1:]:
            a = get_cso_light(chartname, ed[0], year)

            count += ed[1]

            for k, v in cumulative_dict.items():

                for i in range(len(v)):
                    addin = a[k][i]['value']
                    cumulative_dict[k][i]['value'] += addin * ed[1]

        for k, v in cumulative_dict.items():
            for i in v:
                i['value'] = int(i['value'] / count)

        final_data = cumulative_dict[chartname]

    elif calcArea == 'county':
        ref_id = CSORef.objects.filter(desc=area, zoom='county')[0].uid
        final_data = get_cso_light(chartname, ref_id, year)[chartname]
    elif calcArea == 'region':
        ref_id = CSORef.objects.filter(desc=area, zoom='region')[0].uid
        final_data = get_cso_light(chartname, ref_id, year)[chartname]
    elif calcArea == 'country':
        ref_id = 'I00'
        final_data = get_cso_light(chartname, ref_id, year)[chartname]


    return HttpResponse(json.dumps(final_data))


def get_cso_light(chartname, ref_id, year):
    if chartname == 'one':
        data = SexAgeMarriage.objects.filter(uid=ref_id, year=year)[0]

        age_labels = ['0 - 4', "5 - 9", "10 - 14", "15 - 19", "20 - 24",
                      "25 - 29",
                      "30 - 34", "35 - 39", "40 - 44", "45 - 49", "50 - 54",
                      "55 - 59",
                      "60 - 64", "65 - 69", "70 - 74", "75 - 79", "80 - 84",
                      "85+"]

        age_data = [data.age_04, data.age_59, data.age_1014,
                    data.age_1519, data.age_2024, data.age_2529,
                    data.age_3034, data.age_3539, data.age_4044,
                    data.age_4549, data.age_5054, data.age_5559,
                    data.age_6064, data.age_6569, data.age_7074,
                    data.age_7579, data.age_8084, data.age_85p]

        final_data = []
        for i in range(len(age_data)):
            final_data.append({'label': age_labels[i], 'value': age_data[i]})
    elif chartname == 'two':
        data = SexAgeMarriage.objects.filter(uid=ref_id, year=year)[0]

        rel_status = [data.single, data.married, data.separated, data.divorced,
                      data.widowed]

        rel_labels = ['Single', 'Married', 'Separated', 'Divorced', 'Widowed']

        final_data = []
        for i in range(len(rel_status)):
            final_data.append({'label': rel_labels[i], 'value': rel_status[i]})
    elif chartname == 'three':
        data = PoBNat.objects.filter(uid=ref_id, year=year)[0]

        nat_status = [
            data.nat_ire, data.nat_uk, data.nat_pol, data.nat_lit,
            data.nat_oeu, data.nat_row, data.nat_ns]

        nat_labels = [
            'Irish', 'United Kingdom', 'Polish', 'Lithuanian', 'Other EU',
            'Rest of World', 'Not Stated']

        final_data = []
        for i in range(len(nat_status)):
            final_data.append({'label': nat_labels[i], 'value': nat_status[i]})
    elif chartname == 'four':
        data = Families.objects.filter(uid=ref_id, year=year)[0]

        child_status = [data.child_0, data.child_1, data.child_2,
                        data.child_3, data.child_4, data.child_ge5]

        child_labels = ["No Children", "1 Child", "2 Children", "3 Children",
                        "4 Children", "5 or More Children"]

        final_data = []
        for i in range(len(child_status)):
            final_data.append(
                {'label': child_labels[i], 'value': child_status[i]})
    elif chartname == 'five':
        data = Families.objects.filter(uid=ref_id, year=year)[0]

        fam_status = [data.adult, data.pre_fam, data.pre_s,
                      data.early_s, data.pre_adol, data.adol,
                      data.empty_nest, data.retired
                      ]

        fam_labels = ['Adult', 'Pre-Family', 'Pre-School', 'Early School',
                      'Pre-Teen', 'Teenager', 'Empty Nest', 'Retired']

        final_data = []
        for i in range(len(fam_status)):
            final_data.append({'label': fam_labels[i], 'value': fam_status[i]})
    elif chartname == 'six':
        data = PrivHH.objects.filter(uid=ref_id, year=year)[0]

        hh_size = [data.one_phh, data.two_phh, data.three_phh,
                   data.four_phh, data.five_phh, data.six_phh,
                   data.seven_phh, data.ge_eight_phh]

        hh_labels = ['One Person Household', 'Two Person Household',
                     'Three Person Household', 'Four Person Household',
                     'Five Person Household', 'Six Person Household',
                     'Seven Person Household',
                     'More than Eight Person Household']

        final_data = []
        for i in range(len(hh_size)):
            final_data.append({'label': hh_labels[i], 'value': hh_size[i]})
    elif chartname == 'seven':
        data = Housing.objects.filter(uid=ref_id, year=year)[0]

        house_type_data = [data.house_bung, data.apart, data.bedsit,
                           data.caravan, data.type_ns
                           ]

        house_type_labels = ['House or Bungalow', 'Flat or Apartment',
                             'Bed-sit',
                             'Caravan', 'Not Stated'
                             ]

        final_data = []
        for i in range(len(house_type_data)):
            final_data.append(
                {'label': house_type_labels[i], 'value': house_type_data[i]})
    elif chartname == 'eight':
        data = Housing.objects.filter(uid=ref_id, year=year)[0]

        house_age_data = [data.l1919, data.b19_45, data.b46_60,
                          data.b61_70, data.b71_80, data.b81_90,
                          data.b91_00,
                          data.b01_10, data.g11, data.h_age_ns
                          ]
        house_age_labels = ['Before 1919', '1919 - 1945', '1946 - 1960',
                            '1961 - 1970', '1971 - 1980', '1981 - 1990',
                            '1991 - 2000', '2001 - 2010', 'After 2011', 'Not Stated'
                            ]

        final_data = []
        for i in range(len(house_age_data)):
            final_data.append(
                {'label': house_age_labels[i], 'value': house_age_data[i]})
    elif chartname == 'nine':
        data = Housing.objects.filter(uid=ref_id, year=year)[0]

        hh_occupancy_data = [data.oo_wm, data.oo_wom, data.rent_pl,
                             data.rent_la, data.rent_vol,
                             data.rent_free,
                             data.occu_ns
                             ]

        hh_occupancy_labels = ['Owner Occupier with Mortgage',
                               'Owner Occupier without Mortgage',
                               'Rented from Private Landlord',
                               'Rented from Local Authority',
                               'Rented from Voluntary Body',
                               'Rented Free of Rent',
                               'Not Stated'
                               ]

        final_data = []
        for i in range(len(hh_occupancy_data)):
            final_data.append({'label': hh_occupancy_labels[i],
                               'value': hh_occupancy_data[i]})
    elif chartname == 'ten':
        data = Housing.objects.filter(uid=ref_id, year=year)[0]

        hh_rooms_data = [data.rooms_1, data.rooms_2, data.rooms_3,
                         data.rooms_4, data.rooms_5, data.rooms_6,
                         data.rooms_7, data.rooms_ge8, data.rooms_ns
                         ]

        hh_rooms_labels = ['1 Room', '2 Rooms', '3 Rooms', '4 Rooms',
                           '5 Rooms',
                           '6 Rooms', '7 Rooms', 'More than 8 Rooms',
                           'Not Stated'
                           ]

        final_data = []
        for i in range(len(hh_rooms_data)):
            final_data.append(
                {'label': hh_rooms_labels[i], 'value': hh_rooms_data[i]})
    elif chartname == 'eleven':
        data = Housing.objects.filter(uid=ref_id, year=year)[0]

        hh_occupation_data = [data.occupied, data.temp_unoc,
                              data.unoc_hol, data.unoccupied]

        hh_occupation_labels = ['Occupied', 'Temporarily Unoccupied',
                                'Unoccupied Holiday Home', 'Unoccupied']

        final_data = []
        for i in range(len(hh_occupation_data)):
            final_data.append(
                {'label': hh_occupation_labels[i],
                 'value': hh_occupation_data[i]})
    elif chartname == 'twelve':
        data = PrincStat.objects.filter(uid=ref_id, year=year)[0]

        prince_stat_data = [data.work, data.lffj, data.unemployed,
                            data.student, data.home_fam, data.retired,
                            data.sick_dis,
                            data.stat_other
                            ]

        prince_stat_labels = ['Working', 'Looking for First Job', 'Unemployed',
                              'Student', 'Looking After Home/Family',
                              'Retired',
                              'Sick or Disabled',
                              'Other'
                              ]

        final_data = []
        for i in range(len(prince_stat_data)):
            final_data.append(
                {'label': prince_stat_labels[i], 'value': prince_stat_data[i]})
    elif chartname == 'thirteen':
        data = SocClass.objects.filter(uid=ref_id, year=year)[0]

        socclass_data = [data.prof_worker, data.manage_tech,
                         data.non_manual, data.skilled_manual,
                         data.semi_skilled, data.unskilled,
                         data.class_other
                         ]

        socclass_labels = ['Professional Worker', 'Managerial and Technical',
                           'Non-Manual', 'Skilled Manual',
                           'Semi-Skilled', 'Unskilled', 'All Others']

        final_data = []
        for i in range(len(socclass_data)):
            final_data.append(
                {'label': socclass_labels[i], 'value': socclass_data[i]})
    elif chartname == 'fourteen':
        data = Education.objects.filter(uid=ref_id, year=year)[0]

        education_data = [data.nfe, data.primary, data.l_secondary,
                          data.u_secondary, data.tech_vocat,
                          data.apprentice,
                          data.high_cert, data.bach,
                          data.bach_hons,
                          data.postgrad, data.doctorate, data.ed_ns
                          ]

        education_labels = ['No Formal Education', 'Primary',
                            'Lower Secondary',
                            'Upper Secondary', 'Technical Vocatation',
                            'Apprenticeship',
                            'Higher Certificate', 'Bachelors Degree',
                            'Bachelors Degree (Hons)',
                            'Postgraduate Degree', 'Doctorate', 'Not Stated'
                            ]

        final_data = []
        for i in range(len(education_data)):
            final_data.append(
                {'label': education_labels[i], 'value': education_data[i]})
    elif chartname == 'fifteen':
        data = Commuting.objects.filter(uid=ref_id, year=year)[0]

        transport_method_data = [data.foot, data.bike, data.bus,
                                 data.train, data.mbike,
                                 data.car_d,
                                 data.car_p,
                                 data.van, data.other,
                                 data.method_ns
                                 ]

        transport_method_labels = ['Walking', 'Cycling', 'Bus', 'Train',
                                   'Motorbike', 'Car (Driver)',
                                   'Car (Passenger)',
                                   'Van', 'Other', 'Not Stated'
                                   ]

        final_data = []
        for i in range(len(transport_method_data)):
            final_data.append({'label': transport_method_labels[i],
                               'value': transport_method_data[i]})
    elif chartname == 'sixteen':
        data = Commuting.objects.filter(uid=ref_id, year=year)[0]

        transport_time_data = [data.u15m, data.b15_30m,
                               data.b30_45m,
                               data.b45_60m, data.b60_90m,
                               data.o90m,
                               data.time_ns
                               ]

        transport_time_labels = ['Under 15 minutes', '15 - 30 minutes',
                                 '30 - 45 minutes', '45 - 60 minutes',
                                 '60 - 90 minutes', 'Over 90 minutes',
                                 'Not Stated'
                                 ]

        final_data = []
        for i in range(len(transport_time_data)):
            final_data.append({'label': transport_time_labels[i],
                               'value': transport_time_data[i]})
    elif chartname == 'seventeen':
        data = Occupation.objects.filter(uid=ref_id, year=year)[0]

        occupation_data = [data.man_dir_sos, data.prof_oc,
                           data.assoc_prof_tech, data.admin_sec,
                           data.skilled_trade,
                           data.caring_leisure, data.sales_cs,
                           data.process_plant,
                           data.elementary, data.occ_ns
                           ]

        occupation_labels = [
            'Managers, Directors and Senior Officials',
            'Professional Occupations',
            'Associate Professional and Technical Occupations',
            'Administrative and Secretarial Occupations',
            'Skilled Trades Occupations',
            'Caring, Leisure and Other Service Occupations',
            'Sales and Customer Service Occupations ',
            'Process, Plant and Machine Operatives', 'Elementary Occupations',
            'Not Stated'
        ]

        final_data = []
        for i in range(len(occupation_data)):
            final_data.append(
                {'label': occupation_labels[i], 'value': occupation_data[i]})
    elif chartname == 'eighteen':
        data = Industries.objects.filter(uid=ref_id, year=year)[0]

        industry_data = [data.ag_for_fish, data.build_construct,
                         data.manufac, data.comm_trade,
                         data.trans_coms, data.pub_admin,
                         data.prof_ser, data.ind_other]

        industry_labels = ['Agriculture, Forestry and Fishing',
                           'Building and Construction', 'Manufacturing',
                           'Commerce and Trade',
                           'Transport and Communications ',
                           'Public Administration',
                           'Professional Services', 'Other']

        final_data = []
        for i in range(len(industry_data)):
            final_data.append(
                {'label': industry_labels[i], 'value': industry_data[i]})

    return {chartname: final_data}