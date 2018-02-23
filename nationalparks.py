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
        params = {"api_key": self.api_key}
        parks_page1 = REST.get_json(self.BASE_URL_, path, params)
        return parks_page1

        
if __name__ == "__main__":
    ps = ParkScraper()
    response = ps.get_parks()
    for park_data in response["data"]:
        print(park_data["fullName"])
