import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import csv
import re
import requests
from bs4 import BeautifulSoup
import time

print ('I got to this line')

def extract_yellowpages_links(url,start_page =1,end_page =100,all_pages = False):
    """extracts individual links from specified url in yellowpages.com"""
    url =  url + "&page={0}"
    extracted_links = []

    if all_pages is False:
        print ('not all pages on loop. Generating URLs .......')
        while start_page != end_page:
            content = requests.get(url.format(start_page)).content
            soup = BeautifulSoup(content)
            links = [i["href"] for i in soup.find_all("a",{"itemprop":"name"})]
            extracted_links.extend(links)
            start_page += 1

    elif all_pages is True:
        print ('All page loop is on. Generating URLs, this is going to take a while ........')
        while True:
            content = requests.get(url.format(start_page)).content
            soup = BeautifulSoup(content)
            links = [i["href"] for i in soup.find_all("a",{"itemprop":"name"})]
            if not links:
                break
            extracted_links.extend(links)
            start_page += 1

    return extracted_links


def extracted_links_info(links,wait_interval= .1):
    """gets the information of the extracted links"""
    business_names = []
    business_emails = []
    business_websites = []
    street_addresses = []
    cities = []
    business_contact_numbers = []
    business_neighborhoods = []
    business_general_infos = []
    business_ratings = []
    business_ages = []
    business_twitters = []
    business_times = []
    business_payment_methods = []
    business_categories_list = []
    business_extra_links = []
    business_other_infos = []
    business_price_ranges = []
    business_locations = []
    extra_phone_numbers = []
    business_menus = []

    for link in links:
        time.sleep(wait_interval)
        link = "http://www.yellowpages.com" + link
        content = requests.get(link).content
        soup2 = BeautifulSoup(content)
        business_name = [soup2.find("h1",{"itemprop":"name"}).text if soup2.find("h1",{"itemprop":"name"}) else "---"]
        business_rating = [soup2.find("itemscope",{"itemprop":"ratingValue"}).text if soup2.find("itemscope",{"itemprop":"ratingValue"}) else "---"]

        business_twitter = [soup2.find("a",{"class":"description"})["href"] if soup2.find("a",{"class":"description"}) else "---" ]
        business_price_range = [soup2.find("span",{"itemprop":"priceRange"}).text if soup2.find("span",{"itemprop":"priceRange"}) else "---"]

        business_extra_phones = [soup2.find("dd",{"class":"extra-phones"}).text if soup2.find("dd",{"class":"extra-phones"}) else "---"]

        business_menu = [soup2.find("a",{"class":"view-menu"})["href"] if soup2.find("a",{"class":"view-menu"}) else "---"]


        business_time = [soup2.find("dd",{"class":"open-hours"}).text if soup2.find("dd",{"class":"open-hours"}) else "---"]
        business_payment_method = [soup2.find("dd",{"class":"payment"}).text if soup2.find("dd",{"class":"payment"}) else "---"]
        business_categories = [soup2.find("dd",{"class":"categories"}).text if soup2.find("dd",{"class":"categories"}) else "---"]
        business_extra_link = [soup2.find("dd",{"class":"weblinks"}).text if soup2.find("dd",{"class":"weblinks"}) else "---"]
        business_other_info = [soup2.find("dd",{"class":"other-information"}).text if soup2.find("dd",{"class":"other-information"}) else "---"]

        business_location = [soup2.find("dd",{"class":"location-description"}).text if soup2.find("dd",{"class":"location-description"}) else "---"]
        business_neighborhood = [soup2.find("dd",{"class":"neighborhoods"}).text if soup2.find("dd",{"class":"neighborhoods"}) else "---"]
        business_general_info = [soup2.find("dd",{"class":"description"}).text if soup2.find("dd",{"class":"description"}) else "---"]
        business_age = [soup2.find("p",{"class":"count"}).text if soup2.find("p",{"class":"count"}) else "---"]
        city = [soup2.find("p",{"class":"city-state"}).text if soup2.find("p",{"class":"city-state"}) else "---"]
        business_email = [re.sub(r'mailto:', "",soup2.find("a",{"class":"email-business"})["href"]) if soup2.find("a",{"class":"email-business"}) else "---" ]
        business_site = [soup2.find("a",{"class":"custom-link"})["href"] if soup2.find("a",{"class":"custom-link"}) else "---" ]
        street_address = [ soup2.find("p",{"class":"street-address"}).text if soup2.find("p",{"class":"street-address"}) else "----"]
        business_contact_number = [soup2.find("p",{"class":"phone"}).text if soup2.find("p",{"class":"phone"}) else "---"]

        business_names.extend(business_name)
        business_neighborhoods.extend(business_neighborhood)
        business_general_infos.extend(business_general_info)
        business_emails.extend(business_email)
        business_websites.extend(business_site)
        street_addresses.extend(street_address)
        cities.extend(city)
        business_contact_numbers.extend(business_contact_number)
        business_ratings.extend(business_rating)
        business_ages.extend(business_age)
        business_twitters.extend(business_twitter)
        business_times.extend(business_time)
        business_payment_methods.extend(business_payment_method)
        business_categories_list.extend(business_categories)
        business_extra_links.extend(business_extra_link)
        business_other_infos.extend(business_other_info)
        business_price_ranges.extend(business_price_range)
        business_locations.extend(business_location)
        extra_phone_numbers.extend(business_extra_phones)
        business_menus.extend(business_menu)
        print (business_name)
        print (business_email)
        print (business_site)
        print (business_neighborhood)
        print (' ')
        
    return business_names, business_ages, business_price_ranges, business_menus, business_locations, business_payment_methods, business_categories_list, business_times, business_neighborhoods, business_emails, business_websites, street_addresses, cities, business_general_infos


def save_to_csv(filename,extracted_info):
    """saves csv file in root of python 3 directory"""
    items = list(zip(*extracted_info))
    with open("{0}.csv".format(filename), "w")as shops:
        writer = csv.writer(shops)
        writer.writerows(items)



if __name__ == "__main__":
    print ('the bottom code is running')
    extracted_links = extract_yellowpages_links("http://www.yellowpages.com/search?search_terms=restaurants&geo_location_terms=Orlando%2C+FL",40,101,False)
    parsed_info = extracted_links_info(extracted_links)
    save_to_csv("orlando_page_40_101_scrape",parsed_info)
    
    
