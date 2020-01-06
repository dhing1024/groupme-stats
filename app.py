import json
import os
import routines
import argparse
from multiprocessing import Pool, cpu_count
from groups import get_all_groups
from messageGroup import MessageGroup

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--test", help = "Test Program", action = "store_true")
parser.add_argument("-i", "--id", help = "GroupMe ID", action = "store", nargs = "+")
parser.add_argument("-f", "--file", help = "Input file", action = "store", nargs = "+")
args = parser.parse_args()
print(args)


def main():

	# Load the configuration variables
	configs = json.load(open('config.json', 'r'))
	TOKEN = configs['token']
	PATH = configs['path']
	if not os.path.exists(PATH):
		os.makedirs(PATH)

	main_args = {'id' : args.id, 'file' : args.file}

	groups = get_all_groups(TOKEN, outputFile = PATH + "/groups.json", sortby = 'num_messages')
	group_ids = groups.index
	groups_selected = []

	if args.id is not None:
		groups_selected.extend(args.id)

	if args.file is not None:
		new_ids = []
		for file in args.file:
			print("Importing File:", args.file)
			new_ids.extend( open(file, 'r+').readlines())
		new_ids = [x[0:-1] for x in new_ids]
		groups_selected.extend(new_ids)

	if args.test:
		groups_selected = ['39064704']

	if not any(main_args.values()):
		groups_selected = group_ids

	print("Groups: ", groups_selected)
	arguments = [[id, groups.loc[id, 'name'], TOKEN] for id in groups_selected]

	threadNum = cpu_count()
	print("Number of Groups:", len(groups_selected))
	print("Downloading with", threadNum, "threads")
	p = Pool(threadNum)
	ALL_GROUP_DATA = p.map(create_mg, arguments)
	for item in ALL_GROUP_DATA:
		id = item[0]
		mg = item[1]
		main_routine(id, mg, configs, groups)


def create_mg(arguments):
	id = arguments[0]
	name = arguments[1]
	token = arguments[2]
	print("Getting messages for GROUPME", id, ":", name)
	mg = MessageGroup.from_groupme_id(token, id)
	print("Received", mg.num_messages(), "messages from GROUPME", id, ":", name)
	return (id, mg)


def main_routine(id, mg, configs, groups ):
	PATH = configs['path']
	message_output = PATH + "/" + groups.loc[id, 'name']
	if not os.path.exists(message_output):
		os.makedirs(message_output)
	execute_routines(mg, id, groups.loc[id, 'name'], message_output, configs)
	return


def execute_routines(mg, id, name, output, configs):
	configs = json.load(open('config.json', 'r'))
	TOKEN = configs['token']
	PATH = configs['path']

	print("Starting Dump for " + name + " (" + id +  ")")
	routines.dump_group_level_data(mg, output)
	print("Dumped Group Level Data for " + name)
	routines.dump_user_data(mg, output)
	print("Dumped User Level Data for " + name)
	routines.routine_three(mg, output)
	return


if __name__ == '__main__':
	main()
