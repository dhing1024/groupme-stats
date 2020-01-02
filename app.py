from groups import get_all_groups
from messages import get_messages, save_html

def main():

	# Load the configuration variables
	configs = json.load(open('config.json', 'r'))
	token = configs['token']

	groups = get_all_groups(token)
	print(groups)
	get_messages()
	save_html()

if __name__ == '__main__':
	main()
