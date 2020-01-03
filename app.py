import json
import os

from groups import get_all_groups
from messages import get_messages, save_html

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
		data = get_messages(TOKEN, id, outputFile = message_output + "/messages.json", verbose = True )

		user_data_output = message_output + "/user_data"
		if not os.path.exists(user_data_output):
			os.makedirs(user_data_output)
		save_html(data, outputPath = user_data_output )

if __name__ == '__main__':
	main()
