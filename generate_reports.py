import os
import csv
from os import path
from bs4 import BeautifulSoup

import pandas as pd

# For each report we have a getpanchayatTup function which extracts data from html file
# For each report, we also have a createCSV function which helps us to extract the required columns and create the csv file 

years = ["2021-2022", "2022-2023", "2023-2024"]
savedhtml_lines = ['R111', 'R515', 'R141', 'R511', 'R721', 'R711'] 
output_dir = 'csv_files/'

# R 7.1.1
def getpanchayatTup711(fn, state, district, block): 
    with open(fn, encoding='utf-8') as file:  
        soup = BeautifulSoup(file, 'html.parser')

    data = []
    for row in soup.find_all("tr"):
        cols = row.find_all("td") 
        if len(cols) >= 23:  
            panchayat = cols[1].text.strip().lower()
            s1 = cols[9].text.strip()
            s2 = cols[10].text.strip()
            s3 = cols[11].text.strip()
            s4 = cols[12].text.strip()
            s5 = cols[15].text.strip() 
            data.append([state, district, block, panchayat, s1, s2, s3, s4, s5])
    return data[1:-1] 

# R 7.2.1
def getpanchayatTup721(fn, start_row, state, district, block): 
    with open(fn, encoding='utf-8') as file:  
        soup = BeautifulSoup(file, 'html.parser')
    panchayats = soup.findAll("tr")[start_row:-1]
    res = []
    for panchayat in panchayats:
        try:
            panchayat_element = panchayat.find('td').find_next_sibling("td")
            panchayat_name = panchayat_element.text.strip().lower()
            total_td_elements = panchayat.findAll('td')[2:]
            ls = [state, district, block, panchayat_name]
            for td_element in total_td_elements:
                val = td_element.text.strip()
                ls.append(val)
            res.append(ls)
        except Exception as e:
            print("Exception above 1: ", e)
    return res

# R 5.1.5
def getpanchayatTup515(fn, start_row, state, district, block): 
    with open(fn, encoding='utf-8') as file:  
        soup = BeautifulSoup(file, 'html.parser')
    panchayats = soup.findAll("tr")[start_row:-1]
    res = []
    for panchayat in panchayats:
        try:
            panchayat_element = panchayat.find('td').find_next_sibling("td")
            panchayat_name = panchayat_element.text.strip().lower()
            total_td_elements = panchayat.findAll('td')[2:]
            ls = [state, district, block, panchayat_name]
            for td_element in total_td_elements:
                val = td_element.text.strip()
                ls.append(val)
            res.append(ls)
        except Exception as e:
            print("Exception above 1: ", e)
    return res

# R 5.1.1
def getpanchayatTup511(fn, start_row, state, district, block): 
    with open(fn, encoding='utf-8') as file:  
        soup = BeautifulSoup(file, 'html.parser')
    panchayats = soup.findAll("tr")[start_row:-1]
    res = []
    for panchayat in panchayats:
        try:
            panchayat_element = panchayat.find('td').find_next_sibling("td")
            panchayat_name = panchayat_element.text.strip().lower()
            total_td_elements = panchayat.findAll('td')[2:]
            ls = [state, district, block, panchayat_name]
            for td_element in total_td_elements:
                val = td_element.text.strip()
                ls.append(float(val))
            res.append(ls)
        except Exception as e:
            print("Exception above 1: ", e)
    return res

# R 14.1
def getpanchayatTup141(fn, start_row, state, district, block): 
    with open(fn, encoding='utf-8') as file:  
        soup = BeautifulSoup(file, 'html.parser')
    panchayats = soup.findAll("tr")[start_row:-1]
    res = []
    for panchayat in panchayats:
        try:
            panchayat_element = panchayat.find('td').find_next_sibling("td")
            panchayat_name = panchayat_element.text.strip().lower()
            total_td_elements = panchayat.findAll('td')[2:]
            ls = [state, district, block, panchayat_name]
            for td_element in total_td_elements:
                val = td_element.text.strip()
                ls.append(val)
            res.append(ls)
        except Exception as e:
            print("Exception", e)
    return res

