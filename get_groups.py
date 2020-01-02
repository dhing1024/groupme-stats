import json
from http import client
import os
import requests
import pprint

# Load the configuration variables
configs = json.load(open('config.json', 'r'))
token = configs['token']

# Request parameters
server = 'api.groupme.com'
path = '/v3/groups'
connection = client.HTTPSConnection(server)

fileName = 'groups.json'
file = open(fileName, 'w')
file.truncate(0)

# Loop through pages of GroupMe messages using the GroupMe developer's API
data = []
pageNum = 1
print("Beginning Download...")
while pageNum < 10:
    params = '?'+ 'token=' + token + '&page=' + str(pageNum) + '&omit=memberships'
    print("Request: " + "https://" + server + path + params)
    response = requests.get('https://' + server + path + params)
    if response.status_code != 200:
        break
    groups = response.json()['response']
    print(type(groups[0]))
    for i in range(len(groups)):
        newData = {groups[i]['group_id'] : groups[i]['name']}
        data.append(newData)

    #data.extend(groups)
    pageNum += 1

# Write JSON data to local .json file
print(type(json.dumps(data)))
pprint.pprint(data)

#pprint.pprint(json.dumps(data))
file.close()
print("Download Finished!")
