# This file scrapes information from news articles and adds them to a sql
# database

# Imports necessary libraries
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import bs4
import datetime
import pandas as pd
import requests
import time
import re
import urllib.error

# Creates global variables

# List of domains we plan to scrape
domains = (['https://abcnews.go.com',
'https://www.cnn.com',
'https://www.foxbusiness.com',
'https://www.foxnews.com',
'https://www.nbcnews.com',
'https://www.theguardian.com'])

# List of categories the articles will be in
categories = (['business',
'entertainment',
'health',
'opinion',
'politics',
'us',
'world'])

# List of month abbreviations
months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

# List of units of time that may be found in dates
unitsOfTime = ['second', 'minute', 'hour', 'day']

################################################################################
# BEGIN STRING FORMATTING FUNCTIONS
################################################################################
# A set of helper functions used when formatting strings
     
def remove_punc(text):
    exclude = '.,;!? '
    for punc in exclude:
        text = text.replace(punc, '')
    return text

def lower(text):
    return text.lower()

def replaceDash(s):
  return s.replace("—", " ").replace("-", " ")

def replaceApostrophe(s):
  return s.replace("'", " ")

def replaceNumbers(s):
  if s == "0":
    return "zero"
  elif s == "1":
    return "one"
  elif s == "2":
    return "two"
  elif s == "3":
    return "three"
  elif s == "4":
    return "four"
  elif s == "5":
    return "five"
  elif s == "6":
    return "six"
  elif s == "7":
    return "seven"
  elif s == "8":
    return "eight"
  elif s == "9":
    return "nine"
  else:
    return s

def removeNews(s):
    return s.replace('news','')

# Takes in a string an return a lowercase verions without punctuation, capital 
# letters, dashes, apostrophes, numbers, and the word news
def formatString(s):
    return removeNews(remove_punc(replaceNumbers(replaceDash(replaceApostrophe(lower(s))))))

################################################################################
# END STRING FORMATTING FUNCTIONS
################################################################################

################################################################################
# BEGIN SCRAPING HELPER FUNCTIONS
################################################################################

# Takes in a list of lists of elements and returns a flattened list of elements
def flatten(lst):
    newList = []
    for l in lst:
        newList += l
    return newList

# Takes in a month's name or abreviation as a string an returns a number
# corresponding to that month
def monthString2Int(monthString):
    if ((monthString == "January") | (monthString == "Jan")):
        return 1
    elif ((monthString == "February") | (monthString == "Feb")):
        return 2
    elif ((monthString == "March") | (monthString == "Mar")):
        return 3
    elif ((monthString == "April") | (monthString == "Apr")):
        return 4
    elif (monthString == "May"):
        return 5
    elif ((monthString == "June") | (monthString == "Jun")):
        return 6
    elif ((monthString == "July") | (monthString == "Jul")):
        return 7
    elif ((monthString == "August") | (monthString == "Aug")):
        return 8
    elif ((monthString == "September") | (monthString == "Sep") | (monthString == 'Sept')):
        return 9
    elif ((monthString == "October") | (monthString == "Oct")):
        return 10
    elif ((monthString == "November") | (monthString == "Nov")):
        return 11
    elif ((monthString == "December") | (monthString == "Dec")):
        return 12
    else:
        raise Exception('Month not Recognized')

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

    # Connects to the main domain page and gets the HTML code from that page
    page_html = requests.get(url).text

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
        i =0

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

def containsDateTimeElement(s):
    global months
    global unitsOfTime
    if len(s) > 100:
        return False

    formattedS = s.lower()
    index = 0
    length = len(months)
    while ((index < length) and ((months[index] not in formattedS))):
        index += 1
    if index < length:
        n = 0
        while ((n < 10) and (str(n) not in s)):
            n += 1
        if n < 10:
            return True
    else:
        index = 0
        length = len(unitsOfTime)
        while ((index < length) and ((unitsOfTime[index] not in formattedS))):
            index += 1
        if (index < length) and ('ago' in formattedS):
            return True
        else:
            return False
    return False

