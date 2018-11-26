#! /usr/bin/env python3

# eBayTerminalFirefox.py - This python program is run through
# terminal. In terminal, it takes user input then searches for
# it on eBay with new, buy it now, and sold for settings on.
# It collects how many new and buy it now items are available
# and the cost of those items. It then collects the sold for
# items and the price they sold for. It returns those items
# to a CSV file currently called check.csv.

# Possibly added later: Date sold. Running automatically at
# a certain time of day. Automatically producing a report and
# maybe also sending it.

# The following is where the prgram is stored.
# /Users/user/Documents/Web_Scraping/eBayTerminalFirefox.py

# Takes user input when run in terminal and returns the price of
# current new buy it now items, how many items are available,
# the number of sold items from the last 60 days (or how far
# back eBay goes with sold items).

import re
import lxml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import firefox
import os
import bs4
from bs4 import BeautifulSoup
import csv
import openpyxl

# Checks that the driver option is working.
driver_option = webdriver.FirefoxOptions()
print(type(driver_option))

# Asks for the search terms (searchTems) from the user in terminal.
print("Enter eBay search terms: ")
searchTerms = input()
print("You entered " + searchTerms)

# Firefox is opened remotely using selenium.
firefoxdriver = "/Users/user/WebDriver_ExeFiles/geckodriver"
os.environ["webdriver.firefox.driver"] = firefoxdriver
driver = webdriver.Firefox(executable_path=firefoxdriver)
print(type(driver))
driver.get('https://www.ebay.com')

# Finds search box, and tells the user if is able to find it.
try:
    elem = driver.find_element_by_id(
        "gh-ac-box2"
    )
    print('The search box has been found.')
    print('Found <%s> element with that id!' % (elem.tag_name))
except Exception:
    print("Did not find search box.")

# Where the actual search terms are inputted and the search is
# is submitted. Submitted means the button to carry out the
# search is clicked.
searchElem = driver.find_element_by_xpath(
    "//input[@type='text'][@class='gh-tb ui-autocomplete-input']"
)
searchElem.send_keys(searchTerms)
searchElem.submit()
print('The search terms were submitted sucessfully.')

# Waits just in case that is necessary.
driver.implicitly_wait(5)

# Click new, collect the amount of new and buy it now items
# are available, then clicks buy it now.
# Also checks that these options worked.
try:
    # Clicks new
    newElem = driver.find_element_by_xpath(
        '//input[@type="checkbox"][@aria-label="New"][@class="cbx x-refine__multi-select-checkbox "]'
    )
    newElem.click()
    print('Clicking the new element worked.')
except Exception:
    print("Did not click the new option.")

# Waits just in case that is necessary.
driver.implicitly_wait(100)

# Collects the number of new buy it now items are available
# then matches which part of that output is digits. An integer
# is returned.
sourceNew = driver.page_source
soupNew = BeautifulSoup(sourceNew, 'lxml')
availNum = soupNew.find(
    "span", {"class": "x-refine__multi-select-cbx"}, text="Buy It Now"
).next_sibling.get_text(strip=True)
# Turns it to an integer instead of a list with parenthsis.
numExtract = re.compile("\d+")
availMatch = numExtract.search(availNum).group()
print(availMatch)
availNow = int(availMatch)
print(
    "The number of items that are new and buy it now items is: " + availMatch
)

try:
    # Clicks buy it now.
    buyItNowElem = driver.find_element_by_xpath(
        """//div[@id='w3-w0-singleselect[8]']
        /a[@class='rbx x-refine__single-select-link']
        /span[@class='x-refine__multi-select-histogram']"""
    )
    print(buyItNowElem.is_enabled())
    buyItNowElem.click()
    print('Buy it now was clicked.')
except Exception:
    print("Unable to click the buy it now option.")


# Collects all the prices for buy it now new items.
sourcePrice = driver.page_source
soupPrice = bs4.BeautifulSoup(sourcePrice, 'lxml')
priceElem = soupPrice.find_all("span", {"class": "s-item__price"})
extractPrice = [span.get_text() for span in priceElem]
print("The prices for items available are: ")
print(extractPrice)

# Click sold for and collect how many items sold in the last 60 days.
try:
    # Clicks sold for
    soldForElem = driver.find_element_by_xpath(
        "//input[@type='checkbox'][@aria-label='Sold Items']"
    )
    soldForElem.click()
    print('Clicking sold for element worked.')
except Exception:
    print("Did not click the sold for option.")

# Has driver wait just in case.
driver.implicitly_wait(100)

# Collects the numnber of items sold in the last 60 days.
sourceSoldFor = driver.page_source
soupSoldFor = bs4.BeautifulSoup(sourceSoldFor, 'lxml')
availSold = soupSoldFor.find("h1")
print(availSold)
soldForNum = availSold.string
print("The number of sold for items is: " + soldForNum)
soldFor = numExtract.search(soldForNum).group()
# numExtract regex made earlier.
soldForFinal = int(soldFor)
print("The number of sold for items as an integer is: " + soldFor)

# Prices for all the items sold recently.
sourceSold = driver.page_source
soupSold = bs4.BeautifulSoup(sourceSold, 'lxml')
soldElem = soupSold.find_all("span", {"class": "POSITIVE"})
extractSoldFor = [span.get_text() for span in soldElem]
print("The prices for sold for items are: ")
print(extractSoldFor)

# Sets the path to the csv file.
os.path.join(
    'Users', 'Atom_Practice',
    'Web_Scraping_Practice', 'check.csv'
)

# Opens the check.csv file and adds infomation to it.
with open('check.csv', 'w', newline='') as eBayObjFile:
    w = csv.writer(eBayObjFile, delimiter=',')
    w.writerow([searchTerms, availNow, soldForFinal])
    w.writerow(extractPrice)
    w.writerow(extractSoldFor)

print("The csv file was opened and had data inserted. It closed")
print("automatically.")

# Close eBay.
driver.close()

# Confirms in terminal that the program has run successfully.
print('The program successfully completed and is DONE.')

# To potentially add: Possible price categories in CSV.
# Open the spreadsheet automatically. Have it show a graph
# or a spreadsheet that already has formulas. Have the program
# run autimatically and return a report at the same time every
# day. This may work if there is a list to iterate over in terminal.
