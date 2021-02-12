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
# sub-headline, and update time of the article. Assumed format: https://abcnews
# .go.com/Politics/wireStory/extraordinary-warning-trump-10-pentagon-chiefs-750
# 29997?cid=clicksource_4380645_2_heads_hero_live_headlines_hed
def getArticleInfoFormat1(page_html):
    
    # Gets article wrapper
    articleWrappers = page_html.find_all(class_='Article__Wrapper')
    if len(articleWrappers) > 0:
        articleWrapper = articleWrappers[0]
    else:
        return None
    
    # Gets header
    headers = articleWrapper.find_all('header')
    if len(headers) > 0:
        authorSection = headers[0].find_all(class_=re.compile('Author'))[0]
        if len(authorSection) > 0:
            authorStrings = authorSection.get_text().split()
            author = authorStrings[0] + ' ' + authorStrings[1]
            if (author == 'The Associated'):
                return None
        else:
            return None
    else:
        return None

    # Gets headline
    h1s = headers[0].find_all('h1')[0]
    if len(h1s) > 0:
        headline = h1s.get_text()
    else:
        return None

    # Gets image
    pictures = articleWrapper.find_all('figure', class_=re.compile('Image'))
    if len(pictures) > 0:
        image = pictures[0].find_all('img')[0]['src']

        if image[:8] != 'https://':
            image = ''
    else:
        image = ''

    # Gets sub-Headline
    h2s = headers[0].find_all('h2')
    ps = articleWrapper.find_all('p')
    if len(h2s) > 0:
        subHeadline = h2s[0].get_text()
    elif len(ps) > 0:
        subHeadline = ps[0].get_text()
        if len(subHeadline) > 100:
            subHeadline = subHeadline[:100]
    else:
        return None

    # Gets text
    articleContents = articleWrapper.find_all(class_='Article__Content')
    if len(articleContents) > 0:
        text = articleContents[0].get_text()
    else:
        return None

    # Gets update-time
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
    'format': 1,
    'headline' : headline,
    'image' : image,
    'text' : text,
    'subHeadline' : subHeadline,
    'updateTime' : updateTime})
