# This file scrapes information from news articles and adds them to a sql
# database

# Adds FormatScrapers and HelperLibraries folders to Path
import sys
sys.path.insert(0, 'FormatScrapers')
sys.path.insert(0, 'HelperLibraries')

# Imports necessary libraries
from bs4 import BeautifulSoup as soup
from Creds import *
from format1Scraper import getArticleInfoFormat1
from format2Scraper import getArticleInfoFormat2
from format3Scraper import getArticleInfoFormat3
from format4Scraper import getArticleInfoFormat4
from StringHelpers import *
from sqlalchemy import create_engine
import bs4
import datetime
import pandas as pd
# import pymssql
import re
import requests
import time

# Creates global variables

# List of domains we plan to scrape
domains = ([# 'https://abcnews.go.com', Y
# 'https://www.dailywire.com/', Y
# 'https://www.latimes.com', N
# 'https://www.cnn.com', N
# 'https://www.miamiherald.com', N
# 'https://www.univision.com/univision-news', Y
# 'https://www.foxbusiness.com', N
# 'https://www.foxnews.com', N
# 'https://www.nbcnews.com', Y
# 'https://www.theguardian.com' N
# 'https://theintercept.com', N
# WSJ P
# NY Times P
# 'https://www.washingtonpost.com', P
# 'https://www.dailymail.co.uk/home/index.html', Y
])

# List of categories the articles will be in
categories = (['business',
'entertainment',
'health',
'opinion',
'politics',
'us',
'world'])

# List of month abbreviations
months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct',
'nov', 'dec']

# List of units of time that may be found in dates
unitsOfTime = ['second', 'minute', 'hour', 'day']

################################################################################
# BEGIN SCRAPING HELPER FUNCTIONS
################################################################################

# Takes in a list of lists of elements and returns a flattened list of elements
def flatten(lst):
    newList = []
    for l in lst:
        newList += l
    return newList

# Takes in a time as a string in the form HH:MM, and another string that's
# either 'AM' or 'PM,' and returns a tuple of ints: the first int represents the
# hour in a 24-hour clock, and the second represents the minutes
def getTime(time, ampm):
    timeList = time.split(":")
    if ((ampm == "AM") & (timeList[0] != "12")) | ((ampm == "PM") & (timeList[0] == "12")):
        return int(timeList[0]), int(timeList[1])
    elif (ampm == "AM"):
        return 0, int(timeList[1])
    else:
        return int(timeList[0])+12, int(timeList[1])

# Takes in a URL and returns a bs4 element containing the html code from that
# URL
def getSoup(url):
    print('Here 1')
    # Connects to the main domain page and gets the HTML code from that page
    page_html = requests.get(url).text
    print('Here 2')
    # Turns the html code into a soup and returns it
    return soup(page_html, "html.parser")

# Takes in an element and returns a category it is associated with. Returns an 
# empty string if the element is not associated with any categories 
def getAssociatedCategory(element):

    # Imports global variable
    global categories

    # Checks if this is a tag and if it has an href
    if (type(element) == bs4.element.Tag) and ('href' in element.attrs.keys()):

        # Splits the href and formats each substring within the href
        subStrings = list(map(formatString, element['href'].split('/')))

        length = len(subStrings)
        i = 0

        # Goes through each substring and checks if it matches one of the 
        # desired categories
        while (i < length) and (subStrings[i] not in categories):
            i += 1

        if i < length:
            return subStrings[i]
    return ''

# Takes in a soup and returns a list of tuples of all the links within the soup
# that are associated to one of the desired categories along with the category
# each link is associated with
def getRelevantLinks(soup):
    acc = []
    for element in soup.descendants:
        if getAssociatedCategory(element) != '':
            acc.append((getAssociatedCategory(element), element['href']))
    return acc

# Takes in a domain and a link, and adds the domain or https:// to the link if 
# necessary
def formatStartOfLink(domain, link):
    # Adds a domain if necessary
    link = link.lower()
    if ('.com' not in link) and ('.org' not in link) and ('.net' not in link):
        link = domain + link

    # Adds https:// if necessary
    elif ('//' == link[:2]):
        link = link[2:]
    if ('https://' != link[:8]):
        link = 'https://' + link
    return link
    