# R 1.1.1
def getpanchayatTup111(fn, start_row, state, district, block): 
    with open(fn, encoding='utf-8') as file:  
        soup = BeautifulSoup(file, 'html.parser')
    panchayats = soup.findAll("tr")[start_row:-2]
    res = []
    for panchayat in panchayats:
        try:
            panchayat_element = panchayat.find('td').find_next_sibling("td")
            panchayat_name = panchayat_element.text.strip().lower()
            total_td_elements = panchayat.findAll('td')[2:]
            ls = [state, district, block, panchayat_name]
            for td_element in total_td_elements:
                val = td_element.text.strip()
                ls.append(val)
            res.append(ls)
        except Exception as e:
            print("Exception", e)
    return res

def create_csv_711(data): 
    selected_indices = [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8]
    selected_data = [[row[i] for i in selected_indices] for row in data]
    column_names = [
        "year", "state", "district", "block", "panchayat", 
        "unskilled_wage_expenditure", "skilled_wage_expenditure", 
        " material_expenditure", "tax_expenditure", "admin_expenditure"
    ]
    df = pd.DataFrame(selected_data, columns=column_names)
    csv_filename = output_dir + '711.csv'
    df.to_csv(csv_filename, index=False)

def create_csv_721(data): 
    selected_indices = [-1, 0, 1, 2, 3, 4]
    selected_data = [[row[i] for i in selected_indices] for row in data]
    column_names = [
        "year", "state", "district", "block", "panchayat", "average_wage"
    ]
    df_selected = pd.DataFrame(selected_data, columns=column_names)
    csv_filename = output_dir + '721.csv'
    df_selected.to_csv(csv_filename, index=False)

