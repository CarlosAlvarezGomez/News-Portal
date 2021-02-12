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
# sub-headline, and update time of the article. Assumed format: https://www.uni
# vision.com/univision-news/health/cafe-dato-how-to-combat-stress-in-times-of-c
# oronavirus
def getArticleInfoFormat7(page_html):

    # Gets article tag
    articles = page_html.find_all('article')
    if len(articles) > 0:
        article = articles[0]
    else:
        return None

    # Gets header tag from article tag
    headers = article.find_all('header')
    if len(headers) > 0:
        header = headers[0]
    else:
        return None

    # Gets author
    nameSections = article.find_all(attrs={'itemprop': 'name'})
    if len(nameSections) > 0:
        nameSection = nameSections[0]
        author = nameSection.get_text().replace(',', '')
    else:
        return None

    # Gets headline
    h1s = page_html.find_all('h1')
    if len(h1s) > 0:
        headline = h1s[0].get_text()
    else:
        return None

    # Gets image if available
    pictures = article.find_all('picture')
    if len(pictures) > 0:
        picture = pictures[0]
        imgs = picture.find_all('img')
        if len(imgs) > 0:
            image = imgs[0]['src']
        else:
            image = ''
    else:
        image = ''

    # Gets text
    chunks = page_html.find_all(attrs={'id' : 'article-chunks'})
    if len(chunks) > 0:
        ps = chunks[0].find_all('p')
        if len(ps) > 0:
            text = ps[0].get_text()
            for p in ps[1:]:
                text += ' ' + p.get_text()
        else:
            return None
    else:
        return None

    # Gets sub-headline
    descriptions = article.find_all(attrs={'itemprop':'description'})
    if len(descriptions) > 0:
        subHeadline = descriptions[0].get_text()
        if len(subHeadline) > 100:
            subHeadline = subHeadline[:100]
    else:
        return None

    # Gets update time
    times = page_html.find_all('meta', attrs={'itemprop': 'datePublished'})
    if len(times) > 0:
        updateTimeStrings = times[0]['content'].replace(':', '-').replace('T', '-').split('-')
        year = int(updateTimeStrings[0])
        month = int(updateTimeStrings[1])
        day = int(updateTimeStrings[2])
        hour = int(updateTimeStrings[3])
        minutes = int(updateTimeStrings[4])
        updateTime = datetime.datetime(year, month, day, hour, minutes)
    else:
        return None

    return ({'author': author,
    'format' : 7,
    'headline' : headline,
    'image' : image,
    'text' : text,
    'subHeadline' : subHeadline,
    'updateTime' : updateTime
    })