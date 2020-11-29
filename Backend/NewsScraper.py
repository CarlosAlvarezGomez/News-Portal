import pandas as pd
import urllib.error
from urllib.request import urlopen as uReq
import requests
import sqlite3
from bs4 import BeautifulSoup as soup
import datetime
import time

domains = ["cnn", "foxnews", "abcnews", "nbcnews", "theguardian"]

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
    elif ((monthString == "September") | (monthString == "Sep")):
        return 9
    elif ((monthString == "October") | (monthString == "Oct")):
        return 10
    elif ((monthString == "November") | (monthString == "Nov")):
        return 11
    elif ((monthString == "December") | (monthString == "Dec")):
        return 12

def getTime(time, ampm):
    timeList = time.split(":")
    if ((ampm == "AM") & (timeList[0] != "12")) | ((ampm == "PM") & (timeList[0] == "12")):
        return int(timeList[0]), int(timeList[1])
    elif (ampm == "AM"):
        return 0, int(timeList[1])
    else:
        return int(timeList[0])+12, int(timeList[1])
        
def CNNScrape(lastUpdate):
    # Initializes lists that will be returned
    categories = []
    titles = []
    subtitles = []
    links = []
    images = []
    updateTimes = []
    scores = []
    articlesAdded = 0

    # Find all the tabs on CNN's main page
    mainPage = "https://www.cnn.com"
    uClient = uReq(mainPage)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    tabsUL = (page_soup.findAll("ul", {"class":"sc-kAzzGY fDqWjJ"}))[0]
    tabsLIList = tabsUL.findAll("li", {})
    tabs = []
    for li in tabsLIList:
        tabs.append(li["data-section"])

    #Go to each section found
    for tab in tabs:
        uClient = uReq(mainPage + "/" + tab)
        page_html = uClient.read()
        uClient.close()
        page_soup = soup(page_html, "html.parser")
        articles = page_soup.findAll("article", {})
        for article in articles:
            time.sleep(.01)
            if (article.find("a") != None):
                if (article.find("a")["href"][0] == "/"):
                    articleURL = mainPage+article.find("a")["href"]
                else:
                    articleURL = article.find("a")["href"]
                if (articleURL[12:15] == "cnn"):
                    uClient = uReq(articleURL)
                    articleHtml = uClient.read()
                    uClient.close()
                    articleSoup = soup(articleHtml, "html.parser")
                    if (articleSoup.find("p", {"class", "update-time"}) != None):
                        print(articleURL)
                        dateString = (articleSoup.find("p", {"class", "update-time"}).text).split(" ")
                        print(dateString)
                        hour, minute = getTime(dateString[1], dateString[2])
                        print(int(dateString[7]), monthString2Int(dateString[5]), int(dateString[6][:-1]), hour, minute)
                        articleDate = datetime.datetime(int(dateString[7]), monthString2Int(dateString[5]), int(dateString[6][:-1]), hour, minute)
                        if (articleDate > lastUpdate):
                            articlesAdded += 1
                            print("Total articles: " + str(articlesAdded))
                            categories.append(tab)
                            titles.append(article.find("span", {"class", "cd__headline-text"}).text)
                            subtitles.append("")
                            links.append(articleURL)
                            updateTimes.append(articleDate)
                            scores.append((articleDate - lastUpdate).seconds/60)
                            if (article.find("img") != None):
                                images.append(article.find("img")["src"])
                            else:
                                images.append("")
    print("Total articles: " + str(articlesAdded))
    return categories, titles, subtitles, links, images, updateTimes, scores      

def getFoxDateArticle1(dateString):
    dateList = dateString.split(" ")
    currentTime = datetime.datetime.now()
    if (dateList[-2] == "hours") | (dateList[-2] == "hour"):
        delta = datetime.timedelta(0, 0, 0, 0, 0, -int(dateList[-3]))
    elif (dateList[-2] == "mins") | (dateList[-2] == "min"):
        delta = datetime.timedelta(0, 0, 0, 0, -int(dateList[-3]))
    elif (dateList[-2] == "days") | (dateList[-2] == "day"):
        delta = datetime.timedelta(-int(dateList[-3]))
    else:
        raise ValueError("datestring not accounted for")
    return currentTime + delta

def getFoxDateArticle2(dateString):
    dateList = dateString.split("-")
    return datetime.datetime(int(dateList[0]), int(dateList[1]), int(dateList[2]))

def getFoxDateVideo(dateString):
    dateList = dateString.split("-")
    return datetime.datetime(int(dateList[0]), int(dateList[1]), int(dateList[2]))

