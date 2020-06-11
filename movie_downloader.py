import requests, bs4
import os.path 
from pathlib import Path
import urllib.request as urllib2
from selenium import webdriver
import time # to sleep, in case selenium just isn't waiting for long enough
import sys

homedir = os.path.expanduser('~')

#establish a working path
workingPath = os.path.join(homedir, Path('Videos', 'Movies_'))
searchDoc = open(os.path.join(workingPath, 'search_file') + ".txt", 'r')
searchAr = searchDoc.readlines()
searches = []
dateAr = []
count = 0

#format the search terms
for x in searchAr:
    x = x.replace('(', "")
    x = x.replace(')', '')
    if x.find('\''):
        x = x.replace('\'', '')
    x = x.replace(' ', '+')
    x = x.replace('\n', '')
    if x.find('-+'):
        x = x.replace('-+', '')
    dateAr.append(x[-5:])
    dateAr[count] = dateAr[count].replace('+', '')
    searches.append(x)
    count += 1

search_elems = []

count = 0
for i in searches:
    search_elems.append(searches[count].split('+'))
    count+=1
options = webdriver.ChromeOptions()
options.add_argument('headless')


def checkItems(index_, x_):
    for i in search_elems[index_]:
        if (x_.text.lower().find(i) != -1):
            return True
    print('checkitems returned false for  ' + search_elems[0] + ' :: ' + x_.text)
    return False 

movieMatches = []
magnetLink = []
firstTime = True
exceptions_File = open(os.path.join(workingPath, 'Not Yet Aquired') + ".txt", 'a')
magnetLink_file =  open(os.path.join(workingPath, 'magnetLink_file') + ".txt", 'a')
os.system('attrib +h ' + os.path.join(workingPath, 'magnetLink_file') + ".txt")

for z in range(0,len(searches)):
    wordsFromSearch = 0
    noResult = False
    whileSwitch = False
    movieMatches.clear()
    while ((len(search_elems[z]) - wordsFromSearch >= 2 or len(movieMatches) <5)) and (whileSwitch == False):
        try:
            driver.quit()
        except:
            print('Fetching magnet links...')
            

        movieMatches.clear()
        currentSearch = ''

        for e in range(0, len(search_elems[z]) - wordsFromSearch):
            currentSearch += search_elems[z][e]
            
            if search_elems[z][e] != search_elems[z][len(search_elems[z])-wordsFromSearch - 1]:
                currentSearch+='+'

        print('searching in ' + currentSearch)
        trySwitch = False
        tryCount = 0
        while (trySwitch == False):
                try:
                    driver = webdriver.Chrome('chromedriver', chrome_options=options)
                    getUrl = 'https://thepiratebay.org/search.php?q=' + currentSearch + '&all=on&search=Pirate+Search&page=0&orderby='
                    driver.get(getUrl)
                    trySwitch = True
                except:
                    if (tryCount < 6):
                        tryCount+=1
                    if (tryCount == 6):
                        print('\n\nCannot reach PirateBay.. Waiting for 3 minutes and trying again...')
                        time.sleep(300)
                    if (tryCount > 6):
                        print('broken forever...')
                        sys.exit()

        
        for x in range(10):
            listItems = driver.find_elements_by_class_name("list-entry")
            if (len(listItems) == 0):
                time.sleep(0.5)

        
        
        for x in range(0, len(listItems)-1):
            if (checkItems(z, listItems[x])):
                movieMatches.append(listItems[x])
        
        if len(movieMatches) < 5:
            wordsFromSearch += 1
        elif len(movieMatches) >= 5:
            whileSwitch = True
        
        if len(search_elems[z]) - wordsFromSearch <= 2 and len(movieMatches) == 0:
            print('Unable to find results for ' + searches[z])
            noResult = True
            whileSwitch = True
        
    
    if noResult != True:
        magnetLink.append(movieMatches[0].find_elements_by_class_name('item-icons')[0].find_element_by_tag_name("a").get_attribute('href'))
        magnetLink_file.write(str(magnetLink[z]) + '\n')
        if (str(magnetLink[z]) == ''):
            print('Something went wrong with ' + searches[z])
            exceptions_File.write(searches[z])
            magnetLink.append('noResult\n')
        
        print('got magnet link for ' + movieMatches[0].text)
                
    else:
        print('No results found for ' + searches[z])
        exceptions_File.write(searchAr[z] + '\n')
        magnetLink_file.write('noResult\n')
        magnetLink.append('noResult\n')
    
exceptions_File.close()
magnetLink_file.close()
driver.quit()    
print('Program ended succesfully')


#Todo: check seeders.
#todo: one day, turn this learning exercise into a functional app by using Yyfy's api. Will make this code execute in a matter of seconds
#todo: gisaengchung (2019) is the original name for Parasite. I need to put that deals with this. Either in the form of a google search
#or just by replacing gisaengchung (2019) with Parasite (2019).  I like the idea of using google, because
#it would be a first step into making an app that gathers information about stuff in its data set.