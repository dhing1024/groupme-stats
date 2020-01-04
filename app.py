import json
import os
import routines
import argparse

from groups import get_all_groups
from messageGroup import MessageGroup

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--test", help = "Test Program", action = "store_true")
args = parser.parse_args()

def main():

	# Load the configuration variables
	configs = json.load(open('config.json', 'r'))
	TOKEN = configs['token']
	PATH = configs['path']

	if not os.path.exists(PATH):
		os.makedirs(PATH)

	groups = get_all_groups(TOKEN, outputFile = PATH + "/groups.json")
	group_ids = groups.keys()

	if args.test:
		group_ids = ['47833867']

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

	routines.dump_group_level_data(mg, output)
	routines.dump_user_data(mg, output)
	routines.routine_three(mg, output)

	return

if __name__ == '__main__':
	main()
