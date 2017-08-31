"""
Matches townlands.ie electoral district names to CSO electoral district names
"""

import pandas as pd
import difflib

with ('tl_ed_names.txt', 'r') as file:
    tl_eds = file.read()

tl_eds = set(tl_eds)

df = pd.read_csv('AllThemesTablesED.csv')

s = df['GEOGDESC'].value_counts()

dup_list = list(s[s > 1].index)

cso_eds = list(s.index)

# keys: townlands ed names, values: CSO ed names
with ('cross_ref_dict.txt', 'r') as file:
    cross_ref_dict = exec(file.read())

cso_names = []
tl_names = []

for i in range(len(tl_names)):
    cross_ref_dict[tl_names[i]] = cso_names[i]

matched_list = []
rej_list_cso = []
rej_list_tl = []

count = 0
for ed in cso_eds:
    if ed not in cross_ref_dict.values():
        rej_list_cso.append(ed)

for ed in tl_eds:
    if ed not in cross_ref_dict.keys():
        rej_list_tl.append(ed)

remove_list = ['Faithlegg (Part Rural)', 'Knockdrim', 'Eanach Dhúin',
               'Kilraghtis', 'Domhnach Phádraig', 'Doire Fhíonáin', 'Cordal',
               'Conga', 'Ceathrú an Bhrúnaigh (Part Rural)', 'Graigue Rural',
               'Cill Chuimín', 'Cill Chuimin', 'Cill Charthaigh',
               'Cill Bhríde', 'Béal Átha an Ghaorthaidh', 'Killogilleen',
               'Carraig Airt', 'Carragh', 'Bearna (Part Rural)', 'Bearna',
               'Ballynakill (Part Rural)', 'Ballybricken West',
               'Baile an Teampaill (Part Rural)', 'Ardfert', 'An tImleach',
               'An Turlach', 'An Tearmann', 'An Sráidbhaile', 'An Ráth Mhór',
               'Aird Mhór', 'An Baile Breac', 'An Baile Dubh', 'An Corrán',
               'An Daingean', 'An Fhairche', 'An Rinn', 'An Ros', 'Grianfort',
               'Mín an Lábáin', 'Rosbercon Rural', 'Kilbarry (Part Rural)',
               'Partraí', "St. Mary's (Part Rural)",
               "St. Mary's (Part Urban)", 'Leitir Móir', 'Meathas Truim',
               'Noughaval / Castletown']

print(len(remove_list))
print(cross_ref_dict)


options = 0
for ed in rej_list_cso:

    matches = difflib.get_close_matches(ed, possibilities=tl_eds, n=5)

    if len(matches) > 0:
        a = int(input(ed + ' : ' + str(matches)))
        if a == 6:
            continue
        else:
            cross_ref_dict[matches[a]] = ed
            tl_eds.remove(matches[a])
