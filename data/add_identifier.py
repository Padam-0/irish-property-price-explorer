import pandas as pd


def main():
    df = pd.read_csv('PPR-ALL.csv', encoding='latin1')
    df['UIdentifier'] = df.index + 1

    cols = list(df)
    cols.insert(0, cols.pop(cols.index('UIdentifier')))
    df = df.ix[:, cols]

    df.to_csv("PPR-ALL-UIdentifier.csv", index=False)

if __name__ == '__main__':
    main()