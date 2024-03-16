# Imports
import os
import requests
from os import path
from bs4 import BeautifulSoup
from multiprocessing import Process
import pandas as pd
import argparse
import sys

def checkfile(filename):
    """
    check if file exists or not

    Paramters
    ---------
    filename : str
        name of file
    
    Results
    -------
        bool
            if the filename is present or not
    """

    return path.exists(filename)

def check_year(year):
    """
    checks if the given year is in correct format or not

    Parameters
    ----------
        year : str
            financial year whose format is to be checked

    Results
    -------
        bool
            if the year is in correct format or not 
    """

    try:
        #splitting the year in two years
        fyear , syear = year.split("-")
        fyear = int(fyear)
        syear = int(syear)

        #checking if the difference between two years is one or not
        return not (syear - fyear) != 1
    except Exception as e:
        return False


def exec_district(district,state_name,state_dir,parameters):
    """
    function to get data within districts

    Parameters
    ----------
    district : <class 'bs4.element.Tag'>
        district object whose data is to be extracted
    state_name : str
        name of state of the district
    state_dir : str
        the path of the directory where district data will be saved
    parameters: dict
        parameters of the report whose data is to be extracted
    
    Results
    -------
        data within districts is downloaded and saved in html/report_name/year/state/district/ folder
    """
    try:

        # Getting the district link element from the 2nd column
        district_element = district.find('td').find_next_sibling("td")
        
        #useful for report 7.1.1 where some non-district <class 'bs4.element.Tag'> object is between district objects
        #which needed to be ignored
        if(district_element==None):
            return

        # Getting the href element from it
        href_element = district_element.find_all(href=True)

        # If there exist a link, go ahead
        if len(href_element) != 0:

            # Append the link to the base url     
            #replace part for report 7.1.1 to make html_link correct        
            html_link = parameters['base'] + href_element[0]['href'].replace('../../citizen_Html/','')
            
            #One of the panchayat in Andaman and Nicobar has / in name 
            #hence changing it to - so that it does not get interpreted as a directory
            district_name = href_element[0].text.replace("/","-")

            # Check if the district name is non-empty
            if district_name == "":
                print(f"District in State: {state_name} not available")
                return

            
            # Getting the blocks from the district page link formed above
            bsoup = BeautifulSoup(requests.get(html_link).content,'html.parser')
           
           #For the reports where only block level data is available.
            if(pd.isna(parameters['block_trunc_index_start'])):
                if path.exists(path.join(state_dir, district_name + ".html")):
                    return
                file = open(os.path.join(state_dir, district_name + ".html"), 'wb')
                file.write(bsoup.prettify(encoding='utf-8'))
                print("html file saved")
                file.close()
                return
            
            # Create the district directory if doesn't exist
            district_dir = path.join(state_dir, district_name)
            if not path.exists(district_dir):
                os.makedirs(district_dir)
                
            blocks = bsoup.findAll("tr")[int(parameters['block_trunc_index_start']):int(parameters['block_trunc_index_end'])]

            # Iterating through each of the block
            for block in blocks:
                try:

                    # Getting the block name and link from the 2nd column
                    block_element = block.find('td').find_next_sibling("td")
                    href_element = block_element.find_all(href=True)

                    # Check if there exists a link
                    if len(href_element) != 0:

                        # Append the href link obtained to the base url      
                        ##replace part for report 7.1.1 to make html_link correct
                        html_link = parameters['base'] + href_element[0]['href'].replace('../../citizen_html/','')
                        block_name = href_element[0].text.replace("/","-")

                        # Check if the block name is empty
                        if block_name == "":
                            print(f"Block in District {district_name} not available")
                        
                        # Check if the block file already exists
                        if path.exists(path.join(district_dir, block_name + ".html")):
                            continue

                        # Getting the block page
                        block_page = requests.get(html_link).content

                        # Saving the block page to html file
                        file = open(os.path.join(district_dir, block_name + ".html"), 'wb')
                        file.write(block_page)
                        print("html file saved")
                        file.close()
                        
                except Exception as e:
                    print(e)
    except Exception as e:
        print(e)

