from django.shortcuts import render, HttpResponse
from prac.models import Sale, CSORef
from django.conf import settings
from django.db.models import Max, Count
import json
import datetime
import googlemaps
import math


# Create your views here.
def index(request):
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
    bad_data = cookies.get('bad_data_inc', "true")

    with open(settings.BASE_DIR + '/homepage' + settings.STATIC_URL +
              'RRP_timestamp.txt',
              'r') as file:
        lu = file.read()

    database_list = Sale.objects.aggregate(Max('price'), Count('price'))
    max_price = database_list['price__max']

    context = {'last_update': lu, 'max_price': max_price}

    if calcArea == 'map':

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

            ed_list = []

            for ed in eds_to_use:
                try:
                    ref = CSORef.objects.filter(desc=ed[0])[0].uid
                    ed_list.append([ref, ed[1]])
                except:
                    continue

            context['dom_ed'] = max(ed_count, key=ed_count.get)
            context['n_ed'] = len(ed_count)
    elif calcArea == 'radius':
        c_lat = (top - bottom) / 2 + bottom
        c_lng = (left - right) / 2 + right

        right = latlng(c_lat, c_lng, radius, 'E')[1]
        left = latlng(c_lat, c_lng, radius, 'W')[1]
        top = latlng(c_lat, c_lng, radius, 'N')[0]
        bottom = latlng(c_lat, c_lng, radius, 'S')[0]

        ed_data = Sale.objects.filter(quality='good', nfma='No').filter(
            latitude__gte=bottom, latitude__lte=top, longitude__gte=left,
            longitude__lte=right)

        if len(ed_data) == 0:
            context['dom_ed'] = 'Not Applicable'
            context['n_ed'] = 0
        else:

            c_lat = (top - bottom) / 2 + bottom
            c_lng = (left - right) / 2 + right
            ed_count = {}

            for sale in ed_data:
                lat = float(sale.latitude)
                lng = float(sale.longitude)

                if distance(c_lat, c_lng, lat, lng) <= float(radius):
                    if sale.ed in ed_count.keys():
                        ed_count[sale.ed] += 1
                    else:
                        ed_count[sale.ed] = 1

            eds_to_use = []
            for k, v in ed_count.items():
                if v > max(ed_count.values()) / 3:
                    eds_to_use.append([k, v])

            ed_list = []

            for ed in eds_to_use:
                try:
                    ref = CSORef.objects.filter(desc=ed[0])[0].uid
                    ed_list.append([ref, ed[1]])
                except:
                    continue

            context['dom_ed'] = max(ed_count, key=ed_count.get)
            context['n_ed'] = len(ed_count)

    return render(request, 'tableview/index.html', context)


def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - math.cos((lat2 - lat1) * p) / 2 + \
        math.cos(lat1 * p) * math.cos(lat2 * p) * \
        (1 - math.cos((lon2 - lon1) * p)) / 2

    return 12742 * math.asin(math.sqrt(a))


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


