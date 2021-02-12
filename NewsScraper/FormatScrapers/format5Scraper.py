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
# sub-headline, and update time of the article. Assumed format: https://www.dai
# lymail.co.uk/sciencetech/article-9219601/Egyptian-mummy-doesnt-match-3-000-ye
# ar-old-coffin.html
def getArticleInfoFormat5(page_html):

    # Gets author
    authorSections = page_html.find_all(class_=re.compile('author-section'))
    if len(authorSections) > 0:
        authorSection = authorSections[0]
        author = authorSection.get_text()[3:]
    else:
        return None

    # Gets headline
    h2s = page_html.find_all('h2')
    if len(h2s) > 0:
        headline = h2s[0].get_text()
    else:
        return None

    # Gets image if available
    body = page_html.find_all(attrs={"itemprop": "articleBody"})
    if len(body) > 0:
        imgs = body[0].find_all('img')
        if len(imgs) > 0:
            if 'data-src' in imgs[0].attrs.keys():
                image = imgs[0]['data-src']
            else:
                image = ''
        else:
            image = ''  
    else:
        return None

    # Gets text
    ps = body[0].find_all('p', recursive=False)
    if len(ps) > 0:
        text = ps[0].get_text()
        for p in ps[1:]:
            if len(p.find_all('span')) == 0:
                text += ' ' + p.get_text()
    else:
        return None
    
    # Gets sub-headline
    subHeadline = ps[0].get_text()
    if len(subHeadline) > 100:
        subHeadline = subHeadline[:100]

    # Gets update time
    bylines = page_html.find_all(class_=re.compile('byline-section'))
    if len(bylines) > 0:
        times = bylines[0].find_all('time')
        if len(times) > 1:
            updateTimeStrings = times[1].get_text().split()
            year = int(updateTimeStrings[4])
            month = monthString2Int(updateTimeStrings[3])
            day = int(updateTimeStrings[2])
            hhmm = updateTimeStrings[0].split(':')
            hour = int(hhmm[0])
            minutes = int(hhmm[1])
            updateTime = datetime.datetime(year, month, day, hour, minutes)
        else:
            return None
    else:
        return None

    return ({'author': author,
    'format' : 5,
    'headline' : headline,
    'image' : image,
    'text' : text,
    'subHeadline' : subHeadline,
    'updateTime' : updateTime})