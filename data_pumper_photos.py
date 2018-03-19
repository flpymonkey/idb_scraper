#!/usr/local/bin/python3
from sqlalchemy import create_engine, MetaData
from pickle import dump, load
import pprint

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

pp = pprint.PrettyPrinter(indent=2)
photos = {}
with open("./dbpics.pckl", "rb") as infile:
    photos = load(infile)
for photo in photos:
    pp.pprint(photo)
    ins = photos_table.insert().values(photographer=photo['author'],
                                    title=photo['title'],
                                    date=photo['date taken'],
                                    description=photo['description'],
                                    image_url=photo['url'],
                                    flickr_url=photo['direct url'],
                                    likes=photo['Favorites'],
                                    park=photo['park'])

    try:
        pass
        #result = connection.execute(ins)
        #print(result)
    except Exception as e:
        print("Insertion error:", e)

print("Done.")
