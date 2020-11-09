# importing libraries
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

# constants (Don't modify)
base_url = 'https://sifted.eu/european-fintech-startups/'
excel_filepath = 'fintech.csv'
excel_filepath_xlsx = 'fintech.xlsx'

# define the common function
def get_field_by_div(kw,soup):
    Fintech_table = soup.find_all("div", attrs={"class": "sifted-tile-table__item sifted-tile-table__item"})
    fintech_list = []
    for field in Fintech_table:
        Children = field.findChildren("span", recursive=False)
        if kw in Children[0].get_text():
            # print(Children[1].get_text())
            fintech_list.append(Children[1].get_text())
    return fintech_list

def get_field_by_p(kw,soup):
    Fintech_table = soup.find_all("p", attrs={"class": "infotab"})
    fintech_list = []
    for field in Fintech_table:
        Children = field.findChildren("span", recursive=False)
        if kw in Children[0]['class']:
            # print(field.get_text())
            fintech_list.append(field.get_text())
    return fintech_list

def get_fintech_list():
    start_url = base_url
    r = requests.get(start_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    
    # get names
    Fintech_names_table = soup.find_all("h1", attrs={"class": "sifted-tile__name"})
    fintech_names_list = []
    for name in Fintech_names_table:
        # print(name.get_text())
        fintech_names_list.append(name.get_text())

    # get overview
    Fintech_overview_table = soup.find_all("div", attrs={"class": "sifted-tile-table__item"})
    fintech_overview_list = []
    for overview in Fintech_overview_table:
        Children = overview.findChildren("span", recursive=False)
        if "Overview" in Children[0].get_text():
            # print(Children[1].get_text())
            fintech_overview_list.append(Children[1].get_text())
   
    # get stage
    fintech_stage_list = get_field_by_div("Stage", soup)

    # get year
    fintech_year_list = get_field_by_div("Founded", soup)

    # get valuation
    fintech_valuation_list = get_field_by_div("Valuation", soup)

    # get location
    fintech_location_list = get_field_by_p("icon-location", soup)

    # get links
    fintech_links_list = get_field_by_p("icon-link", soup)

    #define table
    table=pd.DataFrame()
    table["Name"]=fintech_names_list
    table["Overview"]=fintech_overview_list
    table["Stage"]=fintech_stage_list
    table["Founded"]=fintech_year_list
    table["Location"]=fintech_location_list
    table["Valuation"]=fintech_valuation_list
    table["Website"]=fintech_links_list
    
    return table

def check_can_write_to_excel():
    try:
        open(excel_filepath_xlsx, "r+")  # or "a+", whatever you need
    except IOError:
        if os.path.isfile(excel_filepath_xlsx):
            raise IOError("Could not open file! Please close Excel!")


def main():
    print("Starting program...")
    check_can_write_to_excel()
    table = get_fintech_list()
    #table = check_companies(table)
    table.to_csv(excel_filepath)
    table.to_excel(excel_filepath_xlsx)
    print(table)
    print("Finished running.")


if __name__ == "__main__":
    main()
