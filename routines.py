from messageGroup import MessageGroup
import json
import os
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta, date
# GROUP LEVEL ROUTINES

def dump_group_level_data(mg, output):

	mg.to_html(output + "/All Messages.html")
	mg.to_json(output + "/messages.json")
	mg.timesort(ascending = False).to_html(output + "/All Messages (Reverse Time Order).html")
	mg.timesort(ascending = False).to_json(output + "/messages_reversed.json")
	mg.likesort(ascending = False).to_html(output + "/Most Popular.html")
	mg.likesort(ascending = False).to_json(output + "/most_popular.json")
	json.dump(mg.info(), open(output + "/info.json", 'w'))

	mg.users_to_html(output + "/User Data.html", sortby = 'num_messages', ascending = False)
	mg.filter_timedate_range(start = datetime.now() - timedelta(days = 180)).users_to_html(output + "/User Data (Last 6 Months).html", sortby = 'num_messages_past6months', ascending = False)

	dump_top_likers(mg, output)
	dump_total_activity(mg, output)
	dump_sender_activity(mg, output)
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

def dump_total_activity(mg, output):
	monthly_messages = mg.dataset.groupby( pd.Grouper(freq = "M") ).apply(lambda x : len(x))
	newPlot = monthly_messages.plot(kind = 'line', ylim = (0, monthly_messages.max() * 1.1),\
		figsize = (10, 7.5), fontsize = 12, title = 'Monthly Messages Sent (All Members)')

	newPlot.set_xlabel("Time")
	newPlot.set_ylabel("Number of Messages")
	fig = newPlot.get_figure()
	plt.tight_layout()
	fig.savefig(output + "/Monthly Messages Sent for All Members.png")
	return

def dump_sender_activity(mg, output):

	users = mg.get_user_data()
	users.sort_values(by = 'num_messages', inplace = True, ascending = False)

	top_n = len(users.index) if len(users.index) < 10 else 10

	months = list(mg.dataset.groupby(pd.Grouper(freq = "M")).groups.keys())
	user_ids = [users.index.values[i] for i in range(top_n)]
	names = [users.loc[sender_id, 'latest_name'] for sender_id in user_ids]
	labels = [users.at[id, 'name'][-1] for id in user_ids]
	user_messages_monthly = pd.DataFrame(0, index = months, columns = names)

	for i in range(top_n):
	    sender_id = user_ids[i]
	    temp = mg.dataset[mg.dataset['sender_id'] == sender_id].groupby( pd.Grouper(freq = "M") ).apply(lambda x : len(x))
	    if temp.empty:
	        continue
	    name = users.loc[sender_id, 'latest_name']
	    user_messages_monthly[name] = temp
	user_messages_monthly.fillna(value = 0, inplace = True)

	newPlot = user_messages_monthly.plot.area(figsize = (10, 7.5), fontsize = 12, \
		title = "Monthly Messages Sent By User")
	newPlot.set_xlabel("Time")
	newPlot.set_ylabel("Number of Messages")
	fig = newPlot.get_figure()
	plt.tight_layout()
	fig.savefig(output + "/Monthly Messages Sent By Top Users")
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
