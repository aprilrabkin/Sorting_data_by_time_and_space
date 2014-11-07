import json 
json_user_data = open("sample_user.json").read()
user = json.loads(json_user_data)
json_worlds_list = open("sample_worlds.json").read()
worlds_list = json.loads(json_worlds_list)