# Takes in a domain (string), a tuple containing a category (string) and a link 
# (string) and returns a link (string) formatted so that it accesses the 
# domain's main webpage for that category
def formatLink(domain, linkTuple):

    # Unpacks the link tuple
    category = linkTuple[0]
    link = linkTuple[1]

    link = formatStartOfLink(domain, link)
    # Finds the segment within the link that matches the category
    subStrings = link.split('/')
    i = 0
    length = len(subStrings)
    while (i < length) and (formatString(subStrings[i]) != category):
        i += 1
    
    # Stores that segment
    subString = subStrings[i]

    # Finds the index of the segment within the link
    index = link.find(subString)

    # Cuts off anything after the segment, and returns a link that points to the
    # domain's main page for that category
    return (category, link[:(index+len(subString))])

# Takes in a list of tuples containing categories (as a string) and links (as a 
# string), and returns a set of tuples containing categories and links to the
# domain's main webpage for each category
def getCategoryLinks(domain, linkTuplesList):

    # Formats the links so that they are all links to main webpages in the
    # domain
    func = lambda linkTuple : formatLink(domain, linkTuple)
    formattedLinks = list(map(func, linkTuplesList))

    # Returns a set of tuples containing a category (string) and a link (string)
    return set(formattedLinks)

# Takes in a bs4.element and retrurn True if it is a tag, and if it has an href
def getArticle(element):
    if ((type(element) == bs4.element.Tag) and
    ('href' in element.attrs.keys())):
        return True
    else:
        return False

def getScore(articleInfo):
    global lastUpdate
    return (articleInfo['updateTime'] - lastUpdate).total_seconds()

# Takes in a url to an article, a domain, a category, and an update time, and, 
# if the article was updated after the last update time, returns the author,
# category, headline, image, link, score, subheadline, and update time of the
# article the link points to. Returns an empty list otherwise.
def getArticleInfo(articleLink, category, domain, lastUpdate):

    # Tries to get the soup for the article
    try:
        page_html = getSoup(articleLink)
    except:
        print('Could not access: ' + articleLink)
        return None

    # Tries to get the information from the link assuming the format of the
    # website is similar to the format of
    # https://abcnews.go.com/Politics/wireStory/extraordinary-warning-trump-10-p
    # entagon-chiefs-75029997?cid=clicksource_4380645_2_heads_hero_live_headline
    # s_hed
    articleInfo = getArticleInfoFormat1(page_html)
    if (articleInfo != None):
        if (articleInfo['updateTime'] > lastUpdate):
            articleInfo['score'] = getScore(articleInfo)
            return articleInfo
        else:
            return None

    # Tries to get the information from the link assuming the format of the
    # website is similar to the format of
    # https://www.cnn.com/2021/01/06/health/south-africa-sequencing-coronavirus-
    # variant/index.html
    articleInfo = getArticleInfoFormat2(page_html)
    if (articleInfo != None):
        if (articleInfo['updateTime'] > lastUpdate):
            articleInfo['score'] = getScore(articleInfo)
            return articleInfo
        else:
            return None


    # Tries to get the information from the link assuming the format of the
    # website is similar to the format of
    # https://www.foxbusiness.com/real-estate/3d-printed-buildings-california-ho
    # using-crisis
    articleInfo = getArticleInfoFormat3(page_html)
    if (articleInfo != None):
        if (articleInfo['updateTime'] > lastUpdate):
            articleInfo['score'] = getScore(articleInfo)
            return articleInfo
        else:
            return None
    
    # Tries to get the information from the link assuming the format of the
    # website is similar to the format of 
    # https://www.nbcnews.com/news/us-news/nick-ut-photojournalist-who-made-fame
    # d-vietnam-war-napalm-girl-n1254517
    articleInfo = getArticleInfoFormat4(page_html)
    if (articleInfo != None):
        if (articleInfo['updateTime'] > lastUpdate):
            articleInfo['score'] = getScore(articleInfo)
            return articleInfo
        else:
            return None

    # Returns None if the potential article did not match any format
    return None

