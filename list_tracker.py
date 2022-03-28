import pandas as pd

SNP_CSV_FILENAME = "snp.csv"
URL_CSV_FILENAME = "urls.csv"

SYMBOL_KEY = "Symbol"
SECURITY_KEY = "Security"
DEF_14A_KEY = "DEF 14A Filed"
URL_KEY = "URL"


def copy_over_d14a_data(row: pd.Series, prev: pd.DataFrame):
    symbol = row[SYMBOL_KEY]
    prev_row_df: pd.DataFrame = prev.loc[prev[SYMBOL_KEY] == symbol]
    if len(prev_row_df) == 0:
        return row

    old_d14a_data = prev_row_df.iloc[0][DEF_14A_KEY]
    row[DEF_14A_KEY] = old_d14a_data
    return row


def update_urls_csv(snp500: pd.DataFrame):
    prev_urls = pd.read_csv(URL_CSV_FILENAME)
    urls = []
    for idx, series in snp500.iterrows():
        symbol = series[SYMBOL_KEY]
        security = series[SECURITY_KEY]
        prev_row_df = prev_urls.loc[prev_urls[SYMBOL_KEY] == symbol]
        old_url = prev_row_df.iloc[0][URL_KEY]
        urls.append({
            SYMBOL_KEY: symbol,
            SECURITY_KEY: security,
            URL_KEY: old_url
        })
    urls_df = pd.DataFrame(urls)
    urls_df.to_csv(URL_CSV_FILENAME, index=False)


def main():
    previous_snp500: pd.DataFrame = pd.read_csv(SNP_CSV_FILENAME)
    snp500: pd.DataFrame = pd.read_html(
        'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    snp500[DEF_14A_KEY] = None
    snp500 = snp500.apply(copy_over_d14a_data, args=(previous_snp500,), axis=1)

    changes_made = not previous_snp500.equals(snp500)
    if changes_made:
        snp500.to_csv(SNP_CSV_FILENAME, index=False)
        # Email


if __name__ == '__main__':
    main()
