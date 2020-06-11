import os.path 
from pathlib import Path
import time
import sys
from qbittorrent import Client
import atexit

qb = Client('http://127.0.0.1:8080/')

qb.login()

catgegory_ = 'movie_downloader'
workingHours = [1,6]
workingHours[0] *= (60*60)
workingHours[0] += (24*60*60)
workingHours[1] *= (60*60)

workingHours[1] += 24*(60*60)

#okay, so this will be me reading the file from the magnet link file.
#I also need to make it so that the program only operates during the hours of 2 and 6 am
#I also need to make it so that this code takes the first magnet link and  checks if its downloading
#if not, it stats thedownload. If it is, then it resumes the download.
#Put this code into start programs.

#Takes a string, and finds the correct file, makes a directory 
#in that folder and makes a directory


def remove(s, indx):
        return ''.join(x for x in s if s.index(x) != indx)

def createMovie_dir(tit):
    fileTit = ''
    tempTit = tit.split(' ')
   
    for i in range(1, len(tempTit)-1):
        fileTit += tempTit[i] + ' '

    print(fileTit)
    for i in range(len(fileTit)-1):
        if (ord(fileTit[i].lower()) < 97 | ord(fileTit[i].lower()) >122):
            fileTit = remove(fileTit, i) 
            i+=1
    
    if (fileTit[0:3].lower() == 'the'):
        tempLetter = fileTit[4]
    
    elif (ord(fileTit[0]) > 47 and ord(fileTit[0]) < 58):
        tempLetter = '0_9'
    else:
        tempLetter = fileTit[0]
    
    
    mf_path = os.path.join(workingPath, Path(tempLetter))
    finalString = os.path.join(mf_path, fileTit)
    return finalString

    

#fetch file, put into an array

homedir = os.path.expanduser('~')
workingPath = os.path.join(homedir, Path('Videos', 'Movies_'))




magnetFile = open(os.path.join(workingPath, 'magnetLink_file.txt'), 'r+')
magnetLinks = magnetFile.readlines()
searchDoc = open(os.path.join(workingPath, 'Movies_ranked_2') + ".txt", 'r+')
searchAr = searchDoc.readlines()

for z in range(len(magnetLinks)-1):
    print('downloading ' + searchAr[0])
    if(magnetLinks[0] == 'noResult'):
        magnetLinks.pop(0)
        searchAr.pop(0)
        continue
    #get torrents downloading now
    torrents = qb.torrents()

    currentTorrent = None
        #figure out which folder to go into:
    pathString = createMovie_dir(searchAr[0])
    try:
        os.mkdir(pathString)
    except:
        pass
    qb.download_from_link(magnetLinks[0], savepath=pathString, category = catgegory_)
    torrents = qb.torrents()

    for i in torrents:
        if catgegory_ == i['category']:
            qb.resume(i['hash'])
    downloading = True
    while downloading:
        
        tor = qb.torrents(category=catgegory_)    
        wait_time = None
        
        while wait_time == None:
            try:
                wait_time = int(tor[0]['eta'])/3
            except:
                pass

        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        
        temp_cTime = current_time.split(':')
        cTime_seconds = int(temp_cTime[0])*(60*60) + int(temp_cTime[1])*60 + int(temp_cTime[2])
        if (cTime_seconds < workingHours[1] and cTime_seconds > workingHours[0]):
            pass
        else:
            sleeping = ((abs(cTime_seconds - workingHours[0]))/(60*60))
            print('sleeping for ' + str(sleeping)[:3] + ' hours...')
            time.sleep(10) 
            #darn, the pause function isn't working too well. put this here for a cheap fix. todo: make this more stable.
            qb.pause(tor[0]['hash']) 
            time.sleep(abs(cTime_seconds - workingHours[0]))
            print('waking up...')
            qb.resume(tor[0]['hash'])
        if (tor[0]['progress']) == 1:
            print('Finished downloading ' + tor[0]['name'])
            qb.delete(tor[0]['hash'])
            magnetLinks.pop(0)
            searchAr.pop(0)
            searchDoc.truncate(0)
            magnetFile.truncate(0)
            for it in searchAr:
                searchDoc.write(it + '\n')
            for it in magnetLinks:
                magnetFile.write(it + '\n')
            #now i Need to make it so that the folder that gets downloaded, the mp4
            downloading = False
        else:
            time.sleep(60)
searchDoc.close()
magnetFile.close()        
print('finished')
    #qb.download_from_link(magnetLinks[0], savepath=dl_path)
#check if any of those torrents match the magnet link of the top result. If there is a match, the resume torrent. if not, start torrent.
#Posible that I will need to save the name of the torrent in a file during movie_downloaders run.
#Specify a path for the Torrent. 

#wait for the torrent to download, then change the folder's name to the movie's name.

#delete the torrent, remove the first element of the maget link array, write the magnet array onto the file.

#repeat.


#I need to run time and the downloader in parallel. So what I will do is follow this: https://stackoverflow.com/questions/7207309/python-how-can-i-run-python-functions-in-parallel
# One function will be keep track of the time and getting ready to pause.. THe other will be checking the downloads and waiting for the downloads to finish, then getting ready for the
#downloads and doing the file stuff.