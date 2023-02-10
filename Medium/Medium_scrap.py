# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 22:16:27 2021

@author: aleex



WSCRAPING WALKTHROUGH using Selenium
https://medium.com/swlh/web-scrapping-healthcare-professionals-information-1372385d639d
"""


from bs4 import BeautifulSoup
import urllib
import re
import time
import pandas as pd
import os

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
chrome = "C:\\Users\\aleex\\chromedriver_win32/chromedriver.exe"
headers = {'User-Agent': 
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

# Define target website

# Define healthcare professional (HCP) body 
hcp_body = 'SPC'

# Set wait times
waittime = 20
sleeptime = 2

url = 'https://prs.moh.gov.sg/prs/internet/profSearch/main.action?hpe=SPC'
html_content = urllib.request.urlopen(url)
page_html = BeautifulSoup(html_content, 'html.parser')

# Set webdriver options
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('ignore-certificate-errors')

driver = webdriver.Chrome(chrome)
driver.get(url)

# We search and move on to the right frame
driver.switch_to.frame(driver.find_element_by_name('msg_main'))
# And we press the button SEARCH
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//input[@name='btnSearch']"))).click()

time.sleep(3)

# Setting up master list CSV to store all the records

file_name = 'master_list.csv'
# Check if file already exists
if os.path.isfile(f'./{file_name}'):
    print(f'Filename {file_name} already exists')
else:
    # Set names of fields we want to extract
    column_names = ['name','reg_number','reg_date','reg_end_date','reg_type','practice_status',
                    'cert_start_date','cert_end_date','qualification','practice_place_name',
                    'practice_place_address','practice_place_phone']
    
    
    # Generate template dataframe
    df_template = pd.DataFrame(columns = column_names)
    
    # Generate csv file from the dataframe template
    df_template.to_csv(f'{file_name}', header=True)
    
    print('Created new master list file')
    
    
# Get current page number

def get_current_page():
    current_page_elem = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,
                                                                                       "//label[@class='pagination_selected_page']"))).text
    
    current_page_num = int(current_page_elem)
    return current_page_num

def get_absolute_last_page():
    # Find all elements with pagination class (since it contains 
    # page numbers)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//a[@class='pagination']")))
    all_pages = driver.find_elements_by_xpath("//a[@class='pagination']")
    # Get final element, which corresponds to 'Last' hyperlink
    # (which will go to last page number)
    last_elem = all_pages[-1].get_attribute('href')

    # Keep only the number of last page
    last_page_num = int(re.sub("[^0-9]", "", last_elem))
    
    return last_page_num


def gen_hcp_dict(): # SINGLE RECORD
    hcp_name = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,"//div[@class='table-head']"))).text
    all_fields = driver.find_elements_by_xpath("//td[@class='no-border table-data']")
    hcp_data = []
    for field in all_fields:
        hcp_data.append(field.text)
        
    hcp_dict = {}
    # Assign extracted data into respective key-value pairs
    hcp_dict['name'] = hcp_name
    hcp_dict['reg_number'] = hcp_data[0]
    # hcp_data[1] is just a blank space, so it can be ignored
    hcp_dict['reg_date'] = hcp_data[2]
    hcp_dict['reg_end_date'] = hcp_data[3]
    hcp_dict['reg_type'] = hcp_data[4]
    hcp_dict['practice_status'] = hcp_data[5]
    hcp_dict['cert_start_date'] = hcp_data[6]
    hcp_dict['cert_end_date'] = hcp_data[7]
    hcp_dict['qualification'] = hcp_data[8]
    hcp_dict['practice_place_name'] = hcp_data[9]
    hcp_dict['practice_place_address'] = hcp_data[10]
    hcp_dict['practice_place_phone'] = hcp_data[11]
    
    
def get_current_pagination_range():

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//a[@class='pagination']")))
    
    # Get all elements related to pagination
    all_pages = driver.find_elements_by_xpath("//a[@class='pagination']")
    
    # Implicit wait to allow page to load
    driver.implicitly_wait(1)
    
    # Find numbers of pagination range, and append to list
    pagination_range_on_page = []
    for elem in all_pages:
        
        # Only extracting numeric values of pagination range
        if elem.text.isnumeric():
            pagination_range_on_page.append(int(elem.text))
            driver.implicitly_wait(1)
        else:
            pass
    driver.implicitly_wait(1)
    return pagination_range_on_page



def click_last_pagination_num(pagination_range):
    last_pagination_num = pagination_range[-1] 
    
    # Introduce implicit wait for page to complete loading
    driver.implicitly_wait(1)
    
    # Click page number once element is located
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, '{}'.format(last_pagination_num)))).click() 
    driver.implicitly_wait(1)
    
def click_first_pagination_num(pagination_range):

    first_pagination_num = pagination_range[0] 
    
    # Introduce implicit wait for page to complete loading
    driver.implicitly_wait(1)
    
    # Click page number once element is located
    WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.LINK_TEXT, '{}'.format(first_pagination_num)))).click() 
    driver.implicitly_wait(1)   
    
    
def locate_target_page(target_page):
    
    last_page_num = get_absolute_last_page()
    #Find midway point, in pages, for the whole search
    midway_point = last_page_num/2
    
    # If target page is in first half, start clicking from the start
    if target_page < midway_point: 
        current_page_num = get_current_page()
        
        if current_page_num == target_page:
            pass
        else:
            pagination_range = get_current_pagination_range()
            while target_page not in pagination_range:
                driver.implicitly_wait(1)
                click_last_pagination_num(pagination_range) 
                current_page_num = get_current_page()
                pagination_range = get_current_pagination_range()
                driver.implicitly_wait(1)
            else:
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT,
                                                                                "{}".format(target_page)))).click()
        # If target page is in later half of list, go to Last page and      
    # move in reverse (This saves alot of time)
    else: 
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, 'Last'))).click()
        time.sleep(3)
        current_page_num = get_current_page()

        if current_page_num == target_page:
            pass
        else:           
            pagination_range = get_current_pagination_range()

            while target_page not in pagination_range:
                driver.implicitly_wait(2)
                click_first_pagination_num(pagination_range)
                current_page_num = get_current_page()
                pagination_range = get_current_pagination_range()
            else:
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT,
                                                                                "{}".format(target_page)))).click() 

def full_scrape(target_page):
    #measure the whole search
    last_page_num = get_absolute_last_page()
    driver.implicitly_wait(1)  
    while target_page != last_page_num:
        locate_target_page(target_page)
        print('Starting with target page ' + str(target_page))
        
        # Retrieve HTML from search page
        target_page_html = driver.find_element_by_xpath("//body").get_attribute('outerHTML')
        driver.implicitly_wait(1)
        
        # Find list of all IDs on that page, and keep the unique IDs
        all_ids = re.findall("P[0-9]{5}[A-Z]{1}", target_page_html)
        id_list = list(dict.fromkeys(all_ids))

        for index, hcp_id in enumerate(id_list):   
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, f"//a[contains(@onclick,'{hcp_id}')]"))).click()
            hcp_dict = gen_hcp_dict()
            df_hcp_dict = pd.DataFrame(hcp_dict,index=[0])
            df_hcp_dict.to_csv(file_name, mode='a', header=False)
            print(f'Scraped row {index+1} of page {target_page}')
            
            if index == len(id_list):
                print(f'Completed scraping for page {target_page}')
                target_page += 1
                print('Updated target page ' + str(target_page))
            else:
                pass
            
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, 'Back to Search Results'))).click() 
            locate_target_page(target_page)
    else: # if we are on last page
        locate_target_page(target_page)
        print('Working on last page')
        target_page_html = driver.find_element_by_xpath("//body").get_attribute('outerHTML')
        driver.implicitly_wait(1)
        all_ids = re.findall("P[0-9]{5}[A-Z]{1}", target_page_html)
        id_list = list(dict.fromkeys(all_ids))

        for index, hcp_id in enumerate(id_list): 
            WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.XPATH, f"//a[contains(@onclick,'{hcp_id}')]"))).click()           
            hcp_dict = gen_hcp_dict()
            df_hcp_dict = pd.DataFrame(hcp_dict, index=[0])
            df_hcp_dict.to_csv(file_name, mode='a', header=False)
            print(f'Scraped row {index+1} of {target_page}')
            
            if index == len(id_list)-1:
                print(f'Completed scraping for page {target_page}')
                print('Mission Complete')
            else:
                pass
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, 'Back to Search Results'))).click() 
            locate_target_page(target_page)
            
# Start with selected target page. target_page = 1 by default (to start from page 1)
target_page = 1

# Display time started
print(time.strftime("%H:%M:%S", time.localtime()))

# Run main web scraping function
full_scrape(target_page)

# Display time concluded
print(time.strftime("%H:%M:%S", time.localtime())) 


# Import master list csv file
df_master = pd.read_csv(f'{file_name}')
# Display master list columns
df_master.columns
# Drop leftmost index column (Unnecessary column)
df_master.drop(columns = [df_master.columns[0]], axis = 1, inplace = True)

# Remove duplicates
df_master.drop_duplicates(keep='first', inplace=True)
# Export final curated list
df_master.to_excel('master_list_final.xlsx', index = False)


