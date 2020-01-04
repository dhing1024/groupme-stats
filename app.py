import json
import os
import routines

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
		execute_routines(mg, message_output, configs)

def execute_routines(mg, output, configs):
	configs = json.load(open('config.json', 'r'))
	TOKEN = configs['token']
	PATH = configs['path']

	routines.routine_one(mg, output)
	routines.routine_two(mg, output)
	routines.routine_three(mg, output)

	return

if __name__ == '__main__':
	main()