# Takes in a bs4 soup object, finds an update time for it, and returns it. If no
# update time is found, returns None
def getUpdateTime(page_html):
    global months

    # Checks if any element in the page has a date element
    potentialDateTimes = page_html.find_all(string=containsDateTimeElement)

    if len(potentialDateTimes) > 0:
        for dt in potentialDateTimes:
            s = dt.lower().split()
            if ('updated' in s) or ('modified' in s) or ('ago' in s):

                # Tries to find a date in the format 'month day, year'
                for month in months:
                    if (month in s):
                        i = s.index(month)
    else:
        print('No dates found')
        return None

    # Checks if there is a date in the header
    # headers = page_html.find_all('header')
    # if (len(headers) > 0):
    #     dates = headers[0].find_all(string=containsDateTimeElement)
    #     if len(dates) > 0
    #         return dates[0]
    
    # Checks if there is an article with

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

# Takes in a bs4 soup containing the html code from a article's webpage, and
# returns a dictionary containing the author, headline, image, score,
# sub-headline, and update time of the article. Assumed format: https://abcnews.
# go.com/Politics/wireStory/extraordinary-warning-trump-10-pentagon-chiefs-75029
# 997?cid=clicksource_4380645_2_heads_hero_live_headlines_hed
def getArticleInfoFormat1(page_html):
    
    articleWrappers = page_html.find_all(class_='Article__Wrapper')
    if len(articleWrappers) > 0:
        articleWrapper = articleWrappers[0]
    else:
        return None
    
    headers = articleWrapper.find_all('header')

    if len(headers) > 0:
        authorSection = headers[0].find_all(class_=re.compile('Author'))[0]
        if len(authorSection) > 0:
            authorStrings = authorSection.get_text().split()
            author = authorStrings[0] + ' ' + authorStrings[1]
        else:
            return None
    else:
        return None

    h1s = headers[0].find_all('h1')[0]
    if len(h1s) > 0:
        headline = h1s.get_text()
    else:
        return None
    
    h2s = headers[0].find_all('h2')
    ps = articleWrapper.find_all('p')
    if len(h2s) > 0:
        subHeadline = h2s[0].get_text()
    elif len(ps) > 0:
        subHeadline = ps[0].get_text()
        if len(subHeadline) > 100:
            subHeadLine = subHeadline[:100]
    else:
        return None

    pictures = articleWrapper.find_all('figure', class_=re.compile('Image'))
    if len(pictures) > 0:
        image = pictures[0].find_all('img')[0]['src']

        if image[:8] != 'https://':
            image = ''
    else:
        image = ''

    times = articleWrapper.find_all(class_=re.compile('Time'))
    if len(times) > 0:
        dateList = times[0].get_text().split()
        if (dateList[4].lower() == 'am') or (dateList[4].lower() == 'pm'):
            hour, minutes = getTime(dateList[3], dateList[4])
        else:
            hhmm = dateList[3].split(':')
            hour = int(hhmm[0])
            minutes = int(hhmm[1])
        updateTime = (datetime.datetime(int(dateList[2][:-1]), \
            monthString2Int(dateList[0]), int(dateList[1][:-1]), hour, minutes))
    else:
        return None
    
    return ({'author': author,
    'headline' : headline,
    'subHeadline' : subHeadline,
    'image' : image,
    'updateTime' : updateTime})