def exec_state(state,year_dir,parameters):
    """
    function to get data within states

    Parameters
    ----------
    state : <class 'bs4.element.Tag'>
        state object whose data is to be extracted
    year : str
        the path of the directory where within state data will be saved
    parameters: dict
        parameters of the report whose data is to be extracted
    
    Results
    -------
        data within states is downloaded and saved in html/report_name/year/state/ folder
    """
    
    try:

        # State name with link in the 2nd column, so moving to the next sibling
        state_element = state.find('td').find_next_sibling("td")

        # Getting the href link from the element
        href_element = state_element.find_all(href = True)

        # Check if there exist an href link
        if len(href_element) != 0:
            # Append the link to the base html url
            html_link = parameters['base'] + href_element[0]['href']

            #One of the panchayat in Andaman and Nicobar has / in name 
            #hence changing it to - so that it does not get interpreted as a directory
            state_name = href_element[0].text.replace("/","-")
            print('Starting:',state_name)

            # Check if the state name is non-empty
            if state_name == "":
                print(f"State not available")
                return

            # Creating the directory for the state if doesn't exist
            state_dir = path.join(year_dir, state_name)
            if not path.exists(state_dir):
                os.makedirs(state_dir)

            # Getting the districts using the link for the state formed above
            dsoup = BeautifulSoup(requests.get(html_link).content,'html.parser')

            print(html_link)

            #finding all the objects corresponding to districts in the state
            districts = dsoup.findAll("tr")[int(parameters['district_trunc_index_start']):int(parameters['district_trunc_index_end'])]
            
            #list of processes
            processes=[]

            #assigning a district to each process
            for district in districts:
                processes.append(Process(target=exec_district,args=(district,state_name,state_dir,parameters)))
            
            #starting all processes
            for j in range(len(districts)):
                processes[j].start()
            
            #waiting for processes to join
            for j in range(len(districts)):
                processes[j].join()

            print('Ending:',state_name,'\n')
    except Exception as e:
        print(e)



def get_report(year,parameters):
    """
    This function gets all the reports in html form.

    Parameters
    ----------
    year: str
        financial year whose data is to be extracted
    parameters: dict
        parameters of the report whose data is to be extracted

    Results
    -------
        data get downloaded and saved in html/report_name/year folder
    """

    #url of the main page of report where state level data is present
    url = parameters['hyperlink']

    #name of report -- directory name where reports will be saved
    param = parameters['report number']

    # Creating the directory for the parameter, if doesn't exist
    param_dir = path.join("html", param)
    if not path.join(param_dir):
        os.makedirs(param_dir)

   
    print("year started",year)

    # Creating the directory for the yeawr, if doesn't exist
    year_dir = path.join(param_dir, year)
    if not path.exists(year_dir):
        os.makedirs(year_dir)

    # Appending the year parameter to the url
    year_url = url + year
    print(f'year url: {year_url}')
    soup = BeautifulSoup(requests.get(year_url).content,'html.parser')

    # Getting all the states into the table on the webpage
    states = soup.findAll("tr")[parameters['state_trunc_index_start']:parameters['state_trunc_index_end']]

    # Iterating through each of the state to get data
    for state in states:
        exec_state(state,year_dir,parameters)
    
    print("year ended",year,'\n')
        

#parser to get command-line arguments
parser = argparse.ArgumentParser(description='A script with command line arguments.')

#an argument -r or --report which defines the report to scrap
parser.add_argument('-r', '--report', type=str, help='Report number.')

#an argument -y or --year which defines the year
parser.add_argument('-y', '--year', type=str, help='Report year.')
args = parser.parse_args()

report_number = args.report
year = args.year

#reading parameters from report_parameter.xlsx
df = pd.read_excel('report_parameters.xlsx')

#getting names of all reports present in report_parameters.xlsx file
reports_list = df['report number'].tolist()

#checking if report present in the report_parameters.xlsx file or not
if(report_number not in reports_list):
    sys.stderr.write(f"Report {report_number} not found.\n")

#checking if year is correct valid or not
elif(not(check_year(year))):
    sys.stderr.write(f"Invalid year {year}. Years should be consecutive and of form YYYY-YYYY.\n")

#if everything is right then continue to scrap report
else:
    #parameters of the report to be scraped in dict form
    parameters = df[df['report number'] == report_number].iloc[0].to_dict()
    get_report(year,parameters)


