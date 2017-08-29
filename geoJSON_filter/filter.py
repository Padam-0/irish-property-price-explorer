# Loops through features in a geoJSON file, extracts and saves as their own
# files

import json

with open('./ireland/eds.geojson') as json_data:
    d = json.load(json_data)

header = '{"type":"FeatureCollection","geocoding":{"creation_date":"2016-10-12","generator":{"author":{"name":"Mapzen"},"package":"fences-builder","version":"0.1.2"},"license":"ODbL (see http://www.openstreetmap.org/copyright)"},"features":['

for feature in range(len(d['features'])):
    try:
        name = d['features'][feature]['properties']["NAME_TAG"].lower()
        county = d['features'][feature]['properties']["CO_NAME"].lower()
    except:
        print(d['features'][feature]['properties']["NAME_TAG"])
        county = input("What county is this in?").lower()
    #print(name, county)
    #[1].lower()
    try:
        with open('../prac/homepage/static/homepage/ireland/neighbourhoods/' +
                          str(name) + '_' + str(county) +
                          '.geojson', 'w') as file:
            file.write("".join([header, str(d['features'][feature]).replace(
                "\'","\""), ']}']))
    except:
        pass