# Takes in a bs4 soup containing the html code from a article's webpage, and
# returns a dictionary containing the author, headline, image, score,
# sub-headline, and update time of the article. Assumed format: https://www.cnn.
# com/2021/01/06/health/south-africa-sequencing-coronavirus-variant/index.html
def getArticleInfoFormat2(page_html):

    # Gets the metadata seciont of the article, which contains the information
    # about the author and update time
    metadata = page_html.find_all(class_='metadata')

    # Checks if a metadata section was found
    if len(metadata) > 0:

        # Looks for an author secion in the metadata section, and, if it is
        # found, looks for a Tag of type 'a'
        authorSection = metadata[0].find_all(class_=re.compile('author'))
        if len(authorSection) > 0:
            authorTag = authorSection[0].find_all('a')

            # If the authorTage is found, gets the text from that tag. Otherwise,
            # get the text from the authorSection and modify it
            if len(authorTag) > 0:
                author = authorTag[0].get_text()
            else:
                authorStringList = authorSection[0].get_text().split()
                author = authorStringList[1] + ' ' + authorStringList[2]
        else:
            return None
    else:
        return None

    # Looks for an h1 element, and, if found, selects its text as the headline
    h1s = page_html.find_all('h1')
    if len(h1s) > 0:
        headline = h1s[0].get_text()
    else:
        return None
    
    # Loops for a p element with 'body' in its class name, and, if found, puts 
    # the first 100 characters of its text as the subHeadline
    ps = page_html.find_all('p', class_ = re.compile('body'))
    if len(ps) > 0:
        subHeadline = ps[0].get_text()
        if len(subHeadline) > 100:
            subHeadLine = subHeadline[:100]
    else:
        return None

    # Looks for elements with 'body' in their class names
    body = page_html.find_all(class_ = re.compile('body'))

    # Then, looks in the second body element for img elements with
    # 'media__image' in the class name
    pictures = body[1].find_all('img', class_=re.compile('media__image'))

    # Sets image as the first element's src if an element is found, and, sets 
    # image to an empty string otherwise
    if len(pictures) > 0:
        image = pictures[0]['src']
        if image[:8] != 'https:':
            image = 'https:' + image
    else:
        image = ''

    # Looks for element with 'update-time' in their class name
    times = metadata[0].find_all(class_=re.compile('update-time'))

    # If an element if found, takes the text from the first element and turns it
    # into a list of strings
    if len(times) > 0:
        dateList = times[0].get_text().split()

        # Checks if there is a colon in the hour-minute string or not, and 
        # divides it accordingly
        if ':' in dateList[1]:
            hhmm = dateList[1].split(':')
            hour = int(hhmm[0])
            minutes = int(hhmm[1])
        else:
            hhmm = dateList[1]
            hour = int(hhmm[:2])
            minutes = int(hhmm[2:])

        # Creates the updateTime element
        updateTime = (datetime.datetime(int(dateList[7]), \
            monthString2Int(dateList[5]), int(dateList[6][:-1]), hour, minutes))
    else:
        return None
    
    # Creates and returns the dictionary
    return ({'author': author,
    'headline' : headline,
    'subHeadline' : subHeadline,
    'image' : image,
    'updateTime' : updateTime})

