import json 
import haversine
import dateutil.parser

class WorldsAround(object):
  def __init__(self, user, worlds):
    json_user_data = open(user).read()
    self.user = json.loads(json_user_data)["user"]
    json_worlds_list = open(worlds).read()
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
    self.active_worlds_list = active_worlds_list


  def within_worlds(self):
    userloc = self.user["userloc"]["coordinates"]
    lat1, long1 = userloc[0], userloc[1]
    within_worlds_list = []
    for world in self.active_worlds_list:
      worldloc = world["loc"]["coordinates"]
      worldradius = world["radius"]
      lat2, long2 = worldloc[0], worldloc[1]
      distance = haversine.distance((lat1, long1), (lat2, long2))
      if distance < worldradius:
        within_worlds_list.append(world)
    self.within_worlds_list = within_worlds_list

  def rank_worlds(self):
    worlds_with_shared_tag_count = []
    for world in self.within_worlds_list:
      count = 0
      for worldtag in world["tags"]:
        for usertag in self.user["tags"]:
          if worldtag == usertag:
            count += 1
      world["shared_tag_count"] = count
      worlds_with_shared_tag_count.append(world)
    ranked_worlds = sorted(worlds_with_shared_tag_count, key=lambda k: k['shared_tag_count'], reverse=True) 
    return ranked_worlds
            
a = WorldsAround("sample_user.json", "sample_worlds.json")
a.active_worlds()
a.within_worlds()
print a.rank_worlds()