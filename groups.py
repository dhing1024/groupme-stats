import json
from http import client
import os
import requests
import pprint

# Save to a groups.json
def get_all_groups(token):

	# Request parameters
	server = 'api.groupme.com'
	path = '/v3/groups'
	connection = client.HTTPSConnection(server)

	# Loop through pages of GroupMe messages using the GroupMe developer's API
	data = []
	dict = {}
	pageNum = 1
	print("Beginning Download...")
	while pageNum < 10:
		params = '?'+ 'token=' + token + '&page=' + str(pageNum) + '&omit=memberships'
		print("Request: " + "https://" + server + path + params)
		response = requests.get('https://' + server + path + params)
		if response.status_code != 200:
			break
		groups = response.json()['response']
		for i in range(len(groups)):
			newData = {groups[i]['group_id'] : groups[i]['name']}
			dict[groups[i]['group_id']] = groups[i]['name']
			data.append(newData)
		pageNum += 1

	# Create new file and write to local file
	fileName = 'groups.json'
	file = open(fileName, 'w')
	file.truncate(0)
	pprint.pprint(data, file)
	file.close()

	print("Download Finished!")
	return dict


if __name__ == '__main__':
	get_all_groups()
