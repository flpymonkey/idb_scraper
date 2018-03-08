from sqlalchemy import create_engine
from pickle import dump, load

engine = create_engine('')

connection = engine.connect()

national_parks = {}
with open("./db.pckl", "rb") as infile:
    national_parks = load(infile)
    # print(national_parks.keys())
for park in national_parks.keys():
    # print(national_parks[park])
    national_park = national_parks[park]
    print (national_park.keys())
    q = "INSERT INTO parks VALUES('{}','{}','{}','{}','{}','{}','{}','{}')".format(national_park['fullName'],
                        national_park['states'],
                        national_park['latLong'],
                        national_park['description'],
                        national_park['directionsInfo'],
                        national_park['url'],
                        national_park['weatherInfo'],
                        national_park['directionsUrl'])
    result = connection.execute(q)
#
# print("Done.")
#
#
# for row in result:
#     print(row['name'])
