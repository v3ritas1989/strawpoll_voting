from urllib import *
import urllib.request
import ssl
import bs4 as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from numpy import genfromtxt
import os

ssl._create_default_https_context = ssl._create_unverified_context
site = input('Copy paste the URL of the Strawpoll you want to vote in?')
##site='https://strawpoll.de/'
poll='xf83w84'
sitepoll=site+poll
proxy = {'http' : 'http://94.130.14.146:31288' }##{'http' : 'http://94.130.14.146:31288' }
hdr = [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'),
       ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
       ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'),
       ('Accept-Encoding', 'none'),
       ('Accept-Language', 'en-US,en;q=0.8'),
       ('Connection', 'keep-alive')]
##imgdump = 'imgdump/'+qinput+'/'
## Test basic variables
##print('Actual IP', urllib.request.urlopen('http://httpbin.org/ip').read())
##print('Actual header',urllib.request.urlopen(site).read())
def openPage(site,hdr,proxy,poll):
    proxy_support = urllib.request.ProxyHandler(proxy)
    opener = urllib.request.build_opener(proxy_support)
    urllib.request.install_opener(opener)
    opener.addheaders = hdr


    site = site+poll
    print(site)
    req = urllib.request.Request(site)#
    ##print(str(req))
    response = opener.open(req).read()
    ## Test request IP  ---> do not too often or get banned by httpbin, only for short test
    ##print('Fake IP', opener.open('http://httpbin.org/ip').read())
    ##print(response)

    soup = bs.BeautifulSoup(response,'lxml')
    
    ##print(body)
    return(soup)

def getpolls(soup):
    body = soup.find('div', {'class' : 'voteanswers'})
    return body

def getpollanswers(soup):
##def pollanswers(soup,click=False,wantedanswer=0,count=0):
    body = getpolls(soup)
    pollanswers = []
##    print("Printing answer: ",wantedanswer)
    for answer in body.findAll('div', {'class' : 'checkbox'}):
        desc = answer.text.strip()
        name = answer.find('input').get('id')
        new = []
        ##print(answer.text.strip())
        new.append(desc)
        ##print(answer.find('input').get('name'))
        new.append(name)
        pollanswers.append(new)
        
    ##print(pollanswers)
    return pollanswers

def seleniumclickbutton(sitepoll,answer,count):
    from fake_useragent import UserAgent
    from selenium.webdriver.common.proxy import Proxy, ProxyType
    from selenium.webdriver.firefox.options import Options
    proxy_list = getproxy()
    for i in range(count):
        agent_IP = proxy_list[i][0]
        agent_Port = proxy_list[i][1]
        print("\n")
        print("\n")
        print('Voting with IP: ',agent_IP+":"+agent_Port)
        useragent = UserAgent()
        profile = webdriver.FirefoxProfile()
        ## randomise browser identity
        profile.set_preference("general.useragent.override", useragent.random)
        ## proxy settiongs
        
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.share_proxy_settings", True)
        profile.set_preference("network.http.use-cache", False)
        profile.set_preference("network.proxy.http", agent_IP)
        profile.set_preference("network.proxy.http_port", int(agent_Port))
        profile.set_preference('network.proxy.ssl_port', int(agent_Port))
        profile.set_preference('network.proxy.ssl', agent_IP)
        profile.set_preference('network.proxy.socks', agent_IP)
        profile.set_preference('network.proxy.socks_port', int(agent_Port))

        
        ## init browser
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Firefox(firefox_profile=profile, options=options)
        try:
            driver.get(sitepoll)
        except:
            print("something went wrong")
            driver.close()
            ##os.system("taskkill /im geckodriver.exe")
            continue
        ## check IP: 'https://www.iplocation.net/find-ip-address'
        ## Check User Agent : https://www.whatismybrowser.com/detect/what-is-my-user-agent
        ## Selecting checkbox
        driver.find_element_by_xpath('//label[@for="'+answer+'"]').click()
        ## Submiting by clicking vote button
        driver.find_element_by_xpath('//*[@id="votebutton"]').click()
        ## getting vote response
        try:
            print(driver.find_element_by_id('voteresponse').text)
        except:
            print("something went wrong", "rU")
        driver.close()
        ##os.system("taskkill /im geckodriver.exe")

        
def getproxy():
    import csv
    file = open('proxylist.csv')
    reader = csv.reader(file, delimiter=":")
    proxy = []
    for row in reader:
        proxy.append(row)
    return proxy
    

def getuserquestion(pollanswers):
    
    print("\n")
    print("Your possible poll answers")
    print("####################################################")
    x = 1
    for answer in pollanswers:
        print("Answer ", x , ": ",answer[0])
        x+=1
    print("####################################################")
    #print(len(pollanswers))
    while True:
        try:
            question = int(input('What answer do you want to boost?'))
        except ValueError:
            print("Thats not an answer! Please choose an Answer and type its Index!")
        else:
            if question > len(pollanswers):
                print("Thats not an answer! Please choose an Answer and type its Index!")
            else:
                print("You chose answer " ,question , " : ",pollanswers[question-1][0])
                break

    ##print(question)
    result = pollanswers[question-1][1]
    ##print(result)
    return result     
            
    
def getuserquestioncount():
    try:
        count = int(input('How often do you want this answer clicked?'))
    except ValueError:
        print("Thats not an answer! Please choose an Answer and type its Index!")

    return count


    
soup = openPage(site,hdr,proxy,poll)
answersarray=getpollanswers(soup)
answer=getuserquestion(answersarray)
count=getuserquestioncount()
seleniumclickbutton(sitepoll,answer,count)


