#!/usr/local/bin/python3
from sqlalchemy import create_engine, MetaData
from pickle import dump, load
import pprint

def get_detail(details, detail_name):
    """
    Return the value for the given detail_name in a camera's details
    """
    for detail_dict in details["details"]:
        if detail_dict["name"] == detail_name:
            return detail_dict["value"]
    return None
    #raise Exception("ERROR: Could not find detail \"" + detail_name + "\" for " + details["name"] + "!")

engine_string = None
with open("./dbinfo.txt", "r") as dbinfo:
    engine_string = str(dbinfo.readline())

if engine_string is None:
    raise Exception("Could not load dbinfo.txt")
engine = create_engine(engine_string)

connection = engine.connect()

metadata = MetaData()
metadata.reflect(bind=engine)

cameras_table = metadata.tables['cameras']

pp = pprint.PrettyPrinter(indent=2)
cams = {}
with open("./dbcams.pckl", "rb") as infile:
    cams = load(infile)
for k in cams:
    ins = cameras_table.insert().values(
            name=k['name'],
            price=k['price'],
            weight=get_detail(k, "Product Weight"),
            type=get_detail(k, "Digital Camera Type"),
            water_resistant=get_detail(k, "Water Resistant"),
            total_megapixels=get_detail(k, "Total Megapixels"),
            effective_megapixels=get_detail(k, "Effective Megapixels"),
            iso=get_detail(k, "ISO Settings"),
            shutter_speeds=get_detail(k, "Shutter Speeds"),
            video_resolution=get_detail(k, "Video Resolution"),
            image_resolution=get_detail(k, "Image Resolution (Display)"),
            sensor=get_detail(k, "Image Sensor Type"))
            
    try:
        result = connection.execute(ins)
        print(result)
    except Exception as e:
        print("Insertion error:", e)

print("Done.")
