#!/usr/local/bin/python3

from requests import get

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
                      "limit": "100"}
            response = REST.get_json(self.BASE_URL_, path, params)
            parks_data += response["data"]
        print() # make a new line separate from all the dots
        return parks_data

        
if __name__ == "__main__":
    ps = ParkScraper()
    park_data = ps.get_parks()
    for park in park_data:
        if park["designation"] == "National Park":
            print(park["designation"], " -- ", park["fullName"])
