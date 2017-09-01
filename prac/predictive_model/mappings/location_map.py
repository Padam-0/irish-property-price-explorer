import pandas as pd

"""
City ED Source:

http://www.boundarycommittee.ie/reports/2013-Report.pdf
http://www.corkcity.ie/services/corporateandexternalaffairs/franchise/boundaryrevision/
"""

waterford_city = ['Ballymaclode', 'Ballynakill', 'Faithlegg', 'Farranshoneen', 'Grange South',
                  'Grange Upper', 'Killea', 'Kilmacleague', 'Newtown', 'Park', 'Rathmoylan', 'Woodstown',
                  'Ballybeg North', 'Ballybeg South', 'Ballynaneashagh', 'Ballytruckle', 'Custom House A',
                  'Drumcannon', 'Grange North', 'Kilbarry', 'Kingsmeadow', 'Larchville', 'Lisduggan',
                  'Mount Sion', 'Poleberry', 'Roanmore', 'Slievekeale', 'Ticor North', 'Ticor South',
                  'Ballybricken', 'Bilberry', 'Centre A', 'Centre B', 'Cleaboy', 'Custom House B', 'Ferrybank',
                  'Gracedieu', 'Islandikane', 'Killoteran', 'Military Road', "Morrisson's Avenue East", "Morrisson's"
                  'Avenue West', "Morrisson's Road", "Newport's Square", 'Pembrokestown', 'Shortcourse',
                  'The Glen', 'Tramore']

cork_city = ['Blackpool A', 'Blackpool B', 'Commons', 'Fair Hill A', 'Farranferris A', 'Farranferris C',
             'Gurranebraher A', 'Gurranebraher B', 'Gurranebraher C', 'Gurranebraher D', 'Gurranebraher E',
             'Shandon A', 'Shandon B', 'Sundays Well B', 'The Glen A', 'The Glen B', 'Mayfield', 'Montenotte A',
             'Montenotte B', "St. Patrick's A", "St. Patrick's B", "St. Patrick's C", 'Tivoli A', 'Tivoli B',
             'Churchfield', 'Fair Hill B', 'Fair Hill C', 'Farranferris B', 'Knocknaheeny', 'Shanakiel', 'Sundays Well A',
             'Ballyphehane A', 'Ballyphehane B', 'Centre A', 'Centre B', 'City Hall A', 'Evergreen', 'Gillabbey A',
             'Greenmount', 'Pouladuff A', 'Pouladuff B', 'South Gate A', 'South Gate B', 'The Lough', 'Togher B',
             'Turners Cross A', 'Turners Cross B', 'Turners Cross C', 'Turners Cross D', 'Ballinlough A', 'Ballinlough B',
             'Ballinlough C', 'Browningstown', 'City Hall B', 'Knockrea A', 'Knockrea B', 'Mahon A', 'Mahon B', 'Mahon C',
             'Tramore A', 'Tramore B', 'Tramore C', 'Bishopstown A', 'Bishopstown B', 'Bishopstown C', 'Bishopstown D',
             'Bishopstown E', 'Gillabbey B', 'Gillabbey C', 'Glasheen A', 'Glasheen B', 'Glasheen C', 'Mardyke', 'Togher A']

limerick_city = ['Abbey C', 'Abbey D', 'Ballysimon', 'Ballyvarra', 'Castleconnell', 'Galvone A', 'Galvone B',
                 'Glentworth A', 'Glentworth B', 'Glentworth C', 'Limerick South Rural', 'Market', 'Rathbane',
                 'Roxborough', 'Singland A', 'Singland B', 'St. Laurence', 'Abbey A', 'Abbey B', 'Ballynanty',
                 'Castle A', 'Castle B', 'Castle C', 'Castle D', 'Coolraine', 'Farranshone', "John's A", "John's B",
                 "John's C", 'Killeely A', 'Killeely B', 'Limerick North Rural', 'Ballinacurra A', 'Ballinacurra B',
                 'Ballycummin', 'Carrig', 'Clarina', 'Custom House', 'Dock A', 'Dock B', 'Dock C', 'Dock D',
                 'Patrickswell', 'Prospect A', 'Prospect B', 'Shannon A', 'Shannon B']

galway_city = ['Bearna', 'Claddagh', 'Cnoc na Cathrach', 'Rockbarton', 'Salthill', 'Taylors Hill'
               'Dangan', 'Eyre Square', 'Mionlach', 'Newcastle', 'Nuns Island', 'Rahoon', 'Shantalla',
               'Toghroinn San Niocláis', 'An Caisleán', 'Baile an Bhriotaigh', 'Ballybaan', 'Lough Atalia',
               'Mervue', 'Murroogh', 'Renmore', 'Wellpark']

cities = cork_city + waterford_city + limerick_city + galway_city

# Model data not available
df = pd.read_csv('../model_data.csv', index_col=0)

for index, row in df.iterrows():
    if row['county'] == 'Dublin':
        df.ix[index, 'model'] = 'Dublin'
    else:
        if row['ed'] in cities:
            df.ix[index, 'model'] = 'City'
        else:
            df.ix[index, 'model'] = 'Rural'

df.to_csv('../model_data_split.csv')

