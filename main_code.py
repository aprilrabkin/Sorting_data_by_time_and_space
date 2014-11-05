import json 
json_user_data=open("user.json").read()
data = json.loads(json_user_data)
print(data)