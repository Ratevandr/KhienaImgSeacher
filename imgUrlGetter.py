from urllib.request import urlopen 
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import urllib
from selenium import webdriver

def getImgInfoFromUrl(imgUrl):
    if (isFurraffinity(imgUrl)):
        return getImgUrlFromFuraffinity(imgUrl)
    
    if (isFurryNetwork(imgUrl)):
        return getImgUrlFromFurryNetwork(imgUrl)

def isFurryNetwork(imgUrl):
    name = urlparse(imgUrl).hostname
    if (name == 'furrynetwork.com'):
        return True
    return False

def isFurraffinity(imgUrl):
    name = urlparse(imgUrl).hostname
    if (name == 'www.furaffinity.net'):
        return True
    return False

def getImgUrlFromFurryNetwork(imgUrl):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    options.add_argument("--headless")
    options.binary_location = "/usr/bin/chromium-browser"
    driver = webdriver.Chrome(options=options)
    driver.get(imgUrl)
    html = driver.page_source
    
    soup = BeautifulSoup(html, "lxml")
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    artist = ""
    tags = []
    imgLink = ""
    #getting artist 
    for link in soup.find_all('div'):
        if (link.has_attr('class') and  link['class'][0] ==  'submission-author__display-name'):
            artist =  link.getText()
   
    for link in soup.find_all('span'):
        if (link.has_attr('class') and len(link['class'])>0  and link['class'][0] ==  'tag__label'):
            tags.append(link.getText())

    for link in soup.find_all('meta'):
        if (link.has_attr('name') and  link['name'] ==  'og:image'):
          imgLink=  link.get('content')
    if (not imgLink):
        imgLink="res/imgHide.png"
    imgInfoStruct = {
        "artist":artist,
        "tags":tags,
        "imgLink":imgLink
    }
    return imgInfoStruct

def  getImgUrlFromFuraffinity(imgUrl):
    url = imgUrl
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    
    artist = ""
    tags = []
    imgLink = ""
    for link in soup.find_all('img'):
        if (link.has_attr('id') and link['id'] == 'submissionImg'):
            imgLink =  'https:'+link.get('src')
    
    for link in soup.find_all('span'):
        if (link.has_attr('class') and len(link['class'])>0  and link['class'][0] ==  'tags'):
            for tagElem in link:
                tags.append(tagElem.getText())

    for link in soup.find_all('div'):
        if (link.has_attr('class') and len(link['class'])>0  and link['class'][0] ==  'section-header'):
            for tagElem in link.find_all('a'):
                for strongElem in tagElem:
                    artist = strongElem.getText()
    if (not imgLink):
        imgLink="res/imgHide.png"
    imgInfoStruct = {
        "artist":artist,
        "tags":tags,
        "imgLink":imgLink
    }
    return imgInfoStruct


      
    
    
#print(getImgUrlFromFurryNetwork("https://furrynetwork.com/artwork/341709/dragon-tea/"))

#print(getImgUrlFromFuraffinity("https://www.furaffinity.net/view/28967718/"))