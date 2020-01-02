

# Declare variables
token = '#####'
pageSize = 100
oldestID = -1

# Request parameters
server = 'api.groupme.com'
path = '/v3/groups/#######/messages'
connection = client.HTTPSConnection(server)

# Open output file
fileName = 'messages.json'
file = open(fileName, 'w')
file.truncate(0)

# Helper function for reading the id by index in the response
def getMessageIDbyIndex(messages, index):
    return messages[index]['id']

# Loop through pages of GroupMe messages using the GroupMe developer's API
data = []
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

# Write JSON data to local .json file
file.write(json.dumps(data))
file.close()
