import json
from http import client
import os
import requests
import pandas as pd
from datetime import datetime, timedelta, date


# Save to a messages.json
def get_messages(token, groupme_id, outputFile = None, verbose = False):

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

# Count the number of attached images
def count_img(x):
    if len(x) == 0: return 0
    count = 0
    for i in range(len(x)):
        if 'image' in x[i]['type']:
            count += 1
    return count

# Get the URLs of attached images
def get_img_urls(x):
    urls = []
    for i in range(len(x)):
        if x[i]['type'] == 'image':
            urls.append(x[i]['url'])
    return urls

# Determine whether a location is attached to the message
def has_loc(x):
    if len(x) == 0: return False
    for i in range(len(x)):
        if x[i]['type'] == 'location':
            return True
    return False

# Get the location info if a location is attached
def get_loc(x):
    if not has_loc(x):
        return

    for i in range(len(x)):
        if x[i]['type'] == 'location':
            return {'lat' : x[i]['lat'],
                    'lng' : x[i]['lng'],
                    'name' : x[i]['name']}
    return


def print_img_urls(x):
    data = ""
    for i in range(len(x)):
        data += "<a>" + x[i] + "</a>" + "<img>" + x[i] + "</img>"
    return data


def remove_nan(x):
    if x == True:
        return ""

# Save dataframe to html
def output_to_html(dataset, fileName, images = True):

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

	table_html = dataset.to_html( justify = 'left', render_links = True)
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

	file = open(fileName, 'w')
	file.truncate(0)
	file.write(html_string.format(table = table_html))
	file.close()
	return

# Save individual html files for each user
def save_html(messages, outputPath):

	# Load the configuration variables
	configs = json.load(open('config.json', 'r'))
	fullPath = configs['path'] + '/' + configs['groupme-id'] + '/members'

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

	# Load the saved JSON data to the notebook
	print(len(messages), "messages loaded")

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
	output_to_html(select_columns(dataset.sort_values(by = 'created_at')), outputPath + '/messages.html', images = True)
	output_to_html(select_columns(dataset.sort_values(by = 'likes', ascending = False).head(250)), outputPath + '/most_liked_messages.html', images = True)
	output_to_html(select_columns(dataset[ dataset['imgs'] > 0 ].sort_values(by = 'likes', ascending = False).head(150)), outputPath + '/most_liked_images.html', images = True)

	users = dataset.sort_values(by = 'created_at', ascending = True).groupby(['sender_id'])['name'].unique().apply(list).to_frame()
	user_id_list = users.index.values

	for id in user_id_list:
	    user_name = users.at[id, 'name'][-1].replace('/', '_')
	    output_to_html(select_columns(dataset[ dataset['sender_id'] == id ].sort_values(by = 'likes', ascending = False)), outputPath + "/" + user_name + '_messages.html', images = True)

if __name__ == '__main__':
	get_messages()
	save_html()
