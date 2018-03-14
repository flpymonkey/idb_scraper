import json
import pprint
import requests
from pickle import dump, load

all_cameras = []

class REST:
    """
    This class contains some useful functions for using the requests library.
    As of right now, it's just a container for the get_json function.
    """
    def get_json(base: str, request_path: str, params: dict={}, search: str) -> list:
        """
        Return the JSON result for the given request path
        request_path - the path to the data we are requesting
        """
        url = base + request_path + search # search ex: "((search=Canon&search=Eos&search=80D)&categoryPath.id!=ab&(categoryPath.id=abcat0401000))"
        response = requests.get(url, params=params)
        print(response)
        result = json.loads(response.text)
        return result

class BestBuyScraper:
    """
    The ImageScraper class contains the functions and values for scraping
    image data.
    """
    def __init__(self, keypath: str="./bestbuykey.txt"):
        self.BASE_URL_ = "https://api.bestbuy.com/v1"
        self.api_key   = ""
        self.set_key(keypath)

    def set_key(self, path: str):
        with open(path) as keyfile:
            key = str(keyfile.readline()).strip()
            self.api_key = key
            print(key)

    def get_camera(self, text) -> dict:
            path = "/products"
            params = {"apiKey": self.api_key,
                      "format": "json",
                      "show": "details.name"}
            splittext = text.split()
            search = "((search=" + splittext[0]
            i = iter(splittext)
            # next(i) FIXME
            # for e in i:
            #     search += "&search\=" + e
            #search += ")&(categoryPath.id=abcat0401000))"
            #/products((search=Canon&search=EOS&search=80D)&(categoryPath.id=abcat0401000))?apiKey=&show=details.name&format=json
            response = REST.get_json(self.BASE_URL_, path, params, search)
            return response
# /v1/products?apiKey=mjEyiiINwXK3fFgNaAyd8x8c&format=json&show=details.value&categoryPath.id=abcat0401000&search=CanonEOS80D
scraper = BestBuyScraper()
result = scraper.get_camera("Canon")
print(result)
