"""
This version of the program fails to properly loop the pages of threadflip.com's dresses.
Using the browser's back button does nottake go to previous page,
but reloads the javascript web app to the first page of the dress listings.
Also, the site's javascript does not reveal href links in the html.
See other dressfinder file for a small working unit of this code. 
"""

#! python3
# dressfinder.py finds threadflip.com dresses of specified size range.
# recommended: clear cookies and browsing history prior to testing


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re


# Ask for size reqs and save as variables.
min_bust = float(input("Enter minimum bust size in inches: "))
max_bust = float(input("Enter maximum bust size in inches: "))
min_waist = float(input("Enter minimum waist size in inches: "))
max_waist = float(input("Enter maximum waist size in inches: "))
min_length = float(input("Enter minimum dress length in inches: "))
max_length = float(input("Enter maximum dress length in inches: "))

start_page = "http://www.threadflip.com/shop/category/clothing/dresses"
browser = webdriver.Firefox()
browser.get(start_page)


# Look up last page by html "page" element and click it. 
page_count = len(browser.find_elements_by_class_name("page"))
pages_list = browser.find_elements_by_class_name("page")
for i in range(page_count):
    pages_list[i] = str(browser.find_elements_by_class_name("page")[i].text)
last_page = str(max(pages_list))
last_page_id = "page-" + last_page 
browser.find_element_by_id(last_page_id).click()

# All dress size matches will be stored in this list. 
match_list = []

# Loop through all pages, from last page to page 1. 
while browser.current_url != start_page:
    
    # Create a list with the same number of items on the page by searching for the item class.
    link_list = [] # most recent update
    page_dresses = browser.find_elements_by_class_name("js-image-link") 
    link_list = list(page_dresses)

    # Replace list placeholders with actual links found from the item class. 
    for dress in range(len(link_list)):
        link_list[dress] = page_dresses[dress].get_attribute("href")

    dress_bust = float()
    dress_waist = float()
    dress_length = float()

    #Loop the links for checking the size of each dress against user input. 
    for link in range(len(link_list)):
        browser.get(link_list[link])
        print(link_list[link])

        dress_text = browser.find_element_by_id("js-sip-description").text

        try:   
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
              dress_length >= min_length and
              link == len(link_list) - 1):
                print("Found a dress your size!")
                match_list.append(link_list[dress])
                print(match_list)
                for link in range(len(link_list) - 1):
                    browser.back()  # This clicks back button multiple times, past item URL's, until you can click for previous page.
            elif (
              dress_bust <= max_bust and
              dress_bust >= min_bust and
              dress_waist <= max_waist and
              dress_waist >= min_waist and
              dress_length <= max_length and
              dress_length >= min_length): 
                print("Found a dress your size!")
                match_list.append(link_list[dress])
                print(match_list)
            else:
                print("Not your size, sorry.") 
                if link == len(link_list) - 1:
                    for link in range(len(link_list) - 1):
                        browser.back()
                else:
                    continue 
        except AttributeError:
            print("Could not find measurements or dress is sold.")
            if link == len(link_list) - 1:
                for link in range(len(link_list) - 1):
                    browser.back()
                continue
            else:
                continue

print("All done with matching, now opening your dresses in browser!")

for i in range(len(match_list)):
    browser.find_element_by_tag_name("body").send_keys(Keys.CONTROL + "t")
    browser.get(match_list[i])

print("Check the dresses in your browser. Enjoy.") 