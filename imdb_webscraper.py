import requests, bs4
import os.path 
from pathlib import Path
import urllib.request as urllib2
movieCap = 50

#get the home directory and user
homedir = os.path.expanduser('~')

#establish a working path
workingPath = os.path.join(homedir, Path('Videos', 'Movies_'))
movieDoc = open(os.path.join(workingPath, 'Movies_ranked') + ".txt", 'a')
movieDoc_2 = open(os.path.join(workingPath, 'Movies_ranked_2') + ".txt", 'a')
#pull the html code from IMDB
res = requests.get('https://www.imdb.com/search/title/?groups=top_250&sort=user_rating')
res.raise_for_status()

movieFile_soup = bs4.BeautifulSoup(res.text, 'html.parser')
movies_raw = movieFile_soup.select('.lister-item-content')

#now to seperate these into their own categories. So I will make two lists:
#One where it is put in the order that it came in

moviesDict = []
searchString = []
#function to create a folder in the correct subdir, and return 
#a path to the folder it created

def remove(s, indx):
        return ''.join(x for x in s if s.index(x) != indx)

def createMovie_dir(tit, about, lnk):
    fileTit = tit
    for i in range(len(tit)-1):
        if (ord(fileTit[i].lower()) < 97 | ord(fileTit[i].lower()) >122):
            fileTit = remove(fileTit, i) 
            i+=1
    
    if (tit[0:3].lower() == 'the'):
        tempLetter = tit[4]
    
    elif (ord(tit[0]) > 47 and ord(tit[0]) < 58):
        tempLetter = '0_9'
    else:
        tempLetter = tit[0]
    
    
    mf_path = os.path.join(workingPath, Path(tempLetter))
    finalString = os.path.join(mf_path, fileTit)
    
    #just doing some fixes for weird glitches with webscraping.. maybe find a way to abstract this a bit better.
    leonString = 'l' + chr(233) + 'on'
    if (fileTit.lower() == leonString):
        fileTit = 'leon the professional'
    
    searchString.append(fileTit.lower())
    os.mkdir(finalString)
    about_mod = about[5:] #put this here becuse I couldn't be arsed right now to do it safely, and I know I always get 5 random spaces when I pull from imdb
    c = 0
    for i in range(len(about_mod)-1):
        if (c > 65 and about_mod[i] == ' '):
            about_mod = about_mod[:i] + '\n' + about_mod[i+1:]
            c = 0
        else:
            c+=1
    #todo, format the about page so that it looks okay
    aboutString = 'About_' + fileTit
    aboutFile = open(os.path.join(finalString, aboutString + '.txt'), 'w')
    aboutFile.write(tit + '\n\n' + about_mod)
    
    

searchFile = open(os.path.join(workingPath, 'search_file') + ".txt", 'a')
index = 0
for x in movies_raw:
    title = x.select('.lister-item-header a')
    year = x.select('.lister-item-header .lister-item-year')
    ranking = x.select('.lister-item-header .lister-item-index')
    link = title[0].get('href')
    link = 'https://www.imdb.com/' + str(link)
    about = x.select('.ratings-bar + p')
    createMovie_dir(str(title[0].text), str(about[0].text), link)
    tempString = str(ranking[0].text) + ' ' + str(title[0].text) + ' ' + str(year[0].text) + '\n'
    moviesDict.append({str(title) : link})
    movieDoc.write(tempString)
    movieDoc_2.write(tempString)
    searchString[index] = searchString[index] + ' ' + str(year[0].text) + '\n'
    searchString[index].replace('(', '')
    searchString[index].replace(')', '')
    searchFile.write(searchString[index])
    index +=1

movieDoc.close()
searchFile.close()
movieDoc_2.close()
os.system('attrib +h ' + os.path.join(workingPath, 'search_file') + ".txt")
os.system('attrib +h ' + os.path.join(workingPath, 'Movies_ranked_2') + ".txt")


#Todo: make it so that it formats the text files as they get put in
#todo: make this list the top 250 best movies
#Todo: make this next part part of a different module.
#todo: write getposter code, lewarn to parse javascript

#todo: write the pirateBay code. Put a qbittorrent api thing.
#think about the sleeping during the day thing.
#todo, put this all together eventually.