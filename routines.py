from messageGroup import MessageGroup
import json
import os

def routine_one(mg, output):

	mg.to_html(output + "/All Messages.html")
	mg.to_json(output + "/messages.json")
	mg.timesort(ascending = False).to_html(output + "/All Messages (Reverse Order).html")
	mg.timesort(ascending = False).to_json(output + "/messages_reversed.json")

	json.dump(mg.info(), open(output + "/info.json", 'w'))

	user_data_output = output + "/user_data"
	if not os.path.exists(user_data_output):
		os.makedirs(user_data_output)

	senders = mg.senders()
	for item in senders:
		mg.filter_senders(item).to_html(user_data_output + "/" + mg.get_name_from_id(item).replace("/", "-") + ".html")

	return
