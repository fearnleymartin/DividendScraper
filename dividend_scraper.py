# download libraries#
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

# Parameters (You can modify these)
end_date = datetime.today()

ftse = 2  # 1 for ftse 100, 2 for ftse 250

# get a list of dates
dates=pd.bdate_range(end=end_date, periods=10).strftime('%Y%m%d').values.tolist()

# define keywords
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
suspension_keywords =['suspend','cancel']
reinstatement_keywords =['resume','resuming','resumption','reinstate','reinstating','reinstatement']

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
    contains_suspension_keywords = []
    contains_reinstatement_keywords = []
    dividend_keywords_text = []
    interim_dividend_keywords_text = []
    buyback_keywords_text = []
    suspension_keywords_text = []
    reinstatement_keywords_text = []
    count = 1
    total = len(ftse_table)
    for row in ftse_table.iterrows():
        idx, series = row
        print(f'Processing {series["Company"]} ({count}/{total})...')
        check_companies_result = check_company(series['AnnouncementLink'])
        contains_dividend_keywords.append(check_companies_result['contains_dividend_keywords'])
        contains_interim_dividend_keywords.append(check_companies_result['contains_interim_dividend_keywords'])
        contains_buyback_keywords.append(check_companies_result['contains_buyback_keywords'])
        contains_suspension_keywords.append(check_companies_result['contains_suspension_keywords'])
        contains_reinstatement_keywords.append(check_companies_result['contains_reinstatement_keywords'])
        dividend_keywords_text.append(check_companies_result['dividend_keywords_text'])
        interim_dividend_keywords_text.append(check_companies_result['interim_dividend_keywords_text'])
        buyback_keywords_text.append(check_companies_result['buyback_keywords_text'])
        suspension_keywords_text.append(check_companies_result['suspension_keywords_text'])
        reinstatement_keywords_text.append(check_companies_result['reinstatement_keywords_text'])
        count += 1
    ftse_table['contains_dividend_keywords'] = contains_dividend_keywords
    ftse_table['contains_interim_dividend_keywords'] = contains_interim_dividend_keywords
    ftse_table['contains_buyback_keywords'] = contains_buyback_keywords
    ftse_table['contains_suspension_keywords']=contains_suspension_keywords
    ftse_table['contains_reinstatement_keywords']=contains_reinstatement_keywords

    ftse_table['contains_overall'] = ftse_table.apply(
        lambda row: row['contains_dividend_keywords'] or row['contains_interim_dividend_keywords'] or row['contains_buyback_keywords'], axis=1)

    ftse_table['dividend_keywords_text'] = dividend_keywords_text
    ftse_table['interim_dividend_keywords_text'] = interim_dividend_keywords_text
    ftse_table['buyback_keywords_text'] = buyback_keywords_text
    ftse_table['suspension_keywords_text']=suspension_keywords_text
    ftse_table['reinstatement_keywords_text']=reinstatement_keywords_text

    print("Finished processing companies.")
    return ftse_table


def check_company(url, dividend_keywords=dividend_keywords, interim_dividend_keywords=interim_dividend_keywords, buyback_keywords=buyback_keywords, suspension_keywords=suspension_keywords, reinstatement_keywords=reinstatement_keywords):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    article_row = soup.findAll("div", {"class": "articleRow"})[0]
    text = article_row.get_text()
    # print(r)

    # variable initialisation
    contains_dividend_keywords = False
    contains_interim_dividend_keywords = False
    contains_buyback_keywords = False
    contains_suspension_keywords = False
    contains_reinstatement_keywords = False
    dividend_keywords_text = []
    interim_dividend_keywords_text = []
    buyback_keywords_text = []
    suspension_keywords_text = []
    reinstatement_keywords_text = []

    # Parse text and update variable if necessary
    for kw in dividend_keywords:
        if kw in text:
            contains_dividend_keywords = True
            dividend_keywords_text = parse_paragraph(text, kw)
    for kw in interim_dividend_keywords:
        if kw in text:
            contains_interim_dividend_keywords = True
            interim_dividend_keywords_text = parse_paragraph(text, kw)
    for kw in buyback_keywords:
        if kw in text:
            contains_buyback_keywords = True
            buyback_keywords_text = parse_paragraph(text, kw)

    for kw in suspension_keywords:
        if kw in text:
            contains_suspension_keywords = True
            suspension_keywords_text = parse_paragraph(text, kw)
    
    for kw in reinstatement_keywords:
        if kw in text:
            contains_reinstatement_keywords = True
            reinstatement_keywords_text = parse_paragraph(text, kw)    
            

    # Return result
    return {
        'contains_dividend_keywords': contains_dividend_keywords,
        'contains_interim_dividend_keywords': contains_interim_dividend_keywords,
        'contains_buyback_keywords': contains_buyback_keywords,
        'contains_suspension_keywords': contains_suspension_keywords,
        'contains_reinstatement_keywords': contains_reinstatement_keywords,
        'dividend_keywords_text': dividend_keywords_text,
        'interim_dividend_keywords_text': interim_dividend_keywords_text,
        'buyback_keywords_text': buyback_keywords_text,
        'suspension_keywords_text': suspension_keywords_text,
        'reinstatement_keywords_text':reinstatement_keywords_text
    }


def parse_paragraph(text, kw):
    return str.join('\n\n',[para.replace(kw, f'#####{kw}#####') for para in text.split("\n") if kw in para])


def check_can_write_to_excel():
    try:
        open(excel_filepath_xlsx, "r+")  # or "a+", whatever you need
    except IOError:
        if os.path.isfile(excel_filepath_xlsx):
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
