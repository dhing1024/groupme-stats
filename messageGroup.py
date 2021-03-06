import json
from http import client
import os
import requests
import pandas as pd
from datetime import datetime, timedelta, date

class MessageGroup(object):

	# Constructor class
	def __init__(self, name, dataset = pd.DataFrame()):
		self.name = name
		self.dataset = dataset
		self.likes_matrix = None
		self.user_data = None

	# PUBLIC METHODS

	@classmethod
	def from_groupme_id(cls, token, groupme_id, outputFile = None, verbose = False):
		json_data = cls.__get_messages(token, groupme_id, outputFile = outputFile, verbose = verbose)
		dataset = cls.__messages_to_pandas(cls, json_data)
		return cls(groupme_id, dataset)

	def to_html(self, fileName, images = True):

		html_string = '''
		<html>
			<head>
				<title>HTML Pandas Dataframe with CSS</title>
				<style>
					table {{
						font-size: 9pt;
						font-family: Arial;
						border-collapse: collapse;
						border: 1px solid silver;
						table-layout: fixed;
						width: 100%
					}}
					td, th {{
						word-wrap: break-word;
						padding: 5px;
					}}
					td:nth-child(1), th:nth-child(1) {{
						width:12.5%;
						text-align: center;
					}}
					td:nth-child(2), th:nth-child(2) {{
						width:12.5%;
						text-align: center;
					}}
					td:nth-child(3), th:nth-child(3) {{
						width:45%;
						text-align: left;
					}}
					td:nth-child(4), th:nth-child(4) {{
						width:5%;
						text-align: center;
					}}
					td:nth-child(5), th:nth-child(5) {{
						width:12.5%;
						text-align: center;
					}}
					td:nth-child(6), th:nth-child(6) {{
						width:10%;
						text-align: center;
					}}
					tr:nth-child(even) {{
						background: #E0E0E0;
					}}
					tr:hover {{
						background: silver;
					}}
				</style>
			</head>
			<link rel="stylesheet" type="text/css" href="table_style.css"/>
			<body>
				{table}
			</body>
		</html>.
		'''

		table_html = self.dataset[['name', 'message', 'likes', 'liked_by', 'loc']]
		table_html = table_html.to_html( justify = 'left', render_links = True)
		table_html = table_html.replace("\\n", "</br>")

		if images == True:
			table_html = table_html.replace("&lt;a&gt;", "<a href = \"")
			table_html = table_html.replace("&lt;/a&gt;", "\" target=\"_blank\">")
			table_html = table_html.replace("&lt;img&gt;", "</br></br><img src = \"")
			table_html = table_html.replace("&lt;/img&gt;", "\" width = \"55%\" ></a></br></br>")
		else:
			table_html = table_html.replace("&lt;a&gt;", "<a href = \"")
			table_html = table_html.replace("&lt;/a&gt;", "\" target=\"_blank\">")
			table_html = table_html.replace("&lt;img&gt;", "</br></br><img src = \"")
			table_html = table_html.replace("&lt;/img&gt;", "\" width = \"55%\" ></a></br></br>")

		html_string = html_string.format(table = table_html)
		file = open(fileName, 'w')
		file.truncate(0)
		file.write(html_string)
		file.close()
		return

	def users_to_html(self, fileName, sortby = 'num_messages', ascending = False):
		table_html = self.get_user_data()

		if table_html is None:
			return

		table_html = table_html.drop(labels = ['name', 'orig_name', 'num_names'], axis = 1)
		table_html = table_html.sort_values(by = sortby, ascending = ascending)
		table_html = table_html.to_html( justify = 'left', render_links = True)
		file = open(fileName, 'w')
		file.truncate(0)
		file.write(table_html)
		file.close()
		return

	def to_json(self, path = None):
		return self.dataset.to_json(path_or_buf = path, orient = 'records')

	def info(self):
		info = {}
		info['Name'] = self.name
		info['Earliest Message'] = self.dataset.iloc[0].name.isoformat()
		info['Number of Messages'] = len(self.dataset.index)
		info['Number of Unique Senders'] = self.dataset['sender_id'].nunique()
		info['Average Message Length'] = self.dataset['text'].apply(lambda x : len(x)).mean()
		info['Stdev Message Length'] = self.dataset['text'].apply(lambda x : len(x)).std()
		info['Latest Message'] = self.dataset.iloc[len(self.dataset.index) - 1]['text']
		info['Latest Message Sender'] = self.dataset.iloc[len(self.dataset.index) - 1]['name']
		return info

	def num_messages(self, sender_id = 'all'):
		if sender_id == 'all':
			return len(self.dataset.index)
		else:
			return len(self.dataset[self.dataset['sender_id'] == sender_id].index)

	def senders(self):
		return self.dataset['sender_id'].unique()

	def senders_names(self):
		return self.dataset['name'].unique()

	def get_name_from_id(self, id):
		messages = self.dataset[self.dataset['sender_id'] == id].sort_index(ascending = False)
		return messages.iloc[0]['name']

	def timesort(self, ascending = True):
		if ascending == True:
			return MessageGroup(self.name, self.dataset.sort_index(ascending = True))
		else:
			return MessageGroup(self.name, self.dataset.sort_index(ascending = False))

	def likesort(self, ascending = False):
		if ascending == False:
			return MessageGroup(self.name, self.dataset.sort_values('likes', ascending = False))
		else:
			return MessageGroup(self.name, self.dataset.sort_values('likes', ascending = True))

	def filter_timedate_range(self, start, end = datetime.now()):
		dataset = self.dataset
		dataset = dataset.sort_index(ascending=True)
		dataset = dataset.loc[dataset.index > start]
		dataset = dataset.loc[dataset.index < end]
		return MessageGroup(self.name, dataset)

	def filter_senders(self, user_id):
		return MessageGroup(self.name, self.dataset[self.dataset['sender_id'] == user_id])

	def liked_by(self, user_id):
		return MessageGroup(self.name, self.dataset[self.dataset['liked_by'].apply(lambda x : user_id in x)])

	def get_likes_matrix(self, normalize = True):
		if self.likes_matrix == None:
			self.__form_likes_matrix()

		if normalize == True:
			return self.likes_matrix

		userIDs = self.senders()
		numMess = pd.Series({id: self.num_messages(sender_id = id) for id in userIDs})
		likes_matrix = self.likes_matrix.multiply(numMess, axis = 0)
		return likes_matrix


	def get_user_data(self):
		if self.user_data is None:
			self.__form_user_data()
		return self.user_data

	def __add__(self, message_group_object):
		return MessageGroup(self.name + " " + message_group_object.name, pd.concat([self.dataset, message_group_object.dataset]))

	# PRIVATE METHODS

	def __get_messages(token, groupme_id, outputFile = None, verbose = False):

		# Request parameters
		server = 'api.groupme.com'
		path = '/v3/groups/' + groupme_id + '/messages'
		connection = client.HTTPSConnection(server)

		# Helper function for reading the id by index in the response
		def getMessageIDbyIndex(messages, index):
			return messages[index]['id']

		if verbose:
			print("Downloading GroupMe messages for GroupMe ID " + groupme_id)

		# Loop through pages of GroupMe messages using the GroupMe developer's API
		data = []
		oldestID = -1
		pageSize = 100
		while True:

			params = '?'+ 'token=' + token + '&limit=' + str(pageSize)
			if oldestID != -1:
				params += '&before_id=' + oldestID

			response = requests.get('https://' + server + path + params)
			if response.status_code != 200:
				break

			messages = response.json()['response']['messages']
			data.extend(messages)
			oldestID = getMessageIDbyIndex(messages,-1)

		if outputFile is not None:
			file = open(outputFile, 'w')
			file.truncate(0)
			file.write(json.dumps(data))
			file.close()
		return data

	def __messages_to_pandas(self, messages):

		# Load the configuration variables
		#configs = json.load(open('config.json', 'r'))
		#fullPath = configs['path'] + '/' + configs['groupme-id'] + '/members'

		now = datetime.now()
		thirty_days = datetime.now() - timedelta(days = 30)
		six_months = datetime.now() - timedelta(days = 180)
		last_year = datetime.now() - timedelta(days = 365)
		first_year = datetime(2017, 1, 1, 0, 0, 0, 0)

		# Helper function for selecting the appropriate columns
		def select_columns(df):
			columns = ['name', 'message', 'likes', 'liked_by', 'loc']
			df = df[columns]
			return df

		# Read the messages into a pandas dataframe, setting the index as the unique message id
		df = pd.read_json(json.dumps(messages) )

		df['timestamp_utc'] = df['created_at']
		df.set_index('timestamp_utc', inplace = True)
		df.rename(columns = {"favorited_by" : "liked_by"}, inplace = True)

		# Generate new columns using the helper functions
		df['likes'] = df['liked_by'].apply(lambda x : len(x))
		df['imgs'] = df['attachments'].apply(lambda x : self.__count_img(x))
		df['img_urls'] = df['attachments'].apply(lambda x : self.__get_img_urls(x))
		df['has_loc'] = df['attachments'].apply(lambda x : self.__has_loc(x))
		df['loc'] = df['attachments'].apply(lambda x : self.__get_loc(x))

		df.loc[df['text'].isnull(), 'text'] = ""
		df['message'] = df['text'] + df['img_urls'].apply(lambda x : self.__print_img_urls(x) )
		df['msg_ln'] = df['text'].apply(lambda x : len(x))
		return df

	def __count_img(x):
	    if len(x) == 0: return 0
	    count = 0
	    for i in range(len(x)):
	        if 'image' in x[i]['type']:
	            count += 1
	    return count

	def __get_img_urls(x):
	    urls = []
	    for i in range(len(x)):
	        if x[i]['type'] == 'image':
	            urls.append(x[i]['url'])
	    return urls

	def __has_loc(x):
	    if len(x) == 0: return False
	    for i in range(len(x)):
	        if x[i]['type'] == 'location':
	            return True
	    return False

	def __get_loc(x):
	    #if not has_loc(x):
	    #    return
	    if len(x) == 0:
	        return
	    for i in range(len(x)):
	        if x[i]['type'] == 'location':
	            return {'lat' : x[i]['lat'],
	                    'lng' : x[i]['lng'],
	                    'name' : x[i]['name']}
	    return

	def __print_img_urls(x):
	    data = ""
	    for i in range(len(x)):
	        data += "<a>" + x[i] + "</a>" + "<img>" + x[i] + "</img>"
	    return data

	def __form_likes_matrix(self):
		userIDs = self.senders()
		likes_matrix = pd.DataFrame(index = userIDs)
		likes_matrix.index.name = 'sender_id'
		numMess = pd.Series({id: self.num_messages(sender_id = id) for id in userIDs})

		for id in userIDs:
			likes_matrix[id] = likes_matrix.index.map(lambda x : len(self.dataset[(self.dataset['sender_id'] == x) & (self.dataset['liked_by'].apply(lambda y : id in y))].index))
		likes_matrix = likes_matrix.divide(numMess, axis = 0)
		self.likes_matrix = likes_matrix

	def __form_user_data(self):

		if self.num_messages() == 0:
			return None

		now = datetime.now()
		six_months = now - timedelta(days = 180)
		now = datetime.now()
		thirty_days = datetime.now() - timedelta(days = 30)
		six_months = datetime.now() - timedelta(days = 180)
		last_year = datetime.now() - timedelta(days = 365)
		first_year = self.dataset.iloc[0].name + timedelta(days = 365)

		# Get Unique sender IDs
		users = self.dataset.sort_values(by = 'created_at', ascending = True).groupby(['sender_id'])['name'].unique().apply(list).to_frame()
		user_id_list = users.index.values

		users['orig_name'] = users['name'].apply(lambda x : x[0])
		users['latest_name'] = users['name'].apply(lambda x : x[-1])
		users['num_names'] = users['name'].apply(len)
		users.sort_values(by = 'num_names', inplace = True, ascending = False)

		users['msg_ln_mean'] = self.dataset.groupby(['sender_id'])['msg_ln'].mean()
		users['msg_ln_stddev'] = self.dataset.groupby(['sender_id'])['msg_ln'].std()
		users['num_messages'] = self.dataset.groupby(['sender_id']).apply(len)
		users['num_messages_past6months'] = self.dataset[ self.dataset.index > six_months ].groupby(['sender_id']).apply(len) if len(self.dataset[self.dataset.index > six_months].index) > 0 else 0
		users['num_messages_firstyear'] = self.dataset[ self.dataset.index < first_year ].groupby(['sender_id']).apply(len)	if len(self.dataset[self.dataset.index < first_year].index) > 0 else 0
		users['tot_likes'] = self.dataset[['likes', 'sender_id']].groupby(['sender_id']).apply(sum)['likes']
		for i in range(len(user_id_list)):
		    users.loc[user_id_list[i], 'likes_given_past6months'] = self.dataset[ self.dataset.index > six_months ]['liked_by'].apply(lambda x : user_id_list[i] in x).sum()

		for i in range(len(user_id_list)):
		    users.loc[user_id_list[i], 'likes_given_total'] = self.dataset['liked_by'].apply(lambda x : user_id_list[i] in x).sum()

		self.user_data = users.sort_values(by = 'num_messages', ascending = False)
		return

	# Save
	def save_html(messages, outputPath):

		# Load the configuration variables
		#configs = json.load(open('config.json', 'r'))
		#fullPath = configs['path'] + '/' + configs['groupme-id'] + '/members'

		now = datetime.now()
		thirty_days = datetime.now() - timedelta(days = 30)
		six_months = datetime.now() - timedelta(days = 180)
		last_year = datetime.now() - timedelta(days = 365)
		first_year = datetime(2017, 1, 1, 0, 0, 0, 0)

		# Helper function for selecting the appropriate columns
		def select_columns(df):
			columns = ['name', 'message', 'likes', 'liked_by', 'loc']
			df = df[columns]
			return df

		# Read the messages into a pandas dataframe, setting the index as the unique message id
		df = pd.read_json(json.dumps(messages) )

		df['timestamp_utc'] = df['created_at']
		df.set_index('timestamp_utc', inplace = True)
		df.rename(columns = {"favorited_by" : "liked_by"}, inplace = True)

		# Generate new columns using the helper functions
		df['likes'] = df['liked_by'].apply(lambda x : len(x))
		df['imgs'] = df['attachments'].apply(lambda x : count_img(x))
		df['img_urls'] = df['attachments'].apply(lambda x : get_img_urls(x))
		df['has_loc'] = df['attachments'].apply(lambda x : has_loc(x))
		df['loc'] = df['attachments'].apply(lambda x : get_loc(x))

		df.loc[df['text'].isnull(), 'text'] = ""
		df['message'] = df['text'] + df['img_urls'].apply(lambda x : print_img_urls(x) )
		df['msg_ln'] = df['text'].apply(lambda x : len(x))
		dataset = df

		# Outputs
		dataset_to_html(select_columns(dataset.sort_values(by = 'created_at')), outputPath + '/messages.html', images = True)
		dataset_to_html(select_columns(dataset.sort_values(by = 'likes', ascending = False).head(250)), outputPath + '/most_liked_messages.html', images = True)
		dataset_to_html(select_columns(dataset[ dataset['imgs'] > 0 ].sort_values(by = 'likes', ascending = False).head(150)), outputPath + '/most_liked_images.html', images = True)

		users = dataset.sort_values(by = 'created_at', ascending = True).groupby(['sender_id'])['name'].unique().apply(list).to_frame()
		user_id_list = users.index.values

		for id in user_id_list:
		    user_name = users.at[id, 'name'][-1].replace('/', '_')
		    dataset_to_html(select_columns(dataset[ dataset['sender_id'] == id ].sort_values(by = 'likes', ascending = False)), outputPath + "/" + user_name + '_messages.html', images = True)
