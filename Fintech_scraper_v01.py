# importing libraries
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

# constants (Don't modify)
base_url = 'https://sifted.eu/european-fintech-startups/'
excel_filepath = 'fintech.csv'
excel_filepath_xlsx = 'fintech.xlsx'

# define the common functions
def get_values_from_div_nodes(kw, soup):
    div_nodes = soup.find_all("div", attrs={"class": "sifted-tile-table__item sifted-tile-table__item"})
    values_list = []
    for div_node in div_nodes:
        children = div_node.findChildren("span", recursive=False)
        if kw in children[0].get_text():
            values_list.append(children[1].get_text())
    return values_list

def get_values_from_p_nodes(kw, soup):
    p_notes = soup.find_all("p", attrs={"class": "infotab"})
    values_list = []
    for div_node in p_notes:
        children = div_node.findChildren("span", recursive=False)
        if kw in children[0]['class']:
            values_list.append(div_node.get_text())
    return values_list

def get_fintech_list():
    start_url = base_url
    r = requests.get(start_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    
    # get names
    Fintech_names_table = soup.find_all("h1", attrs={"class": "sifted-tile__name"})
    fintech_names_list = []
    for name in Fintech_names_table:
        fintech_names_list.append(name.get_text())

    # get overview
    Fintech_overview_table = soup.find_all("div", attrs={"class": "sifted-tile-table__item"})
    fintech_overview_list = []
    for overview in Fintech_overview_table:
        children = overview.findChildren("span", recursive=False)
        if "Overview" in children[0].get_text():
            fintech_overview_list.append(children[1].get_text())
   
    # get stage
    fintech_stage_list = get_values_from_div_nodes("Stage", soup)

    # get year
    fintech_year_list = get_values_from_div_nodes("Founded", soup)

    # get valuation
    fintech_valuation_list = get_values_from_div_nodes("Valuation", soup)

    # get location
    fintech_location_list = get_values_from_p_nodes("icon-location", soup)

    # get links
    fintech_links_list = get_values_from_p_nodes("icon-link", soup)

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
