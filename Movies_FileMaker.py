import os
import os.path 
from pathlib import Path

#get the home directory and user
homedir = os.path.expanduser('~')

#establish a working path
workingPath = os.path.join(homedir, Path('Videos', 'Movies_'))
#make a file called 'Movies' in C:/Users/Kiran/Videos
os.mkdir(workingPath)

#make a file called '0_9' in C:/Users/Kiran/Videos/Movies
os.mkdir(os.path.join(workingPath,'0_9'))
#myFile = open((os.path.join(workingPath,'0_9_movies'), 'w'))
#myFile.close()
#make files from a-z in C:/Users/Kiran/Videos/Movies
for i in range(65,91):
    currentPath = os.path.join(workingPath, chr(i))
    os.mkdir(currentPath)
    #fileName = 'MovieList_' + chr(i) + '.txt'
    #filePath = os.path.join(currentPath, fileName)
    #file1 = open(filePath, 'w')
    #file1.close()
    

