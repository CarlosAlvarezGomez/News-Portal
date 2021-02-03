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
