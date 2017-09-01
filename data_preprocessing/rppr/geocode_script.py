#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import googlemaps
import time
import datetime


def check_null(address, pc, county):
    sa = address

    if not pd.isnull(pc):
        sa += ', ' + pc

    if not pd.isnull(county):
        sa += ', ' + county

    sa += ', Ireland'

    return sa

# This function takes an address and submits it to the Google Maps Api
# A latitude and longitude is returned if found in the Google DB
# Nothing is returned if not
def get_loc(sa, row, key):
    gmaps = googlemaps.Client(key=key)

    try:
        geocode_result = gmaps.geocode(sa)
        key_status = False
    except Exception as e:
        if str(e) == 'HTTP Error: 400':
            geocode_result = ""
            key_status = False
        else:
            geocode_result = ""
            key_status = True

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
        return True, location['lat'], location['lng'], key_status
    else:
        return False, None, None, key_status


# This function maps counties to their respective provence

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


# This function checks the existing geocoded and non geocoded files and returns the next non processed
# row to be processed
def find_next_row_to_process(df, good_output_filename, bad_output_filename):
    good = pd.read_csv(good_output_filename, encoding='latin1', index_col=0)
    bad = pd.read_csv(bad_output_filename, encoding='latin1', index_col=0)

    for row in df.index:
        if (row not in good.index) and (row not in bad.index):
            return row


def main():
    # API keys (First two are Pete's, second two are Andy's, key0 - Another of Andy's key)
    key1 = 'Enter Google API Key'
    key2 = 'Enter Google API Key'
    key3 = 'Enter Google API Key'
    keys = [key1, key2, key3]

    # Output filenames
    good_output_filename = "./geocoded_data.csv"
    bad_output_filename = "./nongeocoded_data.csv"

    # Import data
    df = pd.read_csv('../../Data/PPR-ALL-UIdentifier.csv', encoding='latin1', index_col=0)

    # Remove euro symbol from price column
    df['price'] = df['Price (Â\x80)'].map(lambda x: x.lstrip('Â').replace(',','')).astype(float)

    # For loop to cycle through each Google API Key
    for key in keys:
        key_status = False

        # Number of minutes to pause script between keys
        BACKOFF_TIME = 1
        if key != key1:
            time.sleep(BACKOFF_TIME*60)
        counter = 0


        while key_status == False:
            # This function finds the next row in the data set to process
            row = int(find_next_row_to_process(df, good_output_filename, bad_output_filename))

            # Print the row currently being processed and the count of rows already processed with this key
            counter += 1
            print("Row: ", row, " - ", counter)

            # Isolate all data points from row
            DOS = df.ix[row, :][0]
            address = df.ix[row, :][1]
            pc = df.ix[row, :][2]
            county = df.ix[row, :][3]
            price = float(df.ix[row, :][4][2:].replace(',', ''))
            nfmp = df.ix[row, :][5]
            vat_ex = df.ix[row, :][6]
            DOP = df.ix[row, :][7]
            PSD = df.ix[row, :][8]

            # Return provence associated with property
            region = get_region(county)

            # Restructure the address, adding postcode and county
            sa = check_null(address, pc, county)

            # Use Google API to get latitude and longitude information, if possible
            location, lat, long, key_status = get_loc(sa, row, key)

            # Write all property information to new files, split based on whether they have a longitude
            # and latitude or not
            if key_status == False:
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
