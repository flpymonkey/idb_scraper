#!/usr/local/bin/python3
from sqlalchemy import create_engine, MetaData
from pickle import dump, load

engine_string = None
with open("./dbinfo.txt", "r") as dbinfo:
    engine_string = str(dbinfo.readline())

if engine_string is None:
    raise Exception("Could not load dbinfo.txt")
engine = create_engine(engine_string)

connection = engine.connect()

metadata = MetaData()
metadata.reflect(bind=engine)

parks_table = metadata.tables['parks']

national_parks = {}
with open("./db.pckl", "rb") as infile:
    national_parks = load(infile)
for park in national_parks.keys():
    national_park = national_parks[park]
    try:
        ins = parks_table.insert().values(name=national_park['fullName'],
                                    states=national_park['states'],
                                    latlong=national_park['latLong'],
                                    description=national_park['description'],
                                    directions=national_park['directionsInfo'],
                                    url=national_park['url'],
                                    weather=national_park['weatherInfo'],
                                    directionsUrl=national_park['directionsUrl'])

        result = connection.execute(ins)
        print(result)
    except Exception as e:
        pass

print("Done.")
