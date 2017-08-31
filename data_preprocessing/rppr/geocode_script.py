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


def get_loc(sa, row, key, log_file, counter):
    gmaps = googlemaps.Client(key=key)

    try:
        geocode_result = gmaps.geocode(sa)
        key_status = False
    except Exception as e:
        if str(e) == 'HTTP Error: 400':
            log_file.write(" Error with row {}".format(row))
            geocode_result = ""
            key_status = False
        else:
            log_file.write(" Error with row {}".format(row))
            log_file.write(" Key complete for this period after {} requests".format(counter))
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


def find_next_row_to_process(df, counter, log_file):
    good = pd.read_csv('good_data.csv', encoding='latin1', index_col=0)
    bad = pd.read_csv('bad_data.csv', encoding='latin1', index_col=0)

    for row in df.index:
        if (row not in good.index) and (row not in bad.index):
            return row


def main():
    log_file = open('logfile.txt', 'a')
    log_file.write('\n')
    log_file.write('-------------')
    log_file.write('\n')
    log_file.write(str(datetime.datetime.now()))
    log_file.write('\n -------------')

    # API keys (First two are Pete's, second two are Andy's, key0 - Another of Andy's key)
    key0 = 'AIzaSyDfli3wnRWU6569PLU2CBsipyw3yM01Jqg'
    key1 =  'AIzaSyBFwN-7_erzpXeWWFe3DwMqSPKGoCjj1Hg'
    key2 = 'AIzaSyCS2_nkFXNLvO5EdD0gAcxzTO5h35Z__L0'
    key3 = 'AIzaSyDC3FZnGEFnDQZHEg1d5f9tKfPgFn3t8nU'
    key4 = 'AIzaSyA7u79SHIkWqKmGdxIV6OMIaUah039dS8k'
    keys = [key0, key1, key2, key3, key4]

    good_output_filename = "./good_data.csv"
    bad_output_filename = "./bad_data.csv"

    df = pd.read_csv('../../Data/PPR-ALL-UIdentifier.csv', encoding='latin1', index_col=0)
    df['price'] = df['Price (Â\x80)'].map(lambda x: x.lstrip('Â').replace(',','')).astype(float)

    for key in keys:
        print("\nCurrent Key: ", key)
        key_status = False
        BACKOFF_TIME = 1
        log_file.write('\n')
        log_file.write("Attempting key: {}".format(key))
        log_file.write('\n')
        if key != key0:
            time.sleep(BACKOFF_TIME*30)
        counter = 0
        while key_status == False:
            row = int(find_next_row_to_process(df, counter, log_file))
            counter += 1
            print("Row: ", row, " - ", counter)
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
            location, lat, long, key_status = get_loc(sa, row, key, log_file, counter)
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

                if counter % 100 == 0:
                    log_file.write("Completed {} of {} address".format(counter, 2500))
                    log_file.write('\n')


if __name__ == "__main__":
    main()