def FoxScrape(lastUpdate):
    # Initializes lists that will be returned
    categories = []
    titles = []
    subtitles = []
    links = []
    images = []
    updateTimes = []
    scores = []
    articlesAdded = 0
    errorsCaught = 0

    # Find all the tabs on Foxnews' main page
    mainPage = "https://www.foxnews.com"
    uClient = uReq(mainPage)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    tabsUL = (page_soup.find("nav", {"id":"main-nav"}))
    tabsLIList = tabsUL.findAll("li")
    tabs = []

    for li in tabsLIList:
        tabs.append((li.text, li.a["href"]))
    
    tabs.pop() # Removes the ('More', '#') category
    for (tab, href) in tabs:
        if ((tab != "Fox Nation") & (tab != "TV") & (tab != "Listen")):
            uClient = uReq("https:" + href)
            pageHtml = uClient.read()
            uClient.close()
            pageSoup = soup(pageHtml, "html.parser")
            articles = pageSoup.findAll("article", {})
            for article in articles:
                time.sleep(0.01)
                if (article.a["href"][:6] == "https:"):
                    articleURL = article.a["href"]
                else:
                    articleURL = mainPage+article.a["href"]
                print(articleURL)
                try:
                    uClient = uReq(articleURL)
                    articleHtml = uClient.read()
                    uClient.close()
                except urllib.error.HTTPError:
                    errorsCaught += 1
                    print("Total Errors Caught: "+ str(errorsCaught))
                    continue
                articleSoup = soup(articleHtml, "html.parser")
                if (articleURL[8:13] == "video"):
                    articleDate = getFoxDateVideo(articleSoup.find("meta", {"name":"dc.date"})["content"])
                elif (articleSoup.find("div", {"class":"article-date"}) != None):
                    if (articleSoup.find("div", {"class":"article-date"}).text.split(" ")[-1] == "ago"):
                        articleDate = getFoxDateArticle1(((articleSoup.find("div", {"class":"article-date"})).text))
                    else:
                        articleDate = getFoxDateArticle2(articleSoup.find("meta", {"data-hid":"dc.date"})["content"])
                else:
                    raise ValueError("Date type not accounted for")
                if (((articleURL.split(".")[1] == "foxnews") | (articleURL.split(".")[1] == "foxbusiness")) &
                (articleURL.split(".")[2] != "com") & (articleURL.split("/")[-2] != "shows") &
                (articleURL.split("/")[-1] != "barrons-roundtable") & (articleDate > lastUpdate)):
                    articlesAdded += 1
                    print("Total Articles Added: " + str(articlesAdded))
                    # Adds category
                    categories.append(tab.lower().replace(".",""))

                    #Adds title
                    if (articleURL[8:13] == "video"):
                        nTitle = articleSoup.find("div", {"class":"video-meta"}).h1.text
                    elif (article.find("h2", {"class":"title"} != None)):
                        nTitle = article.find("h2", {"class":"title"}).text
                    elif (article.find("h3", {"class":"title"} != None)):
                        nTitle = article.find("h3", {"class":"title"}).text
                    elif (articleSoup.find("meta", {"name", "dc.title"}) != None):
                        nTitle = articleSoup.find("meta", {"name":"dc.title"})["content"]
                    else:
                        nTitle = articleSoup.find("h1", {"class":"headline"}).text
                    titles.append(nTitle)
                    
                    # Adds subtitle
                    subtitles.append("")

                    # Adds link
                    links.append(articleURL)

                    # Adds image, if possible
                    if (article.find("img") != None):
                        images.append(article.find("img")["src"])
                    else:
                        images.append("")
                    
                    # Adds updateTime
                    updateTimes.append(articleDate)

                    # Adds score
                    scores.append((articleDate - lastUpdate).seconds)

    print("Total Errors Caught: "+ str(errorsCaught))
    print("Total Articles Added: " + str(articlesAdded))
    return categories, titles, subtitles, links, images, updateTimes, scores

def getABCDateArticle(dateString):
    dateList = dateString.split(" ")
    time = dateList[3].split(":")
    hour = int(time[0])
    if (dateList[4] == "PM") & (hour != 12):
        hour += 12
    elif (dateList[4] == "AM") & (hour == 12):
        hour = 0
    minutes = int(time[1])
    return datetime.datetime(int(dateList[2][:-1]), monthString2Int(dateList[0]), int(dateList[1][:-1]), hour, minutes)

def getABCDateVideo(dateString):
    dateList = dateString.split("T")
    date = dateList[0].split("-")
    time = dateList[1].split(":")
    return datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2][:-1]))

