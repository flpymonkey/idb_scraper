#!/usr/local/bin/python3

import json
import requests
from pickle import dump, load

class REST:
    """
    This class contains some useful functions for using the requests library.
    As of right now, it's just a container for the get_json function.
    """
    def get_json(base: str, request_path: str, params: dict={}) -> list:
        """
        Return the JSON result for the given request path
        request_path - the path to the data we are requesting
        """
        url = base + request_path
        response = requests.get(url, params=params)
        # Remove some stupid flickr response garbage "jsonFlickrAPI("
        text = response.text[14:-1]
        result = json.loads(text)
        return result

class ImageScraper:
    """ 
    The ImageScraper class contains the functions and values for scraping
    image data.
    """
    def __init__(self, keypath: str="./flickrkey.txt"):
        self.BASE_URL_ = "https://api.flickr.com/services/rest"
        self.api_key   = ""
        self.set_key(keypath)

    def set_key(self, path: str):
        with open(path) as keyfile:
            key = str(keyfile.readline()).strip()
            self.api_key = key

    def get_photos(self) -> dict:
        path = ""
        params = {"api_key": self.api_key, 
                  "method": "flickr.photos.search",
                  "format": "json",
                  "text":   "yellowstone national park"}
        response = REST.get_json(self.BASE_URL_, path, params)
        return response

        
if __name__ == "__main__":
    image_scraper = ImageScraper()
    photo_data = image_scraper.get_photos()
    for photo in photo_data["photos"]["photo"]:
        url = "https://c1.staticflickr.com/{}/{}/{}_{}_h.jpg".format(
                photo["farm"],
                photo["server"],
                photo["id"],
                photo["secret"])
        print(url)
    print("Done.")

