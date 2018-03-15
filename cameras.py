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
    def get_json(base: str, request_path: str, search: str, params: dict={}) -> list:
        """
        Return the JSON result for the given request path
        request_path - the path to the data we are requesting
        """
        url = base + request_path + search # search ex: "((search=Canon&search=Eos&search=80D)&categoryPath.id!=ab&(categoryPath.id=abcat0401000))"
        response = requests.get(url, params=params)
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

    def get_camera(self, text) -> dict:
            path = "/products"
            params = {"apiKey": self.api_key,
                      "format": "json",
                      "show": "regularPrice,details.value"}
            splittext = (text + " " + " Body Only").split()
            search = "((search=" + splittext[0]
            i = iter(splittext)
            b = next(i)
            for e in i:
                search += "&search=" + e
            search += ")&(categoryPath.id=abcat0401000))"
            response = REST.get_json(self.BASE_URL_, path, search, params)
            return response

if __name__ == "__main__":
    failed = []
    # scraper = BestBuyScraper()
    # result = scraper.get_camera("Canon EOS 80D")
    # print(result)
    with open("./dbpics.pckl", "rb") as infile:
        pics = load(infile)
        results = []
        scraper = BestBuyScraper()
        cams = set()
        for e in pics:
            if e['camera:'] not in cams:
                cams.add( e['camera:'])
                try:
                    raw_data = scraper.get_camera(e['camera:'])
                    price = raw_data['products'][0]['regularPrice']
                    formatted_data = {'name': e["camera:"], 'price': price, 'details': raw_data['products'][0]['details']}
                    results.append(formatted_data)
                    print('Added!: '+ e['camera:'])
                except:
                    print("failed" + e['camera:'])
                    failed.append(e['camera:'])
        print("Done!")
        with open("./dbcams.pckl", "wb") as outfile:
            dump(results, outfile)
        print (cams)
        print("Failed:")
        print(failed)

    # for park in national_parks:
    #     print (park)
    #     park_name = park
    #     try:
    #         get_park_photos(park_name)
    #         print("Done.")
    #     except:
    #         failed.append(park_name)
    # with open("./dbpics.pckl", "wb") as outfile:
    #     dump(all_park_photos, outfile)
    # print ("Dumped!")
    # print(failed)
