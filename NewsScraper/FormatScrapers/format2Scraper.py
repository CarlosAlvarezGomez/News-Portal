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
# sub-headline, and update time of the article. Assumed format: https://www.cnn
# .com/2021/01/06/health/south-africa-sequencing-coronavirus-variant/index.html
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
            subHeadline = subHeadline[:100]
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
