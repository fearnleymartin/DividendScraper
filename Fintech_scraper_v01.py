import os

import requests
import pandas as pd
from bs4 import BeautifulSoup



# constants (Don't modify)
base_url = 'https://sifted.eu/european-fintech-startups/'
excel_filepath = 'fintech.csv'
excel_filepath_xlsx = 'fintech.xlsx'


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
   
    # get stage
    Fintech_stage_table = soup.find_all("div",attrs={"class": "sifted-tile-table__item sifted-tile-table__item"})
    fintech_stage_list = []
    for stage in Fintech_stage_table:
        Children =stage.findChildren("span",recursive=False)
        if "Stage" in Children[0].get_text():
            # print(Children[1].get_text())
            fintech_stage_list.append(Children[1].get_text())

    # get year
    Fintech_year_table = soup.find_all("div",attrs={"class": "sifted-tile-table__item sifted-tile-table__item"})
    fintech_year_list = []
    for year in Fintech_year_table:
        Children =year.findChildren("span",recursive=False)
        if "Founded" in Children[0].get_text():
            # print(Children[1].get_text())
            fintech_year_list.append(Children[1].get_text())

    # get location
    Fintech_location_table = soup.find_all("p", attrs={"class": "infotab"})
    fintech_location_list = []
    for location in Fintech_location_table:
        Children=location.findChildren("span",recursive=False)
        if "icon-location" in Children[0]['class']:
            #print(location.get_text())
            fintech_location_list.append(location.get_text())

    # get valuation
    Fintech_valuation_table = soup.find_all("div",attrs={"class": "sifted-tile-table__item sifted-tile-table__item"})
    fintech_valuation_list = []
    for valuation in Fintech_valuation_table:
        Children =valuation.findChildren("span",recursive=False)
        if "Valuation" in Children[0].get_text():
            # print(Children[1].get_text())
            fintech_valuation_list.append(Children[1].get_text())

 # get links
    Fintech_links_table = soup.find_all("p", attrs={"class": "infotab"})
    fintech_links_list = []
    for links in Fintech_links_table:
        Children=links.findChildren("span",recursive=False)
        if "icon-link" in Children[0]['class']:
            #print(links.get_text())
            fintech_links_list.append(links.get_text())

 # get overview
    Fintech_overview_table = soup.find_all("div",attrs={"class": "sifted-tile-table__item"})
    fintech_overview_list = []
    for overview in Fintech_overview_table:
        Children =overview.findChildren("span",recursive=False)
        if "Overview" in Children[0].get_text():
            # print(Children[1].get_text())
            fintech_overview_list.append(Children[1].get_text())
            
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