def create_csv_515(data): 
    selected_indices = [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
    selected_data = [[row[i] for i in selected_indices] for row in data]
    column_names = [
        "year", "state", "district", "block", "panchayat",
        "jc_issued_sc", "jc_issued_st", "jc_issued_oth", "jc_issued_total", 
        "emp_provided_household_sc", "emp_provided_household_st", 
        "emp_provided_household_oth", "emp_provided_household_total",
        "emp_provided_women_count", "emp_provided_persondays_sc",
        "emp_provided_persondays_st", "emp_provided_persondays_oth", 
        "emp_provided_persondays_total", "emp_provided_persondays_women",
        "families_completed_100_days_sc", "families_completed_100_days_st", 
        "families_completed_100_days_oth", "families_completed_100_days_total"
    ] 
    df_selected = pd.DataFrame(selected_data, columns=column_names) 
    csv_filename = output_dir + '515.csv'
    df_selected.to_csv(csv_filename, index=False)

def create_csv_511(data): 
    selected_indices = [-1, 0, 1, 2, 3, 4, 15, 14, 13, 11, 10, 12]
    selected_data = [[row[i] for i in selected_indices] for row in data]
    column_names = [
        "year", "state", "district", "block", "panchayat",
        "registered_household", "employment_demanded_persons",
        "employment_demanded_household", "total_jobcards_issued",
        "jobcards_issued_st", "jobcards_issued_sc", "jobcards_issued_others"
    ] 
    df_selected = pd.DataFrame(selected_data, columns=column_names)
    csv_filename = output_dir + '511.csv'
    df_selected.to_csv(csv_filename, index=False)

def create_csv_141(data): 
    selected_indices = [-1, 0, 1, 2, 3, 4, 5, 7]
    selected_data = [[row[i] for i in selected_indices] for row in data]
    column_names = [
        "year", "state", "district", "block", "panchayat",
        "delay_compensation_payable_days", "delay_compensation_payabale_amount",
        "delay_compensation_approved_amount"
    ]
    df_selected = pd.DataFrame(selected_data, columns=column_names)
    csv_filename = output_dir + '141.csv'
    df_selected.to_csv(csv_filename, index=False)

def create_csv_111(data): 
    selected_indices = [-1, 0, 1, 2, 3, 10, 7, 6, 8, 9, 5, 11, 13, 12, 14]
    selected_data = [[row[i] for i in selected_indices] for row in data]
    column_names = [
        "year", "state", "district", "block", "panchayat",
        "registered_women_workers", "registered_st_workers", 
        "registered_sc_workers", "registered_oth_workers",   
        "registered_total_workers", "jobcards_issued",        
        "jobcards_active", "active_st_workers", "active_sc_workers", 
        "active_oth_workers"                                
    ] 
    df_selected = pd.DataFrame(selected_data, columns=column_names)
    csv_filename = output_dir + '111.csv'
    df_selected.to_csv(csv_filename, index=False)
    
def readfile(filename): 
    with open(filename, encoding='utf-8') as f:
        content = f.readlines()
    return [x.strip() for x in content]

for i in range(len(savedhtml_lines)):
    data = []
    # Getting the parameter name
    param = savedhtml_lines[i]  

    # Getting the parameter directory
    param_dir = path.join("html", param)
    print(param)

    # If the directory for param doesn't exist
    if not path.exists(param_dir):
        print("Param directory ", param_dir, " does not exist.")

    # Iterating through the years
    for year in years:
        # Checking if the directory for year exist
        year_dir = path.join(param_dir, year)
        if not path.exists(year_dir):
            print("Year directory ", year_dir, " does not exist.")

        # Getting the states from the dir
        print("year_dir : ", year_dir)
        states = [x for x in os.listdir(year_dir)]

        # Iterate through the states
        for state in states:
            try:
                print("state: ", state)
                state_dir = os.path.join(year_dir, state)

                # Getting the districts from the state directory
                districts = [x for x in os.listdir(state_dir)]

                # Iterating over each of the districts
                for district in districts:
                    try:
                        district_dir = os.path.join(state_dir, district)

                        # Getting the blocks from the district directory
                        blocks = [x for x in os.listdir(district_dir)]

                        # Iterating over each of the blocks
                        for block in blocks:
                            try:
                                # Some were having empty names with just .html, skipped those as those were corrupted files
                                if block == ".html":
                                    continue
                                # Getting the block file
                                block_file = os.path.join(district_dir, block) 
                                # print(state.lower(), district.lower(), block.lower()[0:-5])
                                if(i == 0):
                                    panchayatList = getpanchayatTup111(block_file, 10, state.lower(), district.lower(), block.lower()[0:-5])
                                elif(i == 1):
                                    panchayatList = getpanchayatTup515(block_file, 7, state.lower(), district.lower(), block.lower()[0:-5])
                                elif(i == 2):
                                    panchayatList = getpanchayatTup141(block_file, 9, state.lower(), district.lower(), block.lower()[0:-5])
                                elif(i == 3):
                                    panchayatList = getpanchayatTup511(block_file, 6, state.lower(), district.lower(), block.lower()[0:-5])
                                elif(i == 4):
                                    panchayatList = getpanchayatTup721(block_file, 5, state.lower(), district.lower(), block.lower()[0:-5])
                                elif(i == 5):
                                    panchayatList = getpanchayatTup711(block_file, state.lower(), district.lower(), block.lower()[0:-5])

                                if(panchayatList == []):
                                    print(param, year, state, district, block)

                                for p in panchayatList:
                                    p.append(year)
                                    data.append(p)        
                            except Exception as e:
                                print("Exception below 1: ", e, " block name: ", os.path.join(district_dir, block), " panchayat list: ", panchayatList)
                    except Exception as e:
                        print("Exception below 2: ", e)
                # break
            except Exception as e:
                print("Exception below 3: ", e)
    if(i == 0):
        create_csv_111(data)
    elif(i == 1):
        create_csv_515(data)
    elif(i == 2):
        create_csv_141(data)
    elif(i == 3):
        create_csv_511(data)
    elif(i == 4):
        create_csv_721(data)
    elif(i == 5):
        create_csv_711(data)