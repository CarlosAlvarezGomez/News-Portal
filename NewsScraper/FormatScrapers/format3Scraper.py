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

# Takes in a bs4 soup containing the html code from a article's webpage, and
# returns a dictionary containing the author, headline, image, score,
# sub-headline, and update time of the article. Assumed format: https://www.fox
# business.com/real-estate/3d-printed-buildings-california-housing-crisis
def getArticleInfoFormat3(page_html):
    global months
    global unitsOfTime
    
    # Gets the author
    authorSection = page_html.find_all(class_ = re.compile('author'))
    if len(authorSection) > 0:
        a = authorSection[0].find_all('a')
        if len(a) > 0:
            author = a[0].get_text()
        else:
            return None
    else:
        return None

    # Gets the headline
    h1s = page_html.find_all('h1')
    if len(h1s) > 0:
        headline = h1s[0].get_text()
    else:
        return None

    # Gets the sub-headline
    h2s = page_html.find_all('h2')
    if len(h2s) > 0:
        subHeadline = h2s[0].get_text()
    else:
        return None
    
    # Gets images
    articleBody = page_html.find_all(class_=re.compile('body'))
    if len(articleBody) > 0:
        imgs = articleBody[0].find_all('img')
        if len(imgs) > 1:
            image = imgs[1]['src']
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
    else:
        return None

    # Creates and returns the dictionary
    return ({'author': author,
    'headline' : headline,
    'subHeadline' : subHeadline,
    'image' : image,
    'updateTime' : updateTime})
