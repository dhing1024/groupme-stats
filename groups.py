import json
from http import client
import os
import requests
import pprint

def get_all_groups(token, outputFile = None):

	# Request parameters
	server = 'api.groupme.com'
	path = '/v3/groups'
	connection = client.HTTPSConnection(server)

	# Loop through pages of GroupMe messages using the GroupMe developer's API
	data, dict = [], {}
	pageNum = 1
	while True:

		# Send request
		params = '?'+ 'token=' + token + '&page=' + str(pageNum) + '&omit=memberships'
		print("Request: " + "https://" + server + path + params, end = '...')
		response = requests.get('https://' + server + path + params)
		if len(response.json()['response']) == 0:
			print("ending")
			break
		print("success")

		# Add response items data and dict
		groups = response.json()['response']
		for i in range(len(groups)):
			newData = {groups[i]['group_id'] : groups[i]['name']}
			dict[groups[i]['group_id']] = groups[i]['name']
			data.append(newData)

		pageNum += 1

	# Create new file and write to local file
	if outputFile is not None:
		file = open(outputFile, 'w')
		file.truncate(0)
		pprint.pprint(data, file)
		file.close()

	print("Download Finished!")
	return dict
