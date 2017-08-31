"""
Desciption Required
"""

import pandas as pd
import re

# Function to return suffix from address, if one is present
def word_isolation(string):
    keep_words = ['road', 'park', 'avenue', 'court', 'rd', 'street', 'drive', 'st',
                  'grove', 'manor', 'close', 'green', 'view', 'hill', 'house', 'the',
                  'wood', 'terrace', 'heights', 'hall', 'mount', 'grange',
                  'lodge', 'lane', 'main', 'place', 'lawn', 'ave', 'square', 'dr',
                  'estate', 'woodlands', 'harbour', 'quay', 'bay', 'apt', 'sq', 'apartment']
    words = string.split()
    for word in words:
        if word in keep_words:
            return word


# Function to merge suffix abbreviations
def word_map(string):
    if string == 'st':
        return 'street'
    elif string == 'rd':
        return 'road'
    elif string == 'ave':
        return 'avenue'
    elif string == 'dr':
        return 'drive'
    elif string == 'apt':
        return 'apartment'
    elif string == 'sq':
        return 'square'
    else:
        return string


def main():
    # Import geocoded PPR data
    orig_data = pd.read_csv('good_data.csv', encoding='latin1', index_col=0)

    # Update price and date datatypes
    orig_data['price'].apply(pd.to_numeric)
    orig_data['sale_date'] = pd.to_datetime(orig_data['sale_date'])

    # Import geocoded scraped data
    scrape_data = pd.read_csv('good_scrape_data.csv', encoding='latin1')

    # Update price and date datatypes
    scrape_data['price'].apply(pd.to_numeric)
    scrape_data['sale_date'] = pd.to_datetime(scrape_data['sale_date'])

    # Merge both data sets
    df = pd.merge(scrape_data, orig_data, how='inner', on=['sale_date', 'price', 'latitude', 'longitude'])

    # Drop exact duplicates
    df = df.drop_duplicates()

    # Remove properties marked as not full market price and houses exclusive of VAT
    df = df.drop(df[df['nfma_x'] == 'Yes'].index)
    df = df.drop(df[df['vat_ex'] == 'Yes'].index)

    # List of columns required for model
    good_cols = ['sale_date', 'address_x', 'county_x', 'price', 'DOP', 'bed', 'bath',
    'PSD', 'latitude','longitude', 'DoP', 'PSD', 'region']

    # Drop unnecessary columns
    df = df.drop([i for i in df.columns if i not in good_cols], axis='columns')

    # Rename columns
    df.columns = ['sale_date', 'address', 'county', 'price', 'desc', 'bed', 'bath', 'latitude', 'longitude',
                  'condition', 'size', 'region']

    # Regular Expression patterns to isolate apartment and house name features
    apt_pattern = re.compile(r'\b[Aa]pt\.?\b|\b[Aa]partment\b')
    hn_pattern = re.compile(r'[0-9]+')
    df['apt'] = df.address.apply(lambda x: 'Yes' if len(re.findall(apt_pattern, x)) > 0 else 'No')
    df['house_name'] = df.address.apply(lambda x: 'Yes' if len(re.findall(hn_pattern, x)) == 0 else 'No')

    # Processing required to isolate house suffix
    df['address_sans_no'] = df.address.str.replace('\d+', '')
    df['address_sans_no'] = df['address_sans_no'].apply(lambda x: x.lower())
    df['address_sans_no'] = df['address_sans_no'].str.replace(',', '')
    df['suffix'] = df['address_sans_no'].apply(lambda x: word_isolation(x)).apply(lambda x: word_map(x))
    df['suffix'].fillna('None', inplace=True)
    df = df.drop(['address_sans_no'], axis='columns')

    # Export final model to CSV
    df.to_csv('model/model_data.csv')

if __name__ == '__main__':
    main()