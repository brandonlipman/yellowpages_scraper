import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import csv
import re
import requests
from bs4 import BeautifulSoup
import time


def extract_yellowpages_links(url,start_page =1,end_page =100,all_pages = False):
    """extracts individual links from specified url in yellowpages.com"""
    url =  url + "&page={0}"
    extracted_links = []

    if all_pages is False:
        while start_page != end_page:
            content = requests.get(url.format(start_page)).content
            soup = BeautifulSoup(content)
            links = [i["href"] for i in soup.find_all("a",{"itemprop":"name"})]
            extracted_links.extend(links)
            start_page += 1

    elif all_pages is True:
         while True:
            content = requests.get(url.format(start_page)).content
            soup = BeautifulSoup(content)
            links = [i["href"] for i in soup.find_all("a",{"itemprop":"name"})]
            if not links:
                break
            extracted_links.extend(links)
            start_page += 1

    return extracted_links


def extracted_links_info(links,wait_interval= 0):
    """gets the information of the extracted links"""
    business_names = []
    business_emails = []
    business_websites = []
    street_addresses = []
    cities = []
    business_contact_numbers = []

    for link in links:
        time.sleep(wait_interval)
        link = "http://www.yellowpages.com" + link
        content = requests.get(link).content
        soup2 = BeautifulSoup(content)
        business_name = [soup2.find("h1",{"itemprop":"name"}).text]
        business_email = [re.sub(r'mailto:', "",soup2.find("a",{"class":"email-business"})["href"]) if soup2.find("a",{"class":"email-business"}) else "---" ]
        business_site = [soup2.find("a",{"class":"custom-link"})["href"] if soup2.find("a",{"class":"custom-link"}) else "---" ]
        street_address = [ soup2.find("p",{"class":"street-address"}).text if soup2.find("p",{"class":"street-address"}) else "----"]
        city = [soup2.find("p",{"class":"city-state"}).text if soup2.find("p",{"class":"city-state"}) else "---"]
        business_contact_number = [soup2.find("p",{"class":"phone"}).text if soup2.find("p",{"class":"phone"}) else "---"]
        business_names.extend(business_name)
        business_emails.extend(business_email)
        business_websites.extend(business_site)
        street_addresses.extend(street_address)
        cities.extend(city)
        business_contact_numbers.extend(business_contact_number)
        
    return business_names, business_emails, business_websites, street_addresses, cities, business_contact_numbers

def goToNextPage():
    Calculate tyhe number of pages 
    


def save_to_csv(filename,extracted_info):
    """saves csv file in root of python 3 directory"""
    items = list(zip(*extracted_info))
    with open("{0}.csv".format(filename), "w")as shops:
        writer = csv.writer(shops)
        writer.writerows(items)



if __name__ == "__main__":
    extracted_links = extract_yellowpages_links("http://www.yellowpages.com/search?search_terms=restaurants&geo_location_terms=Cincinnati%2C+OH",1,2)
    parsed_info = extracted_links_info(extracted_links)
    save_to_csv("test",parsed_info)
    
    
