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
		routines.routine_one(mg, message_output)
		#mg.to_html(message_output + "/All Messages.html")
		#mg.to_json(message_output + "/messages.json")
		#mg.timesort(ascending = False).to_html(message_output + "/All Messages (Reverse Order).html")
		#mg.timesort(ascending = False).to_json(message_output + "/messages_reversed.json")
		#json.dump(mg.info(), open(message_output + "/info.json", 'w'))
		#user_data_output = message_output + "/user_data"
		#if not os.path.exists(user_data_output):
		#	os.makedirs(user_data_output)

		#senders = mg.senders()
		#for item in senders:
		#	mg.filter_senders(item).to_html(user_data_output + "/" + mg.get_name_from_id(item).replace("/", "-") + ".html")

def execute_routines(mg, configs):
	configs = json.load(open('config.json', 'r'))
	TOKEN = configs['token']
	PATH = configs['path']


	return

if __name__ == '__main__':
	main()
