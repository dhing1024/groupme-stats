from groups import get_all_groups
from messages import get_messages, save_html

def main():
	get_all_groups()
	get_messages()
	save_html()

if __name__ == '__main__':
	main()
