import json 
json_user_data=open("user.json").read()
data = json.loads(json_user_data)
print(data)

import math

def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km
 
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
 
    return d

lat1 = -73.94728440000002; lat2 = lat1 + 0.000001; long1 = 40.682783; long2 = long1
print( distance((lat1, long1), (lat2, long2)) )