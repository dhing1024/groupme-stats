import json
import os
import routines
import argparse
from multiprocessing import Pool, cpu_count
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

	groups = get_all_groups(TOKEN, outputFile = PATH + "/groups.json", sortby = 'num_messages')
	group_ids = groups.index
	arguments = [[id, groups.loc[id, 'name'], TOKEN] for id in group_ids]
	if args.test:
		arguments = [['39064704', groups.loc[id, 'name' ] TOKEN]]

	threadNum = cpu_count()
	print("Number of Groups:", len(group_ids))
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
