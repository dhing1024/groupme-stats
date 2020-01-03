import json
import os

from groups import get_all_groups
from messageGroup import MessageGroup

def main():

	# Load the configuration variables
	configs = json.load(open('config.json', 'r'))
	TOKEN = configs['token']
	PATH = configs['path']

	if not os.path.exists(PATH):
		os.makedirs(PATH)

	groups = get_all_groups(TOKEN, outputFile = PATH + "/groups.json")
	group_ids = groups.keys()
	for id in group_ids:

		message_output = PATH + "/" + groups[id]
		if not os.path.exists(message_output):
			os.makedirs(message_output)

		mg = MessageGroup.from_groupme_id(TOKEN, id)
		mg.to_html(message_output + "/messages.json")

		user_data_output = message_output + "/user_data"
		if not os.path.exists(user_data_output):
			os.makedirs(user_data_output)

if __name__ == '__main__':
	main()
