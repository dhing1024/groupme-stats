from messageGroup import MessageGroup
import json
import os
import matplotlib.pyplot as plt

# GROUP LEVEL ROUTINES

def dump_group_level_data(mg, output):

	mg.to_html(output + "/All Messages.html")
	mg.to_json(output + "/messages.json")
	mg.timesort(ascending = False).to_html(output + "/All Messages (Reverse Time Order).html")
	mg.timesort(ascending = False).to_json(output + "/messages_reversed.json")
	mg.likesort(ascending = False).to_html(output + "/Most Popular.html")
	mg.likesort(ascending = False).to_json(output + "/most_popular.json")
	json.dump(mg.info(), open(output + "/info.json", 'w'))

	dump_top_likers(mg, output)
	return

def dump_top_likers(mg, output):

	users = mg.get_user_data()
	top_n = len(users.index) if len(users.index) < 25 else 25
	# Dump Likes from past 6 months
	users.sort_values('likes_given_past6months', inplace = True, ascending = False)
	newPlot = users.iloc[range(top_n)].plot(kind = 'bar', \
		x = 'latest_name', y = 'likes_given_past6months', \
		title = 'Likes Given by User in Past 6 Months', \
		legend = False, \
		figsize = (15, 10) ,fontsize = 12)
	newPlot.set_xlabel("Name")
	newPlot.set_ylabel("Likes")
	fig2 = newPlot.get_figure()
	plt.tight_layout()
	fig2.savefig(output + "/Likes Given By User (Past 6 Months).png")

	#dump likes from all time
	users.sort_values('likes_given_total', inplace = True, ascending = False)
	newPlot = users.iloc[range(top_n)].plot(kind = 'bar', \
		x = 'latest_name', y = 'likes_given_total', \
		title = 'Likes Given by User (All Time)', \
		legend = False, \
		figsize = (15, 10) ,fontsize = 12)
	newPlot.set_xlabel("Name")
	newPlot.set_ylabel("Likes")
	fig2 = newPlot.get_figure()
	plt.tight_layout()
	fig2.savefig(output + "/Likes Given By User (All Time).png")
	return

# USER LEVEL ROUTINES

def dump_user_data(mg, output):

	user_data_output = output + "/user_data"
	if not os.path.exists(user_data_output):
		os.makedirs(user_data_output)

	senders = mg.senders()
	for item in senders:

		user_path = user_data_output + "/" + mg.get_name_from_id(item).replace("/", "-")
		if not os.path.exists(user_path):
			os.makedirs(user_path)

		user_mg = mg.filter_senders(item)
		user_mg.to_html(user_path + "/All Messages Sent.html")
		user_mg.to_json(user_path + "/messages_sent.json")
		user_mg.timesort(ascending = False).to_html(user_path + "/All Messages Sent (Reverse Time Order).html")
		user_mg.timesort(ascending = False).to_json(user_path + "/messages_sent_reversed.json")
		user_mg.likesort(ascending = False).to_html(user_path + "/Most Popular Messages.html")
		user_mg.likesort(ascending = False).to_json(user_path + "/most_popular_messages.json")
		user_mg.liked_by(item).to_html(user_path + "/Liked Messages.html")
		user_mg.liked_by(item).to_json(user_path + "/liked_messages.json")
		json.dump(user_mg.info(), open(user_path + "/info.json", 'w'))

	return

def routine_three(mg, output):

	return
