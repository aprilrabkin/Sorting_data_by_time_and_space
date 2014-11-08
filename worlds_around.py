import json 
import haversine
import dateutil.parser

class WorldsAround(object):
  def __init__(self):
    json_user_data = open("sample_user.json").read()
    self.user = json.loads(json_user_data)["user"]
    json_worlds_list = open("sample_worlds.json").read()
    self.worlds_list = json.loads(json_worlds_list)["data"]

  def active_worlds(self):
    userdatetime = dateutil.parser.parse(self.user['usertime'])
    active_worlds_list = []
    for worldhash in self.worlds_list:
      if "timestart" in worldhash["time"]:
        timestart = dateutil.parser.parse(worldhash["time"]["timestart"])
        timeend = dateutil.parser.parse(worldhash["time"]["timeend"])
        if timestart < userdatetime < timeend:
          active_worlds_list.append(worldhash)
      else:
        active_worlds_list.append(worldhash)
    return active_worlds_list


  def within_worlds(self):
    userloc = self.user["userloc"]["coordinates"]
    lat1, long1 = userloc[0], userloc[1]
    within_worlds_list = []
    for world in self.worlds_list:
      worldloc = world["loc"]["coordinates"]
      worldradius = world["radius"]
      lat2, long2 = worldloc[0], worldloc[1]
      distance = haversine.distance((lat1, long1), (lat2, long2))
      if distance < worldradius:
        within_worlds_list.append(world)
    return len(within_worlds_list)



a = WorldsAround()
print a.active_worlds()
print a.within_worlds()