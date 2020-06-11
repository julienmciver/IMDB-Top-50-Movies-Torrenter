IMDB Top 50 Movies Webscraper
----------------------------------------------------

I coded this to learn how to code in python, focussing primarily on webscraping. A lot of the methods etc. that I used aren't
the most efficient ways of doing this particular task, and I avoided using a torrent site api
in order to learn how to parse javascript generated content. 

------------------------------------------------------------
How to use this
------------------------------------------------------------

So as it stands, you need to click into and run each script individually.

in this order:

Movies_FileMaker.py
imdb_webscraper.py
movie_downloader.py
torrenter.py

*** imdb_webscraper is very slow due to it having to wait for javascript generated elements to appear on the webpage.

*** torrenter will pause between the hours of 6am and 1am.
 
--------------------------------------------------------------
To improve this code:
--------------------------------------------------------------

- I want to make it so that you can specify which path the movies_ folder will have.
- I want to create a central code that will manage the running of other codes. WIll be fun to do 
  and I willk get on that after my next project. That way, you will only need to run that single script and all of these scripts
  will run sequentially. Either that or just get it all into modules. But I think I would prefer to do it with an overlord type script that works through the cmd. Would be more interesting for now.
- Renaming folders etc is also something I want to get to, so that you avoid having a folder that is obviously from a torrent.
- I can improve this by just using YIFY's api, which will be WAY more effective.
- THe only thing I did to ensure some sort of high seeder count was to just take the highest ranked torrent in a list of torrents ordered from highest seeder count to lowest. This could be improved further.
- Get the torrenter to run on windows start until it is finished, then deleting itself, will be a useful way to keep this all going.
- Parasite doesn't get downloaded, since its listed by its original name (Gisaengchung (2019)), but its not saved that way on any torrents. I just gotta make it so that the code can find out more about the data its working with if it doesn't kow where to find it, or just hard-code a correction in there
  but I'd rather avoid that.
- Make this run in the background using python.exe


