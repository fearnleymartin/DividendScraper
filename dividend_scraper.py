import requests
import pandas as pd
from bs4 import BeautifulSoup

# Parameters (You can modify these)
dates = ['20200803', '20200804']
ftse = 1  # 1 for ftse 100, 2 for ftse 250

dividend_keywords = ['dividend']
interim_dividend_keywords = ['interim dividend']
buyback_keywords = [
    'buyback',
    'buy back',
    'purchase',
    'purchases',
    'repurchase',
    'repurchases',
    'own shares',
]

# constants (Don't modify)
base_url = 'https://www.investegate.co.uk'
excel_filepath = f'dividends_{str.join("_",dates)}_{"ftse100" if ftse == 1 else "ftse250"}.csv'
excel_filepath_xlsx = f'dividends_{str.join("_",dates)}_{"ftse100" if ftse == 1 else "ftse250"}.xlsx'


def get_ftse_table(dates):
    print("Getting table of ftse companies...")
    tables = []
    for date in dates:
        print(f"Processing date {date}")
        table = get_ftse_table_per_date(date)

        tables.append(table)
    print("Finished getting table of ftse companies.")
    return pd.concat(tables)


def get_ftse_table_per_date(date):
    start_url = f'{base_url}/Index.aspx?ftse={ftse}&date={date}&limit=-1'
    r = requests.get(start_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    announcement_list_table = soup.find(id='announcementList')

    data = []
    rows = announcement_list_table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        # cols = [ele.text.strip() for ele in cols]
        cols = [ele.text.strip() for ele in cols] + [(base_url + ele.a.get('href')) if ele.a else '' for ele in cols if ele][-1:]
        data.append([ele for ele in cols if ele]) # Get rid of empty values

    table = pd.DataFrame(data)
    table['Date'] = date
    columns = ['Time', 'Source', 'Company', 'Announcement', 'AnnouncementLink', 'Date']
    table.columns = columns
    table = table[['Date', 'Time', 'Source', 'Company', 'Announcement', 'AnnouncementLink']]
    table = table.dropna(subset=['Company'])
    return table


def check_companies(ftse_table: pd.DataFrame):
    print("Processing companies one by one...")
    contains_dividend_keywords = []
    contains_interim_dividend_keywords = []
    contains_buyback_keywords = []
    for row in ftse_table.iterrows():
        idx, series = row
        print(f'Processing {series["Company"]}...')
        check_companies_result = check_company(series['AnnouncementLink'])
        contains_dividend_keywords.append(check_companies_result['contains_dividend_keywords'])
        contains_interim_dividend_keywords.append(check_companies_result['contains_interim_dividend_keywords'])
        contains_buyback_keywords.append(check_companies_result['contains_buyback_keywords'])
    ftse_table['contains_dividend_keywords'] = contains_dividend_keywords
    ftse_table['contains_interim_dividend_keywords'] = contains_interim_dividend_keywords
    ftse_table['contains_buyback_keywords'] = contains_buyback_keywords
    ftse_table['contains_overall'] = ftse_table.apply(
        lambda row: row['contains_dividend_keywords'] or row['contains_interim_dividend_keywords'] or row['contains_buyback_keywords'], axis=1)
    print("Finished processing companies.")
    return ftse_table


def check_company(url, dividend_keywords=dividend_keywords, interim_dividend_keywords=interim_dividend_keywords, buyback_keywords=buyback_keywords):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    article_row = soup.findAll("div", {"class": "articleRow"})[0]
    text = article_row.get_text()
    # print(r)

    contains_dividend_keywords = False
    contains_interim_dividend_keywords = False
    contains_buyback_keywords = False

    for kw in dividend_keywords:
        if kw in text:
            contains_dividend_keywords = True
    for kw in interim_dividend_keywords:
        if kw in text:
            contains_interim_dividend_keywords = True
    for kw in buyback_keywords:
        if kw in text:
            contains_buyback_keywords = True

    return {
        'contains_dividend_keywords': contains_dividend_keywords,
        'contains_interim_dividend_keywords': contains_interim_dividend_keywords,
        'contains_buyback_keywords': contains_buyback_keywords
    }


def check_can_write_to_excel():
    try:
        open(excel_filepath, "r+")  # or "a+", whatever you need
    except IOError:
        raise IOError("Could not open file! Please close Excel!")


def main():
    print("Starting program...")
    check_can_write_to_excel()
    table = get_ftse_table(dates)
    table = check_companies(table)
    table.to_csv(excel_filepath)
    table.to_excel(excel_filepath_xlsx)
    print(table)
    print("Finished running.")


if __name__ == "__main__":
    main()
