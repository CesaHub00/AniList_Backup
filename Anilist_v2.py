from datetime import datetime
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
from pathing import pathing


def main():

    # Url
    OG_Url = 'https://anilist.co/user/Cesa00/animelist'

    # scroll page function
    results = loadingPage(OG_Url)

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

    # dictionary with lists and total length
    lines = {
            "TOTAL": len(Watching_list) + len(Rewatching_list) + len(Dropped_list) + len(Completed_list) + len(Planning_list),
            "WATCHING": [len(Watching_list), Watching_list],
            "REWATCHING": [len(Rewatching_list), Rewatching_list],
            "DROPPED": [len(Dropped_list), Dropped_list],
            "COMPLETED": [len(Completed_list), Completed_list],
            "PLANNING": [len(Planning_list), Planning_list]
            }

    # saving on file
    fileCreation(lines)

    return "Backup done!"


# open the page, scroll to the bottom, saving and returning the page
def loadingPage(Url):

    # driver intsall
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    options = webdriver.ChromeOptions()

    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    SCROLL_PAUSE_TIME = 5.0

    # initiating web driver
    driver.get(Url)
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:

        # scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # getting the same page (in link) after full load
    get_url = driver.page_source

    # ready for parsing
    page_results = BeautifulSoup(get_url, features="html.parser")

    return page_results


def fileCreation(lines):

    # get current date and time
    current_date = datetime.now().strftime("%Y-%m-%d")
    print("Current date: ", current_date)

    # convert datetime obj to string
    str_current_datetime = str(current_date)

    # file
    with open(pathing + 'Anilist ' + str_current_datetime + '.txt', 'w') as list:
        json.dump(lines, list, indent=3)
    print("Wrote dict into .txt file")




if __name__ == "__main__":
    main()