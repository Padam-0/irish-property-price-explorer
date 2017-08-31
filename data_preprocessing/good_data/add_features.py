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

df = pd.read_csv('good_data_ed.csv', encoding='latin1')

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

df.to_csv('good_data_full_features.csv')