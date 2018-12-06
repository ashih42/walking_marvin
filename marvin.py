# (☞ﾟヮﾟ)☞  marvin.py

from exceptions import ParserException, MarvinException
from colorama import Fore, Back, Style
import sys

from marvin_manager import MarvinManager

def exit_with_usage_message():
	print('usage: ' + Fore.RED + 'python3' + Fore.BLUE + ' marvin.py ' + Fore.RESET)
	print('\t --help (-h)')
	print('\t --train (-t)')
	print('\t --walk (-w)')
	print('\t --episodes (-e) n_episodes \t (must be a positive integer, default = 10)')
	print('\t --t_max (-m) t_max \t\t (must be a positive integer, default = 200)')
	print('\t --seed (-z) seed \t\t (must be a positive integer)')
	print('\t --load (-l) file')
	print('\t --save (-s) file')
	print('\t --bipedal (-b) \t\t (run BipedalWalker-v2 instead)')
	sys.exit(0)

# must be a positive integer
def parse_number(expr):
	try:
		value = int(expr)
		if value <= 0:
			exit_with_usage_message()	
		return value
	except ValueError as e:
		exit_with_usage_message()

def parse_options():
	options = {
		'help': False,
		'train': False,
		'walk': False,
		'episodes': 10,
		't_max': 200,
		'seed': None,
		'load': None,
		'save': None,
		'env': 'Marvin-v0'
	}
	if len(sys.argv) == 1:
		options['train'] = True
		options['walk'] = True
	else:
		i = 0
		while i < len(sys.argv):
			flag = sys.argv[i]
			if flag == '--help' or flag == '-h':
				options['help'] = True
			elif flag == '--train' or flag == '-t':
				options['train'] = True
			elif flag == '--walk' or flag == '-w':
				options['walk'] = True
			elif flag == '--episodes' or flag == '-e':
				if i + 1 >= len(sys.argv):
					exit_with_usage_message()
				options['episodes'] = parse_number(sys.argv[i + 1])
				i += 1
			elif flag == '--t_max' or flag == '-m':
				if i + 1 >= len(sys.argv):
					exit_with_usage_message()
				options['t_max'] = parse_number(sys.argv[i + 1])
				i += 1
			elif flag == '--seed' or flag == '-z':
				if i + 1 >= len(sys.argv):
					exit_with_usage_message()
				options['seed'] = parse_number(sys.argv[i + 1])
				i += 1
			elif flag == '--load' or flag == '-l':
				if i + 1 >= len(sys.argv):
					exit_with_usage_message()
				options['load'] = sys.argv[i + 1]
				i += 1
			elif flag == '--save' or flag == '-s':
				if i + 1 >= len(sys.argv):
					exit_with_usage_message()
				options['save'] = sys.argv[i + 1]
				i += 1
			elif flag == '--bipedal' or flag == '-b':
				options['env'] = 'BipedalWalker-v2'
			i += 1
	return options

def main():
	options = parse_options()
	if options['help']:
		exit_with_usage_message()

	try:
		marvin_manager = MarvinManager(options['env'])
		if options['seed'] is not None:
			marvin_manager.set_seed(options['seed'])

		if options['load'] is not None:
			marvin_manager.load(options['load'])
		if options['save'] is not None:
			marvin_manager.set_filename(options['save'])

		if options['train']:
			marvin_manager.train(
				n_episodes=options['episodes'],
				t_max=options['t_max'],
				also_walk=options['walk'])
		elif options['walk']:
			marvin_manager.walk(n_episodes=options['episodes'])

		if options['save'] is not None:
			marvin_manager.save(options['save'])

	except IOError as e:
		print(Style.BRIGHT + Fore.RED + 'I/O Error: ' + Style.RESET_ALL + Fore.RESET + str(e))
	except ParserException as e:
		print(Style.BRIGHT + Fore.RED + 'ParserException: ' + Style.RESET_ALL + Fore.RESET + str(e))
	except MarvinException as e:
		print(Style.BRIGHT + Fore.RED + 'MarvinException: ' + Style.RESET_ALL + Fore.RESET + str(e))

if __name__ == '__main__':
	main()