# Takes in a category, domain, update time, and link, and returns a list of all
# the authors, categories, headlines, images, links, scores, subheadlines, and
# update times of all the articles on the link that were updated after the 
# given update time.
def getArticles(category, domain, lastUpdate, mainLink):

    print('Mainlink: ' + mainLink)
    # Gets the soup element for the mainLink
    page_html = getSoup(mainLink)
    
    # Gets all descendants of the main soup element, and filters them using 
    # getArticle
    filteredDescendants = list(set(filter(getArticle, list(page_html.descendants))))

    # Gets all links from the list of descendants and formats them if necessary
    getLink = lambda element: formatStartOfLink(domain, element['href'])
    articleLinks = list(set(map(getLink, filteredDescendants)))

    # Initializes link list and dictionary list to store all the articles we
    # find
    artLinks = []
    artDictionaries = []

    # func = lambda articleLink : getArticleInfo(articleLink, domain, category, lastUpdate)
    # articlesInfo = list(map(func, articleLinks))
    count = 0
    for articleLink in articleLinks:

        # This if-statement is here in order to avoid the error I was getting
        # where a link, â, would print and the program would stop working
        if 'â' in articleLink:
            continue
        # print(articleLink)
        articlesInfo = getArticleInfo(articleLink, domain, category, lastUpdate)

        print(articleLink)
        # Checks if article info was actually found
        if articlesInfo != None:

            # Checks if the article is already in the list
            if articleLink not in artLinks:

                count += 1
                print(count)

                # Adds a category and link item to the article dictionary
                articlesInfo['category'] = category
                articlesInfo['link'] = articleLink

                # Adds dictionary and link to the list of found articles
                artDictionaries.append(articlesInfo)
                artLinks.append(articleLink)


    return artDictionaries

# Takes in a list of dictionaries, dicts, and a key, k, and returns a shortened
# list of dictionaries such that no two dictionaries have the same value at key
# k
def removeDuplicateDicts(dicts, key):
    getValue = lambda dic : dic[key]
    values = list(set(list(map(getValue, dicts))))
    isInList = [False for i in values]

    newDicts = []
    for dic in dicts:
        index = values.index(dic[key])
        if not(isInList[index]):
            newDicts.append(dic)
            isInList[index] = True
    
    return newDicts

################################################################################
# END SCRAPING HELPER FUNCTIONS
################################################################################

# Takes in a pandas dataframe and adds it to a database
def addToDatabase(database, dataframe, password, server, user):

    # Connects to the database
    connection = create_engine('mssql+pymssql://'+user+':'+password+'@'+server+'/'+database)

    # Adds data to dataframe
    dataframe.to_sql('ArticleInfo', con=connection, if_exists='append', index=False)

# Takes in a domain and a time, and returns a dataframe of all the articles 
# from that domain that have been updated after the given time
def domainScrape(domain, lastUpdate):
    print(domain)

    # Imports global variable
    global categories

    # Gets a bs4 element containing the html code for each domain
    pageSoup = getSoup(domain)

    # Gets a list of all relevant attributes from within the soup
    linkTuplesList = getRelevantLinks(pageSoup)

    # Selects a subset of the links from the list above that only contains links
    # to the main categories in the website
    categoryLinkTuples = getCategoryLinks(domain, linkTuplesList)
    for x in categoryLinkTuples:
        print(x)

    # Initializes lists that will store all the author, categories, headlines,
    # images, links, scores, sub-headlines, and update times for each article
    allArticles = []

    # Goes through each tuple and gets a cetegory, headline, sub-headline, link
    # image, update time, author, and a score for each article found on each 
    # category link. Returns a list for each one of these elements
    func1 = lambda clt: getArticles(clt[0], domain, lastUpdate, clt[1])
    allArticles = removeDuplicateDicts(flatten(list(map(func1, categoryLinkTuples))), 'link')
    
    # Converts the list of dictionaries into 2D array by replacing each 
    # dictionary with a 1D list
    articleArray = list(map(lambda x : x.values(), allArticles))

    # Converts the 2D array into a pandas dataframe
    articlesDF = pd.DataFrame(articleArray, columns=['Author', 'Headline',
    'SubHeadline', 'Image', 'UpdateTime', 'Score', 'Category', 'Link'])

    # Returns the dataframe
    return articlesDF

lastUpdate = datetime.datetime(2021, 1, 23, 23, 33)
func = lambda x : domainScrape(x, lastUpdate)

for domain in domains:
    func(domain)