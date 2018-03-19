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
with open("./dbcams.pckl", "rb") as infile:
    cams = load(infile)
for k in cams:
    #print(k)
    print(k)

print("Done.")
