import json
from http import client
import os
import requests
import pprint
import pandas as pd

def get_all_groups(token, outputFile = None, sortby = 'None', ascending = False):

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
			dict[groups[i]['group_id']] = [groups[i]['name'], groups[i]['messages']['count']]
			data.append(newData)
		pageNum += 1

	# Create new file and write to local file
	if outputFile is not None:
		file = open(outputFile, 'w')
		file.truncate(0)
		pprint.pprint(data, file)
		file.close()

	retval = pd.DataFrame.from_dict(dict, orient = 'index')
	retval.rename(columns = { 0 : 'name', 1 : 'num_messages'}, inplace = True)

	if sortby is not None:
		retval.sort_values(sortby, ascending = ascending, inplace = True)

	print("Download Finished!")
	return retval
