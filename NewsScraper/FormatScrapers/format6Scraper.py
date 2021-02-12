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

# List of categories the articles will be in
categories = (['business',
'entertainment',
'health',
'opinion',
'politics',
'us',
'world'])

# Takes in an element and returns a category it is associated with. Returns an 
# empty string if the element is not associated with any categories 
def getAssociatedCategory(string):

    # Imports global variable
    global categories
    string = formatString(string)

    if string in categories:
        return string
    elif (string == 'review') or ('entertainment' in string):
        return 'entertainment'
    elif string == 'analysis':
        return 'opinion'
    else:
        return ''

# Takes in a bs4 soup containing the html code from a article's webpage, and
# returns a dictionary containing the author, headline, image, score,
# sub-headline, and update time of the article. Assumed format: https://www.dai
# lywire.com/news/netflix-dominates-2021-golden-globe-nominations-full-list-ann
# ounced
def getArticleInfoFormat6(page_html):

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
    authorSections = header.find_all('a')
    if len(authorSections) > 0:
        authorSection = authorSections[0]
        author = authorSection.get_text()
    else:
        return None

    # Gets category
    h2s = header.find_all('h2')
    if len(h2s) > 0:
        category = h2s[0].get_text().replace('—', '').replace(' ', '')
        if getAssociatedCategory(category) != '':
            category = getAssociatedCategory(category)
        else:
            category = 'politics'
    else:
        return None

    # Gets headline
    h1s = page_html.find_all('h1')
    if len(h1s) > 0:
        headline = h1s[0].get_text()
    else:
        return None

    # Gets image if available
    imgs = article.find_all('img')
    if len(imgs) > 0:
        image = imgs[0]['src']
    else:
        image = ''

    # Gets text
    bodies = article.find_all(attrs = {'id' : 'post-body-text'})
    if len(bodies) > 0:
        ps = bodies[0].find_all('p')
        if len(ps) > 0:
            text = ps[0].get_text()
            for p in ps[1:]:
                text += ' ' + p.get_text()
        else:
            return None
    else:
        return None

    # Gets sub-headline
    ps = article.find_all('p')
    if len(ps) > 0:
        subHeadline = ps[0].get_text()
        if len(subHeadline) > 100:
            subHeadline = subHeadline[:100]
    else:
        return None

    # Gets update time
    times = header.find_all('time')
    if len(times) > 0:
        updateTimeStrings = times[0].get_text().split(' ')
        year = int(updateTimeStrings[2])
        month = monthString2Int(updateTimeStrings[0])
        day = int(updateTimeStrings[1][:-1])
        updateTime = datetime.datetime(year, month, day)
    else:
        return None

    return ({'author': author,
    'format' : 6,
    'headline' : headline,
    'category' : category,
    'image' : image,
    'text' : text,
    'subHeadline' : subHeadline,
    'updateTime' : updateTime})