def ABCScrape(lastUpdate):
    # Initializes lists that will be returned
    categories = []
    titles = []
    subtitles = []
    links = []
    images = []
    updateTimes = []
    scores = []
    articlesAdded = 0
    imagesAdded = 0

    # Find all the tabs on Foxnews' main page
    mainPage = "https://abcnews.go.com"
    uClient = uReq(mainPage)
    pageHtml = uClient.read()
    uClient.close()
    pageSoup = soup(pageHtml, "html.parser")
    tabsLIList = (pageSoup.find("div",{"class":"more-dropdown"}).ul.findAll("li"))
    tabs = []

    for li in tabsLIList:
        tabs.append((li["class"], li.a["href"]))
    
    del tabs[8] # Removes the tab at index 8, which is the 'Virtual Reality' tab
    del tabs[9] # Removes the tab at index 7, which is the 'Tips' tab
    del tabs[10] # Removes the tab at index 7, which is the 'FiveThirtyEight' tab


    for (tab, href) in tabs:
        uClient = uReq(href)
        tabHtml = uClient.read()
        uClient.close()
        TabSoup = soup(tabHtml, "html.parser")
        contentLists = TabSoup.findAll("section", {"class":"ContentList"})
        articleURLList = []

        for contentList in contentLists:
            sections = contentList.findAll("section", {"class":"ContentList__Item"})
            for section in sections:
                articleURLList.append(section.a["href"])
            
        latestHeadlines = TabSoup.findAll("li", {"class":"LatestHeadlines__item"})
        for headline in latestHeadlines:
            articleURLList.append(headline.a["href"])

        contentRolls = TabSoup.findAll("section", {"class":"ContentRoll"})

        for contentRoll in contentRolls:
            contentRollItems = contentRoll.findAll("section", {"class":"ContentRoll__Item"})
            for item in contentRollItems:
                articleURLList.append(item.find("a")["href"])

        for articleURL in articleURLList:
            time.sleep(0.01)
            print(articleURL)
            uClient = uReq(articleURL)
            articleHtml = uClient.read()
            uClient.close()
            articleSoup = soup(articleHtml, "html.parser")
            try:
                if (articleSoup.find("div", {"class":"Byline__Meta Byline__Meta--publishDate"}) != None):
                    articleDate = getABCDateArticle(articleSoup.find("div", {"class":"Byline__Meta Byline__Meta--publishDate"}).text)
                else:
                    articleDate = getABCDateVideo(articleSoup.find("meta", {"itemprop":"uploadDate"})["content"])
            except TypeError:
                continue
            if (articleDate > lastUpdate):
                articlesAdded += 1
                print("Total Articles: " + str(articlesAdded))
                categories.append(tab)
                if (articleSoup.find("h1", {"class":"Article__Headline__Title"}) != None):
                    titles.append(articleSoup.find("h1", {"class":"Article__Headline__Title"}).text)
                else:
                    titles.append(articleSoup.find("h1", {"itemprop":"name"}).text)
                subtitles.append("")
                links.append(articleURL)
                if (articleSoup.find("img", {"class":"amp-poster"}) != None):
                    imagesAdded += 1
                    print("Total images: " + str(imagesAdded))
                    images.append(articleSoup.find("img", {"class":"amp-poster"})["src"])
                else:
                    images.append("")
                updateTimes.append(articleDate)
                scores.append((articleDate - lastUpdate).seconds)

    print("Total Articles: " + str(articlesAdded))
    print("Total images: " + str(imagesAdded))
    return categories, titles, subtitles, links, images, updateTimes, scores

        
        # for articleURL in articleURLList:
        #     uClient = uReq(articleURL)
        #     articleHtml = uClient.read()
        #     uClient.close()
        #     articleSoup = soup(articleHtml, "html.parser")

lastUpdate = datetime.datetime(2020, 5, 24, 15)
categories = []
titles = []
subtitles = []
links = []
images = []
updateTimes = []
scores = []
for domain in domains:
    if (domain == "cnn"):
        # nCategories, nTitles, nSubtitles, nLinks, nImages, nUpdateTimes, nScores = CNNScrape(lastUpdate)
        # categories += nCategories
        # titles += nTitles
        # subtitles += nSubtitles
        # links += nLinks
        # images += nImages
        # updateTimes += nUpdateTimes
        # scores += nScores
        time.sleep(0.01)
    elif (domain == "foxnews"):
        # nCategories, nTitles, nSubtitles, nLinks, nImages, nUpdateTimes, nScores = FoxScrape(lastUpdate)
        # categories += nCategories
        # titles += nTitles
        # subtitles += nSubtitles
        # links += nLinks
        # images += nImages
        # updateTimes += nUpdateTimes
        # scores += nScores
        time.sleep(0.01)
    elif (domain == "abcnews"):
        # nCategories, nTitles, nSubtitles, nLinks, nImages, nUpdateTimes, nScores = ABCScrape(lastUpdate)
        # categories += nCategories
        # titles += nTitles
        # subtitles += nSubtitles
        # links += nLinks
        # images += nImages
        # updateTimes += nUpdateTimes
        # scores += nScores
        time.sleep(0.01)