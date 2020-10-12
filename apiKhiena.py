import requests
import json
import logging
from pprint import pprint


def imgSearch(imgPath):
    print("imgPath:  ",imgPath)
    URL = "https://api.kheina.com/v1/search"

    filePath = imgPath
    files =  {
    'file': open(filePath, 'rb')
}
    response = requests.post(url=URL,  files=files )
    data = response.text
    try:
        jsonData = json.loads(data)
        #print(jsonData)
        similarity = jsonData["results"][0]["similarity"]
        title =  jsonData["results"][0]["sources"][0]["title"]
        source =  jsonData["results"][0]["sources"][0]["source"]
        artist =  jsonData["results"][0]["sources"][0]["artist"]
        rating =  jsonData["results"][0]["sources"][0]["rating"]
        imgRes = {
            "similarity":similarity,
            "title":title,
            "source":source,
            "artist":artist,
            "rating":rating,
            "localImgPath":imgPath
        }
        print("Similarity:  ",similarity)
        print("Title: "+title)
        print("Source: "+source)
        print("Artist: "+artist)
        print("Rating: ", rating)
        return imgRes

    except ValueError as e:
        logging.error(f"Error while searching image: {e}")
        print(data)
        return
 
#imgSearch("/home/landgrafpc/Изображения/unsort/sort/драконы-неразобр5/all_glory_to_the_dragon_lord_by_harwicks_art-d9zlld2.jpg")