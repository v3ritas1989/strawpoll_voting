# strawpoll_voting

# Description
This programm is voting for you on strawpoll.de as often as you like using a proxy list a random request header information.
Written in pyhton 3.x


## HOW TO
```
- Clone this repository
- Go to https://github.com/mozilla/geckodriver/releases
- And download the geckodriver.exe into the same folder as this repository
- Open your CMD
- CD path:to\your\clones\strawpoll_voting
- python Strawpoll_voting.py
```

You will get asked for the strawpoll link.
Copy and Paste the complete link of the strawpoll then proceed with instructions

## DEPENDENCIES

you may have to install dependencies

- pip install urllib
- pip install ssl
- pip install bs4
- pip install selenium
- pip install os
- pip install csv

## Known Issue:

#1
It may be that some of the provided proxy are not working any more or some of those in the list are not https proxys
For some reason this only works with https. HTTP only proxys will give you a long waiting time per call
If someone has the time, change the proxylist.csv so that it only contains https proxys or do an inital check if proxy is available an https

#2
the inital request to the poll to retrieve its info is not made from the proxylist, but has a static proxy programmed.
It should pull its infor from the list, but before that it trys one it should already know if its working

#3
the inital request to the poll to retrieve its info is not made with a static header information and is not randomised as later
in the voting process. This may cause an issue later.
