# import module
from datetime import datetime
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

# scroll page function
def scrolldown(Url):
    
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    SCROLL_PAUSE_TIME = 1.0

    driver.get(Url)
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    # getting the same page (in link) after full load
    get_url = driver.page_source

    # ready for parsing
    results = BeautifulSoup(get_url, features="html.parser")

    return results

# https://realpython.com/beautiful-soup-web-scraper-python/

OG_Url = 'https://anilist.co/user/Cesa00/animelist'

# driver intsall
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
options = webdriver.ChromeOptions()

# creatinglists
Watchinglist = []
Completedlist = []
Planninglist = []
Rewatchinglist = []
Droppedlist = []

# scroll results (view scroll page function)
results = scrolldown(OG_Url)

# parsing
tot_elements = results.find_all("div", class_="list-wrap")
for tot_element in tot_elements:

    # print section
    status_element = tot_element.find("h3", class_="section-name")
    status_element = status_element.text.strip().upper()
    
    # print title
    links = tot_element.find_all("a")
    for link in links:
        link = link.text.strip().lower().capitalize()

        if status_element == "WATCHING":
            Watchinglist.append(link)
        elif status_element == "REWATCHING":
            Rewatchinglist.append(link)
        elif status_element == "COMPLETED":
            Completedlist.append(link)
        elif status_element == "PLANNING":
            Planninglist.append(link)
        elif status_element == "DROPPED":
            Droppedlist.append(link)

##
## SAVING ON FILE
##
# get current date and time
current_date = datetime.now().strftime("%Y-%m-%d")
print("Current date: ", current_date)
 
# convert datetime obj to string
str_current_datetime = str(current_date)

lines = {
        "WATCHING": [len(Watchinglist), Watchinglist],
        "REWATCHING": [len(Rewatchinglist), Rewatchinglist],
        "DROPPED": [len(Droppedlist), Droppedlist],
        "COMPLETED": [len(Completedlist), Completedlist],
        "PLANNING": [len(Planninglist), Planninglist]
        }
with open('Anilist '+str_current_datetime+'.txt', 'w') as list:
    json.dump(lines, list, indent=3)
print("Done writing dict into .txt file")

