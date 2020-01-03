import json

from groups import get_all_groups
from messages import get_messages, save_html

def main():

	# Load the configuration variables
	configs = json.load(open('config.json', 'r'))
	TOKEN = configs['token']
	PATH = configs['path']

	groups = get_all_groups(TOKEN, outputFile = PATH + "/groups.json")
	print(groups)
	get_messages()
	save_html()

if __name__ == '__main__':
	main()
