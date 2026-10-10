import re
import pandas as pd

USD_TO_INR = 100
CRORE = 10_000_000


def to_number(x):
    """'20,00,00,000' / '\\xc2\\xa05,000,000' / '14,342,000+' -> float, else NaN"""
    if pd.isna(x):
        return float('nan')
    x = str(x).replace('\\xc2\\xa0', '').replace('+', '')
    x = re.sub(r'[^\d.]', '', x)          # keep digits and dot only
    return float(x) if x else float('nan')


def clean(path='startup_funding.csv'):
    df = pd.read_csv(path, encoding='utf-8-sig')

    # 1. drop remark column
    df = df.drop(columns=['Remarks'])

    # 2. set index to sno
    df = df.set_index('Sr No')

    # 3. rename columns
    df.columns = ['date', 'startup', 'vertical', 'subvertical',
                  'city', 'investors', 'round', 'amount']
    df.index.name = 'sno'

    # 4. convert amount (USD) into INR crores
    df['amount'] = df['amount'].apply(to_number) * USD_TO_INR / CRORE

    # fix messy dates before parsing
    df['date'] = (df['date'].astype(str)
                  .str.replace('\\xc2\\xa0', '', regex=False)
                  .str.replace('.', '/', regex=False)
                  .str.replace('//', '/', regex=False))
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y', errors='coerce')

    # 5. drop na rows (rows missing key fields)
    df = df.dropna(subset=['date', 'startup', 'investors', 'vertical', 'city', 'round', 'amount'])

    # tidy text
    df['investors'] = df['investors'].str.replace('"', '', regex=False).str.strip()
    df['city'] = df['city'].str.strip()
    return df


if __name__ == '__main__':
    df = clean()
    df.to_csv('startup_cleaned.csv')
    print(df.shape)
    print(df.head())