import json
import pandas as pd
from datetime import datetime, timedelta, date
import os


# Load the configuration variables
configs = json.load(open('config.json', 'r'))
fullPath = configs['path'] + '/' + configs['groupme-id'] + '/members'

now = datetime.now()
thirty_days = datetime.now() - timedelta(days = 30)
six_months = datetime.now() - timedelta(days = 180)
last_year = datetime.now() - timedelta(days = 365)
first_year = datetime(2017, 1, 1, 0, 0, 0, 0)

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
def output_to_html(dataset, fileName, images = False):

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

    if not os.path.exists(fullPath):
        os.makedirs(fullPath)

    file = open(fullPath + '/' + fileName, 'w')
    file.truncate(0)
    file.write(html_string.format(table = table_html))
    file.close()
    return

# Helper function for selecting the appropriate columns

def select_columns(df):
	columns = ['name', 'message', 'likes', 'liked_by', 'loc']
	df = df[columns]
	return df


# Load the saved JSON data to the notebook
messageFile = configs['path'] + '/' + configs['groupme-id'] + '/messages.json'
messages = json.load(open(messageFile, 'r'))
print(len(messages), " messages loaded")


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




# Get Unique sender IDs
users = dataset.sort_values(by = 'created_at', ascending = True).groupby(['sender_id'])['name'].unique().apply(list).to_frame()
user_id_list = users.index.values

users['orig_name'] = users['name'].apply(lambda x : x[0])
users['num_names'] = users['name'].apply(len)
users.sort_values(by = 'num_names', inplace = True, ascending = False)

users['msg_ln_mean'] = dataset.groupby(['sender_id'])['msg_ln'].mean()
users['msg_ln_stddev'] = dataset.groupby(['sender_id'])['msg_ln'].std()
users['num_messages'] = dataset.groupby(['sender_id']).apply(len)
users['num_messages_past6months'] = dataset[ dataset.index > six_months ].groupby(['sender_id']).apply(len)
users['num_messages_firstyear'] = dataset[ dataset.index < first_year ].groupby(['sender_id']).apply(len)

for i in range(len(user_id_list)):
    users.loc[user_id_list[i], 'likes_given_past6months'] = dataset[ dataset.index > six_months ]['liked_by'].apply(lambda x : user_id_list[i] in x).sum()

for i in range(len(user_id_list)):
    users.loc[user_id_list[i], 'likes_given_total'] = dataset['liked_by'].apply(lambda x : user_id_list[i] in x).sum()

users.sort_values(by = 'num_messages', inplace = True, ascending = False)


# Outputs
output_to_html(select_columns(dataset.sort_values(by = 'created_at')), 'messages.html', images = True)
output_to_html(select_columns(dataset.sort_values(by = 'likes', ascending = False).head(250)), 'most_liked_messages.html', images = True)
output_to_html(select_columns(dataset[ dataset['imgs'] > 0 ].sort_values(by = 'likes', ascending = False).head(150)), 'most_liked_images.html', images = True)

users = dataset.sort_values(by = 'created_at', ascending = True).groupby(['sender_id'])['name'].unique().apply(list).to_frame()
user_id_list = users.index.values


for id in user_id_list:
    user_name = users.at[id, 'name'][-1].replace('/', '_')
    output_to_html(select_columns(dataset[ dataset['sender_id'] == id ].sort_values(by = 'likes', ascending = False)), user_name + '_messages.html', images = True)
