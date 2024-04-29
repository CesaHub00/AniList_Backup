# **AniList_Backup**
Algorithm to create a backup note with all the watching/completed/planning/dropped series on anilist profile.

### [*Anilist_v1*](Anilist_v1.py) was the first program done.
- Using the *Requests* library to obtain the data and the *BeautifulSoup* library to analyze the content
- the section name and the series it contains are read and saved in the correspondents list
- then a file is created with the current date and populated with the section, series name, and total series in each section

But the series stop at the letter D because the web page is dynamic and not all the series are loaded at the same time.
To solve the problem the second program was created.

### [*Anilist_v2*](Anilist_v2.py) is the latest version and it is done with web scraping tools.
Instead of using the *Requests* library, a web scraping tool is used before the analysis phase with *BeautifulSoup*; to do so the *Selenium* library is used to import the *webdriver*.

The main core of the new version is to directly opend the web page and scroll it to the end with a pause between each scrolling action, to allow the page load all series, also the fully loaded page is given to the *BeautifulSoup* class to start the parsing phase, from this point on the algorith is the same as the first version.
