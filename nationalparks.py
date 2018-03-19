#!/usr/local/bin/python3

from requests import get
from pickle import dump, load
import pprint

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
        response = get(url, params=params)
        response = response.json()
        return response

class ParkScraper:
    """ 
    The ParkScraper class contains the functions and values for scraping
    national park data.
    """
    def __init__(self, keypath: str="./key.txt"):
        self.BASE_URL_ = "https://developer.nps.gov/api/v1"
        self.api_key   = ""
        self.set_key(keypath)

    def set_key(self, path: str):
        with open(path) as keyfile:
            key = str(keyfile.readline()).strip()
            self.api_key = key

    def get_parks(self) -> dict:
        path = "/parks"
        parks_data = []
        for page in range(0, 10):
            print(".", end="", flush=True)
            params = {"api_key": self.api_key, 
                      "start": str(page * 100),
                      "limit": "100",
                      "fields": "images"}
            response = REST.get_json(self.BASE_URL_, path, params)
            parks_data += response["data"]
        print() # make a new line separate from all the dots
        return parks_data

        
if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=2)
    """
    ps = ParkScraper()
    park_data = ps.get_parks()
    national_parks = {}
    for park in park_data:
        if park["designation"] == "National Park":
            national_parks[park["fullName"]] = park
            print(park["designation"], " -- ", park["fullName"])
            pp.pprint(park)
    with open("./db.pckl", "wb") as outfile:
        dump(national_parks, outfile)

    """
    national_parks = {}
    with open("./db.pckl", "rb") as infile:
        national_parks = load(infile)
        print(national_parks.keys())
    for park in national_parks.keys():
        pp.pprint(national_parks[park])
    #"""

    print("Done.")
