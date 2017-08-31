import pandas as pd
import re


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
    orig_data = pd.read_csv('good_data.csv', encoding='latin1', index_col=0)
    orig_data['price'].apply(pd.to_numeric)
    orig_data['sale_date'] = pd.to_datetime(orig_data['sale_date'])
    print("Orig data ed size: ", len(orig_data.index))

    daft_data = pd.read_csv('good_scrape_data.csv', encoding='latin1')
    daft_data['price'].apply(pd.to_numeric)
    daft_data['sale_date'] = pd.to_datetime(daft_data['sale_date'])
    print("Daft data size: ", len(daft_data.index))

    df = pd.merge(daft_data, orig_data, how='inner', on=['sale_date', 'price', 'latitude', 'longitude'])

    print("Post Merge: ", len(df.index))
    df = df.drop_duplicates()
    print("Duplicates removed: ", len(df.index))
    df = df.drop(df[df['nfma_x'] == 'Yes'].index)
    df = df.drop(df[df['vat_ex'] == 'Yes'].index)

    good_cols = ['sale_date', 'address_x', 'county_x', 'price', 'DOP', 'bed', 'bath',
    'PSD', 'latitude','longitude', 'DoP', 'PSD', 'region']

    df = df.drop([i for i in df.columns if i not in good_cols], axis='columns')
    df.columns = ['sale_date', 'address', 'county', 'price', 'desc', 'bed', 'bath', 'latitude', 'longitude',
                  'condition', 'size', 'region']

    apt_pattern = re.compile(r'\b[Aa]pt\.?\b|\b[Aa]partment\b')
    hn_pattern = re.compile(r'[0-9]+')

    df['apt'] = df.address.apply(lambda x: 'Yes' if len(re.findall(apt_pattern, x)) > 0 else 'No')
    df['house_name'] = df.address.apply(lambda x: 'Yes' if len(re.findall(hn_pattern, x)) == 0 else 'No')

    df['address_sans_no'] = df.address.str.replace('\d+', '')
    df['address_sans_no'] = df['address_sans_no'].apply(lambda x: x.lower())
    df['address_sans_no'] = df['address_sans_no'].str.replace(',', '')

    df['suffix'] = df['address_sans_no'].apply(lambda x: word_isolation(x)).apply(lambda x: word_map(x))
    df['suffix'].fillna('None', inplace=True)
    df = df.drop(['address_sans_no'], axis='columns')

    print(len(df.index))
    print(df.columns)
    print(df.info())

    df.to_csv('model_data.csv')

if __name__ == '__main__':
    main()