def ajax_response_table(request):

    calcArea = request.GET['calcArea']
    length = int(request.GET['length'])
    order = request.GET['order']
    sort = request.GET['sort']
    price_high = int(request.GET['ph'])
    price_low = int(request.GET['pl'])
    date_min = int(request.GET['dl'])
    date_max = int(request.GET['dh'])
    offset = int(request.GET['offset']) - 1
    dh = datetime.datetime.fromtimestamp(date_max / 1000)
    dl = datetime.datetime.fromtimestamp(date_min / 1000)

    start = (offset * length)
    end = start + length

    goodlist = []

    if calcArea == 'map':
        right = float(request.GET['r'])
        left = float(request.GET['l'])
        top = float(request.GET['t'])
        bottom = float(request.GET['b'])

        data = Sale.objects.filter(quality='good').filter(
            latitude__gte=bottom, latitude__lte=top, longitude__gte=left,
            longitude__lte=right, price__lte=price_high, price__gte=price_low,
            sale_date__gte=dl, sale_date__lte=dh)

        if len(data) == 0:
            return HttpResponse("Not Enough Data")

        for sale in data:
            goodlist.append([float(sale.latitude), float(sale.longitude)])

        total_length = len(data)

        if order == 'asc':
            data = data.order_by(sort)[start:end]
        else:
            data = data.order_by('-' + sort)[start:end]

    elif calcArea == 'radius':
        right = float(request.GET['r'])
        left = float(request.GET['l'])
        top = float(request.GET['t'])
        bottom = float(request.GET['b'])
        radius = float(request.GET['radius'])

        c_lat = (top - bottom) / 2 + bottom
        c_lng = (left - right) / 2 + right

        right = latlng(c_lat, c_lng, radius, 'E')[1]
        left = latlng(c_lat, c_lng, radius, 'W')[1]
        top = latlng(c_lat, c_lng, radius, 'N')[0]
        bottom = latlng(c_lat, c_lng, radius, 'S')[0]

        data = Sale.objects.filter(quality='good', nfma='No').filter(
            latitude__gte=bottom, latitude__lte=top, longitude__gte=left,
            longitude__lte=right, price__lte=price_high, price__gte=price_low,
            sale_date__gte=dl, sale_date__lte=dh)

        if len(data) == 0:
            return HttpResponse("Not Enough Data")

        if order == 'asc':
            data = data.order_by(sort)
        else:
            data = data.order_by('-' + sort)

        rdata = []

        for sale in data:
            lat = float(sale.latitude)
            lng = float(sale.longitude)

            if distance(c_lat, c_lng, lat, lng) <= radius:
                rdata.append(sale)
                goodlist.append([lat, lng])

        if len(rdata) == 0:
            return HttpResponse("Not Enough Data")

        total_length = len(rdata)

        data = rdata[start:end]
    elif calcArea == 'county':
        county = request.GET['areaSecond'].capitalize()
        bad_data = request.GET['bad_data']

        if bad_data == 'true':
            data = Sale.objects.filter(nfma='No', price__lte=price_high,
                                       price__gte=price_low,
                                       sale_date__gte=dl, sale_date__lte=dh,
                                       county=county)
        else:
            data = Sale.objects.filter(quality='good', nfma='No',
                                       price__lte=price_high,
                                       price__gte=price_low,
                                       sale_date__gte=dl, sale_date__lte=dh,
                                       county=county)

        if len(data) == 0:
            return HttpResponse("Not Enough Data")

        for sale in data:
            goodlist.append([float(sale.latitude), float(sale.longitude)])

        total_length = len(data)

        if order == 'asc':
            data = data.order_by(sort)[start:end]
        else:
            data = data.order_by('-' + sort)[start:end]

    elif calcArea == 'region':
        region = request.GET['areaSecond'].capitalize()

        bad_data = request.GET['bad_data']

        if bad_data == 'true':
            data = Sale.objects.filter(nfma='No', price__lte=price_high,
                                       price__gte=price_low,
                                       sale_date__gte=dl,
                                       sale_date__lte=dh, region=region)
        else:
            data = Sale.objects.filter(quality='good', nfma='No',
                                       price__lte=price_high,
                                       price__gte=price_low,
                                       sale_date__gte=dl, sale_date__lte=dh,
                                       region=region)

        if len(data) == 0:
            return HttpResponse("Not Enough Data")

        total_length = len(data)

        if order == 'asc':
            data = data.order_by(sort)[start:end]
        else:
            data = data.order_by('-' + sort)[start:end]

    elif calcArea == 'country':
        bad_data = request.GET['bad_data']

        if bad_data == 'true':
            data = Sale.objects.filter(nfma='No', price__lte=price_high,
                                       price__gte=price_low,
                                       sale_date__gte=dl, sale_date__lte=dh)
        else:
            data = Sale.objects.filter(quality='good', nfma='No',
                                       price__lte=price_high,
                                       price__gte=price_low,
                                       sale_date__gte=dl, sale_date__lte=dh)

        if len(data) == 0:
            return HttpResponse("Not Enough Data")

        total_length = len(data)

        if order == 'asc':
            data = data.order_by(sort)[start:end]
        else:
            data = data.order_by('-' + sort)[start:end]

    final_data = {}
    for i in range(len(data)):
        final_data[i] = {'price': int(data[i].price),
                         'address': data[i].address,
                         'sale_date': str(data[i].sale_date),
                         'postcode': data[i].postcode,
                         'county': data[i].county,
                         'nfma': data[i].nfma, 'vat_ex': data[i].vat_ex,
                         'dop': data[i].DoP, 'size': data[i].PSD,
                         'ed': data[i].ed}
    final_data['results'] = total_length
    final_data['points'] = goodlist

    return HttpResponse(json.dumps(final_data))


def geolocate(address_string):
    """
    Take address from search bar and return lat & long location if possible.
    :param address_string:
    :return: location, status

    Shorthand for status:
    0 - No search conducted
    1 - Good search results
    2 - Bad / No results
    """
    gmaps = googlemaps.Client(key='AIzaSyBFwN-7_erzpXeWWFe3DwMqSPKGoCjj1Hg')

    # Add Ireland to search string to remove ambiguity
    address = address_string + ' Ireland'

    # Get results from gmaps API
    geocode_result = gmaps.geocode(address)

    # If a result is returned
    if len(geocode_result) > 0:
        # Set the location as the result
        location = geocode_result[0]['geometry']['location']
        location['l'] = location['lng'] - 0.04866600036624025
        location['r'] = location['lng'] + 0.04866600036624025
        location['t'] = location['lat'] + 0.019106276426853697
        location['b'] = location['lat'] - 0.019106276426853697
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
        location = {'lng': -6.2603, 'lat': 53.3498, 'l': -6.30896600036624,
                    'r': -6.211633999633818, 't': 53.368906276426856,
                    'b': 53.330685156427386}

    return location, status


def ajax_response_map(request):

    search_address = request.POST['address']

    loc, stat = geolocate(search_address)

    final_data = {'status': stat, 'location': loc}

    return HttpResponse(json.dumps(final_data))
