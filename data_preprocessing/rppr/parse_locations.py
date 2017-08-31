import pandas as pd
import googlemaps
from tqdm import tqdm
import subprocess
import sys

def check_null(address, pc, county):
    sa = address

    if not pd.isnull(pc):
        sa += ', ' + pc

    if not pd.isnull(county):
        sa += ', ' + county

    sa += ', Ireland'

    return sa

def get_loc(sa):
    ### Petes Keys
    gmaps = googlemaps.Client(key='AIzaSyBFwN-7_erzpXeWWFe3DwMqSPKGoCjj1Hg')
    # gmaps = googlemaps.Client(key='AIzaSyCS2_nkFXNLvO5EdD0gAcxzTO5h35Z__L0')

    ### Andys Keys
    # gmaps = googlemaps.Client(key='AIzaSyDC3FZnGEFnDQZHEg1d5f9tKfPgFn3t8nU')
    # gmaps = googlemaps.Client(key='AIzaSyA7u79SHIkWqKmGdxIV6OMIaUah039dS8k')

    geocode_result = gmaps.geocode(sa)

    if len(geocode_result) > 0:
        # Set the location as the result
        location = geocode_result[0]['geometry']['location']
        status = True
    else:
        status = False

    # Check if location is within east/west boundary of Ireland
    if status is True:
        if location['lng'] > -10.738539 and location['lng'] < -5.930445:
            pass
        else:
            status = False

    # Check if location is within north/south boundary of Ireland
    if status is True:
        if location['lat'] > 51.387652 and location['lat'] < 55.445918:
            pass
        else:
            status = False

    if status is True:
        return True, location['lat'], location['lng']
    else:
        return False, None, None

def get_region(county):
    counties = {
        'Connacht': ['Galway', 'Leitrim', 'Mayo', 'Roscommon', 'Sligo'],
        'Leinster': ['Carlow', 'Dublin', 'Kildare', 'Kilkenny', 'Laois',
                     'Longford', 'Louth', 'Meath', 'Offaly', 'Westmeath',
                     'Wexford', 'Wicklow'],
        'Munster': ['Clare', 'Cork', 'Kerry', 'Limerick', 'Tipperary',
                    'Waterford'],
        'Ulster': ['Antrim', 'Armagh', 'Cavan', 'Donegal', 'Down', 'Fermanagh',
                   'Londonderry', 'Monaghan', 'Tyrone']
    }
    for region, county_list in counties.items():
        if county in county_list:
            return region

    return None


def iden_match(df, good, bad):
    """
    This function cross references the good and bad data files with the PPR-ALL file and assigns
    a unique identifier to each address based on its corresponding line in the PPR-All file
    """

    for row in tqdm(good.index):
        DOS = good.ix[row, :][0]
        address = good.ix[row, :][1]
        price = good.ix[row, :][4]

        if (address in df.Address.values) and (DOS in df.loc[:,['Date of Sale (dd/mm/yyyy)']].values) and (price in df.price.values):
            good.ix[row, "UIdentifier"] = df.iloc[df.loc[df.Address == address].index, 0].values[0]
        else:
            good.ix[row, "UIdentifier"] = ""

    cols = list(good)
    cols.insert(0, cols.pop(cols.index('UIdentifier')))
    good = good.ix[:, cols]
    good = good.set_index(['UIdentifier'])
    good.to_csv('good_data_test.csv')

    for row in tqdm(bad.index):
        DOS = bad.ix[row, :][0]
        address = bad.ix[row, :][1]
        price = bad.ix[row, :][4]

        if (address in df.Address.values) and (DOS in df.loc[:,['Date of Sale (dd/mm/yyyy)']].values) and (price in df.price.values):
            bad.ix[row, "UIdentifier"] = df.iloc[df.loc[df.Address == address].index, 0].values[0]
        else:
            bad.ix[row, "UIdentifier"] = ""

    cols = list(bad)
    cols.insert(0, cols.pop(cols.index('UIdentifier')))
    bad = bad.ix[:, cols]
    bad = bad.set_index(['UIdentifier'])
    bad.to_csv('bad_data_test.csv')


def processed_check(df, good, bad):
    for row in tqdm(df.index):
        DOS = df.ix[row, :][1]
        address = df.ix[row, :][2]
        price = float(df.ix[row, :][5][2:].replace(',', ''))

        if (address in good.address.values) and (DOS in good.sale_date.values) and (price in good.price.values):
            df['Processed?'] = "Yes"
        elif(address in bad.address.values) and (DOS in bad.sale_date.values) and (price in bad.price.values):
            df['Processed?'] = "Yes"
        else:
            df['Processed?'] = "No"

    df.to_csv('PPR-ALL-Processed.csv')


def find_next_row_to_process(df):
    good = pd.read_csv('good_data.csv', encoding='latin1', index_col=0)
    bad = pd.read_csv('bad_data.csv', encoding='latin1', index_col=0)
    for row in df.index:
        if (row not in good.index) and (row not in bad.index):
            return row


def main():
    good_output_filename = "./good_data.csv"
    bad_output_filename = "./bad_data.csv"

    df = pd.read_csv('../../Data/PPR-ALL-UIdentifier.csv', encoding='latin1', index_col=0)
    df['price'] = df['Price (Â\x80)'].map(lambda x: x.lstrip('Â').replace(',','')).astype(float)

    counter = 0
    while counter < 1629:
        row = int(find_next_row_to_process(df))
        print("\nNext row to process", row)
        counter += 1
        print("Count: ", counter)
        DOS = df.ix[row, :][0]
        address = df.ix[row, :][1]
        pc = df.ix[row, :][2]
        county = df.ix[row, :][3]
        price = float(df.ix[row, :][4][2:].replace(',', ''))
        nfmp = df.ix[row, :][5]
        vat_ex = df.ix[row, :][6]
        DOP = df.ix[row, :][7]
        PSD = df.ix[row, :][8]
        region = get_region(county)
        sa = check_null(address, pc, county)
        location, lat, long = get_loc(sa)
        if location:
            with open(good_output_filename, "a") as file:
                file.write((str(row) + ',' + DOS + ',\"' + address + '\",' + str(pc) +
                            ',' + county + ',' + str(price) + ','
                            + str(nfmp) + ',' + str(vat_ex) + ','
                            + str(DOP) + ',' + str(PSD) + ',' +
                            str(region) + ',' + str(lat) + ',' + str(
                    long)).replace('nan', ''))
                file.write('\n')
        else:
            with open(bad_output_filename, "a") as file:
                file.write(
                    (str(row) + ',' + DOS + ',\"' + address + '\",' + str(pc) +
                     ',' + county + ',' + str(price) + ','
                     + str(nfmp) + ',' + str(vat_ex) + ','
                     + str(DOP) + ',' + str(PSD) + ',' +
                     str(region)).replace('nan', ''))
                file.write('\n')


if __name__ == "__main__":
    main()
