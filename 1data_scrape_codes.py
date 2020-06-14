"""
Scrape data from trademe.com and save the scraped data to a .csv file
Author: Yao Chen
Edite Date: 16/05/2019
"""

from urllib import request
import re
import csv
import os

os.chdir('H:/1ads/COSC480-19S1/project/')


def content_of_webpage(url, headers):
    """Open a given url and return the content of the webpage.
       Parameters£º
       url: the target website;
       headers: request header, in order to reduce the risk of getting blocked. 
    """
    opener = request.build_opener()
    opener.addheaders = [headers]
    request.install_opener(opener) # install it so it can be used with urlopen.
    content_of_webpage = request.urlopen(url).read().decode("UTF-8")
    return content_of_webpage


def item_url_part(content):
    """Save urls of every motor advertised on the web to a set, 
       to avoid repetition.
       Parameters£º
       content:the content of a webpage.
    """
    pattern_item_url = 'a class="tmm-sf-search-card-list-view__link" href="(/motors/used-cars/.*?)">'
    pattern_model = 'class="tmm-sf-search-card-list-view__title--bold"> (.*?) </div>'
    item_url_list = re.compile(pattern_item_url).findall(content)
    item_url_set = set(item_url_list)
    return item_url_set


def item_dict(content_of_itempage):
    """Extract specific car information from itempage, and return a dictionary
       of cars information.
       Parameter:
       content_of_itempage:content of a specified car's detailed webpage.
    """
    pattern_price_now = '<div id="BuyNow_BuyNow" class="large-text buynow-details buy-now-price-text">(.*?)</div>'
    pattern_price_ask = '<span class="large-text buynow-details asking-price-text.*?">(.*?)</span>'
    pattern_price_start = '<div id="Bidding_CurrentBidValue" class="large-text current-bid-details current-bid-details">(.*?)</div>'
    pattern_location = '<span id="ListingDateBox_LocationText" class="location-text">(.*?)</span>'
    now_price = re.compile(pattern_price_now).findall(content_of_itempage)
    ask_price = re.compile(pattern_price_ask).findall(content_of_itempage)
    start_price = re.compile(pattern_price_start).findall(content_of_itempage)
    location = re.compile(pattern_location).findall(content_of_itempage)
    item_dict = {"location":location, "buy_now":now_price, "asking_price":ask_price, "start_price":start_price} 
    pattern_attribute_label = '<label class="motors-attribute-label">(.*?)</label>'
    pattern_attribute_value = '<span class="motors-attribute-value">(.*?)<'    
    attribute_label = re.compile(pattern_attribute_label).findall(content_of_itempage)
    attribute_value = re.compile(pattern_attribute_value).findall(content_of_itempage)        
    for i in range(0, len(attribute_label)):
        item_dict[attribute_label[i]] = attribute_value[i]
    return item_dict


def outfile(filename, data, keys_list):
    """Write the data into a .csv file
       Parameters:
       filename: filename of the saving file.
       data: data to be saved in the file.
       keys_list:dictionary's keys, the file the first line as column names.       
    """
    outfile = open(filename, 'w', newline='')
    cw = csv.DictWriter(outfile, fieldnames=keys_list)
    cw.writeheader() 
    for rowdict in data:
        cw.writerow(rowdict) 
    

def main():
    """Extract all the useful information from every page of the webside,
       and write them into the .csv file, forming the raw_data_scraped.
    """
    url = "https://www.trademe.co.nz/motors/used-cars/more-makes"
    headers = (
    "User-Agent",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36"
    )
    filename = '1_raw_data_scraped.csv'   
    page = 50
    ttl_item_url = set()
    for i in range(1, page):
        url_request = url + "?page=" + str(i)
        content = content_of_webpage(url_request, headers)
        item_url_set = item_url_part(content)
        ttl_item_url = ttl_item_url.union(item_url_set)
    
    all_item_extract = []
    keys_list = set()
    for item in ttl_item_url:
        item_url = "https://www.trademe.co.nz" + item
        content_of_itempage = content_of_webpage(item_url, headers)
        item_diction = item_dict(content_of_itempage)
        item_diction["item_url"] = item_url
        all_item_extract.append(item_diction)
        keys_list = keys_list.union(set(list(item_diction.keys())))
    
    outfile(filename, all_item_extract, keys_list)
    
    print("Csv file has been successfully exported!")

# Call the main function to run the program
main()