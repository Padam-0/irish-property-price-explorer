import pandas as pd
import numpy as np
import json


with open('eds100.geojson') as f:
    eds = json.load(f)

features = []

for feature in eds['features']:
    f_data = {'geometry': feature['geometry'], 'type': 'Feature'}
    f_data['properties'] = {'uid': 'E' + feature['properties']['CSOED_3409']}

    features.append(f_data)


with open('eds.js', 'w') as f:
    f.write("var ed_data = {'type':'FeatureCollection','features':")
    f.write(str(features).replace('None', "'None'"))
    f.write('};')

cso_ref = pd.read_csv('cso_ref.csv', index_col=1)[['desc']]
print(cso_ref.to_dict()['desc'])

with open('cso_prov.geojson') as f:
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

with open('country.geojson') as f:
    irl = json.load(f)

features = []

f_data = {'geometry': irl['geometry'], 'type': 'Feature'}
f_data['properties'] = {'name': 'Ireland'}

with open('country.js', 'w') as f:
    f.write("var irl_data = {'type':'FeatureCollection','features':")
    f.write(str(f_data).replace('None', "'None'"))
    f.write('};')

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