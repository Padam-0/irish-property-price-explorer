"""
Checks last updated timestamp on RPPR and downloads if that is different to
timestamp stored on file
"""

from urllib.request import urlopen
import re
import pandas as pd
import zipfile
import wget
import os


def get_local_timestamp():
    with open('../../prac/homepage/static/RRP_timestamp.txt', 'r') as file:
        return file.read()


def update_raw_data(last_updated):
    """
    Queries the RPPR website to identify if new data has been updated since
    last searched. If new data exists, it is downloaded and returned,
    along with the timestamp for the new data.

    :param last_updated:
    :return: updated (Boolean), new_data (DataFrame),
        new_last_updated (String)
    """

    # Retrieve html from site
    html = urlopen('https://www.propertypriceregister.ie/website/npsra'
                   '/pprweb.nsf/page/ppr-home-en').read()

    # Compile regex to search for timestamp
    luPattern = re.compile(b'id="LastUpdated"(.{20})', flags=re.IGNORECASE)

    # Retrieve Last Updated timestamp
    new_last_updated = re.findall(luPattern, html)[0][1:].decode("utf-8")

    # If there is new data since previous search:
    if last_updated != new_last_updated:
        # Compile regex to search for download filename
        dfPattern = re.compile(b'(href="/website/npsra/ppr/npsra-ppr.nsf/'
                               b'Downloads/.+\.zip")', flags=re.IGNORECASE)

        # Retrieve filename and prepend domain information
        download_file = 'https://www.propertypriceregister.ie' + \
            re.findall(dfPattern, html)[0][6:-1].decode("utf-8")

        # Get current files in directory
        files = set([f for f in os.listdir('.')])

        # Download file as data.zip
        wget.download(download_file, 'data.zip')

        # Unzip and extract csv data
        zip_ref = zipfile.ZipFile('data.zip', 'r')
        zip_ref.extractall()
        zip_ref.close()

        # Find new files after download and extraction
        new_files = set([f for f in os.listdir('.')]) - files
        # Find extracted data filename as new_data
        raw_data = [f for f in new_files if f != 'data.zip'][0]

        # Read raw data into DataFrame
        new_data = pd.read_csv(raw_data, encoding='latin1')

        # Delete temp files for housekeeping
        os.remove("data.zip")
        os.remove(raw_data)

        # Return data and new last updated timestamp
        return True, new_data, new_last_updated

    else:
        return False, None, None


def main():

    update = update_raw_data(get_local_timestamp())
    if update[0]:
        data = update[1]

        # Start data preprocessing pipeline here

        with open('./temp/RRP_timestamp.txt', 'w') as file:
            file.write(update[2])


if __name__ == '__main__':
    main()
