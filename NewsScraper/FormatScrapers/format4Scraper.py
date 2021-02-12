# Adds helper libraries to path
import sys
sys.path.insert(0, '../HelperLibraries')

# Imports necessary libraries
from bs4 import BeautifulSoup as soup
from StringHelpers import *
import bs4
import datetime
import re
import time

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

# Takes in a bs4 soup containing the html code from a article's webpage, and
# returns a dictionary containing the author, headline, image, score,
# sub-headline, and update time of the article. Assumed format: https://www.nbc
# news.com/news/us-news/nick-ut-photojournalist-who-made-famed-vietnam-war-napa
# lm-girl-n1254517
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
    else:
        return None

    # Gets headline
    h1s = header.find_all('h1')
    if len(h1s)> 0:
        headline = h1s[0].get_text()
    else:
        return None

    # Gets image if available
    pictures = page_html.find_all(class_=re.compile('_main-image'))
    if len(pictures) > 0:
        imgs = pictures[0].find_all('img')
        if len(imgs) > 0:
            image = imgs[0]['src']
        else:
            image = ''
    else:
        image = ''

    # Gets text
    articleBodies = page_html.find_all(class_=re.compile('article-body__content'))
    if len(articleBodies) > 0:
        ps = articleBodies[0].find_all('p')
        if len(ps) > 0:
            text = ps[0].get_text()
            for p in ps[1:]:
                text += ' ' + p.get_text()
        else:
            return None
    else:
        return None

    # Gets sub-headline
    dek = header.find_all(class_ = re.compile('dek'))
    body = page_html.find_all(class_ = re.compile('body'))
    if len(dek) > 0:
        subHeadline = dek[0].get_text()
    elif len(body) > 0:
        ps = body[0].find_all('p')
        if len(ps) > 0:
            subHeadline = ps[0].get_text()
            if len(subHeadline) > 100:
                subHeadline = subHeadline[:100]
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
    else:
        return None

    return ({'author': author,
    'format' : 4,
    'headline' : headline,
    'image' : image,
    'text' : text,
    'subHeadline' : subHeadline,
    'updateTime' : updateTime})