# Takes in a bs4 soup containing the html code from a article's webpage, and
# returns a dictionary containing the author, headline, image, score,
# sub-headline, and update time of the article. Assumed format: https://www.foxb
# usiness.com/real-estate/3d-printed-buildings-california-housing-crisis
def getArticleInfoFormat3(page_html):
    global months
    global unitsOfTime
    
    # Gets the author
    authorSection = page_html.find_all(class_ = re.compile('author'))
    if len(authorSection) > 0:
        a = authorSection[0].find_all('a')
        if len(a) > 0:
            author = a[0].get_text()
            # print('Author: ' + author)
        else:
            return None
    else:
        return None

    # Gets the headline
    h1s = page_html.find_all('h1')
    if len(h1s) > 0:
        headline = h1s[0].get_text()
        # print('Headline: ' + headline)
    else:
        return None

    # Gets the sub-headline
    h2s = page_html.find_all('h2')
    if len(h2s) > 0:
        subHeadline = h2s[0].get_text()
        # print('Sub-Headline: ' + subHeadline)
    else:
        return None
    
    # Gets images
    articleBody = page_html.find_all(class_=re.compile('body'))
    if len(articleBody) > 0:
        imgs = articleBody[0].find_all('img')
        # for img in imgs:
        #     print(img['src'])
        if len(imgs) > 1:
            image = imgs[1]['src']
            # print('Image: ' + image)
        else:
            image = ''
    else:
        image = ''

    # Gets update time
    times = page_html.find_all('time')
    if len(times) > 0:
        timeStrings = times[0].get_text().split()
        currentTime = datetime.datetime.now()

        if timeStrings[-1] == 'ago':
            if (timeStrings[-2] == "hours") | (timeStrings[-2] == "hour"):
                delta = datetime.timedelta(0, 0, 0, 0, 0, -int(timeStrings[-3]))
            elif (timeStrings[-2] == "mins") | (timeStrings[-2] == "min"):
                delta = datetime.timedelta(0, 0, 0, 0, -int(timeStrings[-3]))
            elif (timeStrings[-2] == "days") | (timeStrings[-2] == "day"):
                delta = datetime.timedelta(-int(timeStrings[-3]))
            else:
                raise ValueError("datestring not accounted for")
            updateTime = currentTime + delta

        else:
            try:
                month = monthString2Int(timeStrings[-2])
            except:
                return None
            updateTime = datetime.datetime(currentTime.year, month, int(timeStrings[-1]))
        # print('Time: ' + updateTime.strftime('%d/%m/%Y'))
    else:
        return None

    # Creates and returns the dictionary
    return ({'author': author,
    'headline' : headline,
    'subHeadline' : subHeadline,
    'image' : image,
    'updateTime' : updateTime})

