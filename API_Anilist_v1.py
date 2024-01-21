##########################################
# With requests method, taking all the entry from a dinamyc website and copiyng them on a note on the desktop.
# Problem: Only a part of the entry taken (until letter "D").
# Solution: Load all the entry before.
##########################################

from datetime import datetime
import json
import requests
from bs4 import BeautifulSoup

# Url
OG_Url = 'https://anilist.co/user/Cesa00/animelist'

# requests
response = requests.get(OG_Url)
results = BeautifulSoup(response.content, features="html.parser")

# creating lists
Watching_list = []
Completed_list = []
Planning_list = []
Rewatching_list = []
Dropped_list = []

# parsing
tot_elements = results.find_all("div", class_="list-wrap")
for tot_element in tot_elements:

    # section
    status_element = tot_element.find("h3", class_="section-name")
    status_element = status_element.text.strip().upper()
    
    # title
    links = tot_element.find_all("a")
    for link in links:
        link = link.text.strip().lower().capitalize()

        # populating lists
        if status_element == "WATCHING":
            Watching_list.append(link)
        elif status_element == "REWATCHING":
            Rewatching_list.append(link)
        elif status_element == "COMPLETED":
            Completed_list.append(link)
        elif status_element == "PLANNING":
            Planning_list.append(link)
        elif status_element == "DROPPED":
            Dropped_list.append(link)

##
## SAVING ON FILE
##
# get current date and time
current_date = datetime.now().strftime("%Y-%m-%d")
print("Current date: ", current_date)
 
# convert datetime obj to string
str_current_datetime = str(current_date)

# dictionary with lists and total length
lines = {
        "WATCHING": [len(Watching_list), Watching_list],
        "REWATCHING": [len(Rewatching_list), Rewatching_list],
        "DROPPED": [len(Dropped_list), Dropped_list],
        "COMPLETED": [len(Completed_list), Completed_list],
        "PLANNING": [len(Planning_list), Planning_list]
        }

# file
with open('Anilist ' + str_current_datetime + '.txt', 'w') as list:
    json.dump(lines, list, indent=3)
print("Done writing dict into .txt file")

