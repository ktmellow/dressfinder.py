"""
note to self:
approximately 26460 dresses on threadflip.com since 26 Aug 2015 10:55am
test measurements - 29-30 bust, 26-29 waist, 39-42 length
"""

#! python3
# dressfinder uses threadflip.com's api and user descriptions
# to find size-matched dresses in inches

import json
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Ask for size measurements and save as variables.
min_bust = float(input("Enter minimum bust size in inches: "))
max_bust = float(input("Enter maximum bust size in inches: "))
min_waist = float(input("Enter minimum waist size in inches: "))
max_waist = float(input("Enter maximum waist size in inches: "))
min_length = float(input("Enter minimum dress length in inches: "))
max_length = float(input("Enter maximum dress length in inches: "))
 
# Initial call to API finds the total pages (total calls to API)
initial_response = requests.get('http://www.threadflip.com/api/v3/items?attribution%5Bapp%5D=web&item_collection_id=&type_ids=3&q=&page=1&page_size=100') 
json_data = json.loads(initial_response.text)
total_pages = json_data['pagination']['total_pages'] # type int

"""
# Each call to API is stored as a .json file. 
for i in range(1, total_pages + 1):
    page = str(i)
    page_response = requests.get('http://www.threadflip.com/api/v3/items?attribution%5Bapp%5D=web&item_collection_id=&type_ids=3&q=&page='+page+'&page_size=100')
    page_json_data = json.loads(page_response.text)
    with open('json_file%s.json' % i, 'w') as g:
        json.dump(page_json_data, g)
  

# Writing JSON data
#with open('data.json', 'w') as f:
#     json.dump(data, f)

# Reading data back
#with open('data.json', 'r') as f:
#     data = json.load(f)

"""

# Check each file for dresses that match user-defined measurements. 
match_list = []
for i in range(1, total_pages + 1):
    page = str(i)
    with open('json_file%s.json' % i, 'r') as f:
        current_page = json.load(f)
    
    for i in range(len(current_page['items']) -1):
        try:
            dress_text = str(current_page['items'][i]['description'])
            bust_regex = re.compile(r"ust:(\d)?(\d\d)|ust: (\d)?(\d\d)|ust.(\d)?(\d\d)|ust(\d)?(\d\d)")
            bust_description = bust_regex.search(dress_text)
            bust_number_regex = re.compile(r"(\d)?(\d)(\d)")
            dress_bust = float(bust_number_regex.search(bust_description.group()).group())

            waist_regex = re.compile(r"aist:(\d)?(\d\d)|aist: (\d)?(\d\d)|aist.(\d)?(\d\d)|aist(\d)?(\d\d)")
            waist_description = waist_regex.search(dress_text)
            waist_number_regex = re.compile(r"(\d)?(\d)(\d)")
            dress_waist = float(waist_number_regex.search(waist_description.group()).group())   

            length_regex = re.compile(r"ength:(\d)?(\d\d)|ength: (\d)?(\d\d)|ength.(\d)?(\d\d)|ength(\d)?(\d\d)")
            length_description = length_regex.search(dress_text)
            length_number_regex = re.compile(r"(\d)?(\d)(\d)")
            dress_length = float(length_number_regex.search(length_description.group()).group())
                
            if (
              dress_bust <= max_bust and
              dress_bust >= min_bust and
              dress_waist <= max_waist and
              dress_waist >= min_waist and
              dress_length <= max_length and
              dress_length >= min_length):
                print("Found a dress your size!")
                match_list.append(current_page['items'][i]['full_url'])
                print(match_list)
            else:
                print("Not your size, sorry.") 
        except:
            print("Could not find measurements or dress is sold.")
            continue # del line if errors

print("All done with matching, now opening your dresses in browser!")
browser = webdriver.Firefox()
for i in range(len(match_list)):
    browser.find_element_by_tag_name("body").send_keys(Keys.CONTROL + "t")
    browser.get(match_list[i])

print("Check the dresses in your browser. Enjoy.") 
