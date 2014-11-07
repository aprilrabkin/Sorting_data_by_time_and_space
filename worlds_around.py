import json 
import haversine
# import time
# import datetime
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
    print "hello"


a = WorldsAround()
print a.active_worlds()