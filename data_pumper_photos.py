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

#photos_table = metadata.tables['photos']

photos = {}
with open("./dbpics.pckl", "rb") as infile:
    photos = load(infile)
for k in photos:
    print(k)
    # photo = photos[k]
    # try:
    #     ins = photos_table.insert().values(name=photo['fullName'],
    #                                 states=photo['states'],
    #                                 latlong=photo['latLong'],
    #                                 description=photo['description'],
    #                                 directions=photo['directionsInfo'],
    #                                 url=photo['url'],
    #                                 weather=photo['weatherInfo'],
    #                                 directionsUrl=photo['directionsUrl'])
    #
    #     result = connection.execute(ins)
    #     print(result)
    # except Exception as e:
    #     pass

print("Done.")
