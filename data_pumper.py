#!/usr/local/bin/python3

from sqlalchemy import create_engine
from pickle import dump, load

engine_string = None
with open("./dbinfo.txt", "r") as dbinfo:
    engine_string = str(dbinfo.readline())

if engine_string is None:
    raise Exception("Could not load dbinfo.txt")
engine = create_engine(engine_string)

connection = engine.connect()

national_parks = {}
with open("./db.pckl", "rb") as infile:
    national_parks = load(infile)
    # print(national_parks.keys())
for park in national_parks.keys():
    # print(national_parks[park])
    national_park = national_parks[park]
    print (national_park.keys())
    try:
        q = "INSERT INTO parks VALUES('{}','{}','{}','{}','{}','{}','{}','{}')".format(national_park['fullName'],
                            national_park['states'],
                            national_park['latLong'],
                            national_park['description'],
                            national_park['directionsInfo'],
                            national_park['url'],
                            national_park['weatherInfo'],
                            national_park['directionsUrl'])
        result = connection.execute(q)
    except Exception e:
        print(e)

print("Done.")

# for row in result:
#     print(row['name'])