# Takes in a bs4 soup containing the html code from a article's webpage, and
# returns a dictionary containing the author, headline, image, score,
# sub-headline, and update time of the article. Assumed format: https://www.nbcn
# ews.com/news/us-news/nick-ut-photojournalist-who-made-famed-vietnam-war-napalm
# -girl-n1254517
def getArticleInfoFormat4(page_html):

    headers = page_html.find_all('header')
    if len(headers) > 0:
        header = headers[0]
    else:
        return None

    # Gets author
    authorSection = page_html.find_all(class_ = re.compile('byline'))
    if len(authorSection) > 0:
        author = authorSection[0].get_text()[2:]
        if ':' in author:
            return None
        # print('Author: ' + author)
    else:
        return None

    # Gets headline
    h1s = header.find_all('h1')
    if len(h1s)> 0:
        headline = h1s[0].get_text()
        # print('Headline: ' + headline)
    else:
        return None

    # Gets image if available
    pictures = page_html.find_all('picture')
    if len(pictures) > 0:
        imgs = pictures[0].find_all('img')
        if len(imgs) > 0:
            image = imgs[0]['src']
            # print('Image: ' + image)
        else:
            image = ''
    else:
        image = ''

    # Gets sub-headline
    dek = header.find_all(class_ = re.compile('dek'))
    body = page_html.find_all(class_ = re.compile('body'))
    if len(dek) > 0:
        subHeadline = dek[0].get_text()
        # print('Sub-Headline: ' + subHeadline)
    elif len(body) > 0:
        ps = body[0].find_all('p')
        if len(ps) > 0:
            subHeadline = ps[0].get_text()
            if len(subHeadline) > 100:
                subHeadline = subHeadline[:100]
            # print('Sub-Headline: ' + subHeadline)
        else:
            return None
    else:
        return None

    # Gets update time
    times = page_html.find_all('time')
    if len(times) > 0:
        timeStrings = times[0].get_text().split()
        if timeStrings[0] == 'Updated':
            timeStrings.pop(0)
        hhmm = timeStrings[3]
        ampm = timeStrings[4]
        try:
            hour, minutes = getTime(hhmm, ampm)
            year = int(timeStrings[2].replace(',', ''))
            month = monthString2Int(timeStrings[0].replace('.',''))
            day = int(timeStrings[1].replace(',',''))
        except:
            return None
        updateTime = datetime.datetime(year, month, day, hour, minutes)
        # print('Update Time: ' + updateTime.strftime('%d/%m/%Y'))
    else:
        return None

    return ({'author': author,
    'headline' : headline,
    'subHeadline' : subHeadline,
    'image' : image,
    'updateTime' : updateTime})

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
# update times of all the articles on the link that were updated after the given
# update time.
def getArticles(category, domain, lastUpdate, mainLink):

    # Gets the soup element for the mainLink
    page_html = getSoup(mainLink)
    print('Main Link: ' + str(mainLink))
    
    # Gets all descendants of the main soup element, and filters them using 
    # getArticle
    filteredDescendants = list(set(filter(getArticle, list(page_html.descendants))))

    # Gets all links from the list of descendants and formats them if necessary
    getLink = lambda element: formatStartOfLink(domain, element['href'])
    articleLinks = list(set(map(getLink, filteredDescendants)))

    print(len(articleLinks))

    # Initializes link list and dictionary list to store all the articles we
    # find
    artLinks = []
    artDictionaries = []

    # func = lambda articleLink : getArticleInfo(articleLink, domain, category, lastUpdate)
    # articlesInfo = list(map(func, articleLinks))

    counter = 0

    for articleLink in articleLinks:

        # This if-statement is here in order to avoid the error I was getting
        # where a link, â, would print and the program would stop working
        if 'â' in articleLink:
            continue

        articlesInfo = getArticleInfo(articleLink, domain, category, lastUpdate)

        # Checks if article info was actually found
        if articlesInfo != None:

            # Checks if the article is already in the list
            if articleLink not in artLinks:

                # Updates the counter
                counter += 1
                print(articleLink)
                print(counter)

                # Adds a category and link item to the article dictionary
                articlesInfo['category'] = category
                articlesInfo['link'] = articleLink

                # Adds dictionary and link to the list of found articles
                artDictionaries.append(articlesInfo)
                artLinks.append(articleLink)


    print('Articles added: ' + str(len(artDictionaries)))
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

# Takes in a domain and a time, and returns a dataframe of all the articles from 
# that domain that have been updated after the given time
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

    # Initializes lists that will store all the author, categories, headlines,
    # images, links, scores, sub-headlines, and update times for each article
    allArticles = []

    # Goes through each tuple and gets a cetegory, headline, sub-headline, link
    # image, update time, author, and a score for each article found on each 
    # category link. Returns a list for each one of these elements
    func = lambda clt: getArticles(clt[0], domain, lastUpdate, clt[1])
    allArticles = removeDuplicateDicts(flatten(list(map(func, categoryLinkTuples))), 'link')
    print(len(allArticles))
    # for categoryLinkTuple in categoryLinkTuples:
    #     allArticles += func(categoryLinkTuple)
    # allArticles = list(set(allArticles))
    #     category = categoryLinkTuple[0]
    #     link = categoryLinkTuple[1]

    #     articlesInfo = getArticles(category, domain, lastUpdate, link)

lastUpdate = datetime.datetime(2020, 1, 13)
func = lambda x : domainScrape(x, lastUpdate)

for domain in domains:
    func(domain)

# nbcHtml = 'https://www.nbcnews.com/news/us-news/live-blog/2021-01-15-covid-live-updates-vaccine-news-n1254373'
# nbcSoup = getSoup(nbcHtml)
# c = getArticleInfoFormat4(nbcSoup)

# times = []
# for k in range(1):
#     t0 = time.time()
#     k = list(map(func,domains))
#     t1 = time.time()
#     times.append(t1-t0)
# print(sum(times)/len(times))
# df = pd.concat(list(map(func, domains)))