"""
From CSO 100m Electoral district geojson files, strips out specific features
and saves them to discrete files.
"""

import pandas as pd
import json


def cso_tl_cross_reference_names():
    # Create a data frame that cross references the CSO electoral district ID
    # with the electoral district name

    with open('eds100.geojson') as f:
        eds = json.load(f)

    features = []

    for feature in eds['features']:
        f_data = {'geometry': feature['geometry'], 'type': 'Feature'}
        f_data['properties'] = {'uid': 'E' +
                                       feature['properties']['CSOED_3409']}

        features.append(f_data)

    with open('eds.js', 'w') as f:
        f.write("var ed_data = {'type':'FeatureCollection','features':")
        f.write(str(features).replace('None', "'None'"))
        f.write('};')

    # cso_ref = pd.read_csv('cso_ref.csv', index_col=1)[['desc']]
    # print(cso_ref.head())


def create_counties_subset():
    # Creates a static .js file with county boundary data to be displayed on
    # the front end

    with open('counties.geojson') as f:
        cou = json.load(f)

    features = []

    for feature in cou['features']:
        f_data = {'geometry': feature['geometry'], 'type': 'Feature'}
        f_data['properties'] = {'name': feature['name'].split(' ')[1]}

        features.append(f_data)

    with open('counties.js', 'w') as f:
        f.write("var cou_data = {'type':'FeatureCollection','features':")
        f.write(str(features).replace('None', "'None'"))
        f.write('};')


def create_regions_subset():
    # Creates a static .js file with region boundary data to be displayed on
    # the front end

    with open('regions_cso.geojson') as f:
        prov = json.load(f)

    features = []

    for feature in prov['features']:
        f_data = {'geometry': feature['geometry'], 'type': 'Feature'}
        f_data['properties'] = {'name': feature['properties']['PROVINCE']}

        features.append(f_data)

    with open('regions.js', 'w') as f:
        f.write("var prov_data = {'type':'FeatureCollection','features':")
        f.write(str(features).replace('None', "'None'"))
        f.write('};')


def create_country_subset():
    # Creates a static .js file with country boundary data to be displayed on
    # the front end

    with open('country_cso.geojson') as f:
        irl = json.load(f)

    f_data = {'geometry': irl['geometry'], 'type': 'Feature'}
    f_data['properties'] = {'name': 'Ireland'}

    with open('country.js', 'w') as f:
        f.write("var irl_data = {'type':'FeatureCollection','features':")
        f.write(str(f_data).replace('None', "'None'"))
        f.write('};')


def main():
    cso_tl_cross_reference_names()
    create_counties_subset()
    create_regions_subset()
    create_country_subset()


if __name__ == '__main__':
    main()
