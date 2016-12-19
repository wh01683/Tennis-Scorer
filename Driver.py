#!/usr/bin/python

import sys
import re

def main():
	print sys.argv
	results = Validation.validate_args(sys.argv[1:])
	print results
        if len(results) > 0 and results.keys()[0] in Validation.error_code_to_description.keys():
		Validation.print_errors(results)
	else:
		session = Session(results)
		session.run_session()
		
class Session():
	def __init__(self, args):
		self.p1name = args.get('--p1name', 'Player1')
		self.p2name = args.get('--p2name', 'Player2')
		self.p1score = args.get('--p1score', 'Love')
		self.p2score = args.get('--p2score', 'Love')
		self.p1wins = args.get('--p1wins', 0)
		self.p2wins = args.get('--p2wins', 0)
		self.mode = args.get('--mode', 'set')
		
		self.p1numscore = Validation.word_to_point[self.p1score]
		self.p2numscore = Validation.word_to_point[self.p2score]
	
	def run_session(self):
		print 'Starting session.'
		self.print_intro()
		while True:
			user_input = raw_input('> ')
		  	print 'User input: ', user_input	
			if re.compile('^(.+) scores!$').match(user_input) != None:
				player_name = re.compile('^(.+) scores!$').match(user_input).group(1)
				self.increment_score(player_name)
				score_result = self.decide_game_score()
				print score_result
				if re.compile('^.*wins.*$').match(score_result) != None : sys.exit(0)

			elif re.compile('^exit$').match(user_input) != None:
				sys.exit(0)
			
			else: print 'Invalid Input'

	def set_p1numscore(self, new_p1numscore):
		self.p1numscore = new_p1numscore
	
	def set_p2numscore(self, new_p2numscore):
		self.p2numscore = new_p2numscore
	
	def decide_game_score(self):
		if self.p1numscore < 4 and self.p2numscore < 4:
			return self.p1score + ' - ' + self.p2score
		elif self.p1numscore == self.p2numscore:
			return 'Deuce!'
		elif 2 > (self.p1numscore - self.p2numscore) > 0:
			return self.p1name + ' advantage!'
		elif 2 > (self.p2numscore - self.p1numscore) > 0:
			return self.p2name + ' advantage!'
		elif (self.p1numscore - self.p2numscore) > 1:
			return self.p1name + ' wins the game'
		elif (self.p2numscore - self.p1numscore) > 1:
			return self.p2name + ' wins the game'
	
	def print_intro(self):
		
		leader = self.p1name if self.p1numscore > self.p2numscore else self.p2name
		set_leader = self.p1name if self.p1wins > self.p2wins else self.p2name

		print '========================== GAME CONDITIONS ========================='
		print self.p1name + ' is playing against ' + self.p2name + '.'
		
		if self.p1numscore != self.p2numscore:
			print 'The score is ' + str(self.p1score) + ' to ' + str(self.p2score) + ' with ' + leader + ' in the lead.'
		else: 
			print 'Both players are tied with a score of ' + str(self.p1score) + ' to ' + str(self.p2score) + '.'
		if self.mode == 'set': 
			print self.p1name + ' has ' + str(self.p1wins) + ' wins and ' + self.p2name + ' has ' + str(self.p2wins) + ' wins.'
		
		print 'The mode is \'' + self.mode + '\''
		print 'Type \'exit\' to exit the program.'
		print '===================================================================='		
		
		
	def increment_score(self, player_name):
		if player_name == self.p1name:
			self.set_p1numscore(self.p1numscore + 1)
			self.p1score = Validation.point_to_word[self.p1numscore] if self.p1numscore < 4 else 'Forty'
		elif player_name == self.p2name:
			self.set_p2numscore(self.p2numscore + 1)
			self.p2score = Validation.point_to_word[self.p2numscore] if self.p2numscore < 4	else 'Forty'
		else:
			print player_name, ' is an invalid player name!'
	
		
				
class Validation():

	score_regex = re.compile('^Love$|^Fifteen$|^Thirty$|^Forty$|^Advantage$')
	initial_wins_regex = re.compile('^[0-6]$')
	
	arg_to_regex = {'--p1name' : re.compile('.+'),
			'--p2name' : re.compile('.+'),
			'--p1score' : score_regex,
			'--p2score' : score_regex,
			'--p1wins' : initial_wins_regex,
			'--p2wins' : initial_wins_regex,
			'--mode' : re.compile('^game$|^set$')}

	arg_to_description = {'--p1name' : 'Player 1\'s name', 
				'--p2name' : 'Player 2\'s name',
				'--p1score' : 'The initial score for player 1 - (one of Love, Fifteen, Thirty, Forty, Advantage - default is love.',
				'--p2score' : 'The initial score for player 2 - (one of Love, Fifteen, Thirty, Forty, Advantage - default is love.',
				'--p1wins' : 'The initial # of wins for player 1 - (an integer between 0 and 6 - default is 0)',
				'--p2wins' : 'The initial # of wins for player 2 - (an integer between 0 and 6 - default is 0)',
				'--mode' : 'Whether to run the program in game mode or set mode (one of game or set - default is set'}
	
	point_to_word = {0 : 'Love',
			1 : 'Fifteen',
			2 : 'Thirty',
			3 : 'Forty'}
	
	word_to_point = {'Love' : 0,
			'Fifteen' : 1,
			'Thirty' : 2,
			'Forty' : 3}	
	
	error_code_to_description = {'e1' : 'Invalid number of arguments',
					'e2' : 'Invalid argument',
					'e3' : 'Both players cannot have an Advantage at the same time.',
					'e4' : 'Invalid argument syntax.'}
	
	@staticmethod
	def print_errors(error_codes):
		not_all_valid = False
		for error in error_codes:
			print Validation.error_code_to_description[error]
			if error == 'e2' or error == 'e4':
                                for offending_arg in error_codes[error]:
					if offending_arg not in Validation.arg_to_description.keys():
						not_all_valid = True
				if not_all_valid and 'e2' in error_codes.keys() and 'e4' in error_codes.keys():
					break
				else:
					for offending_arg in error_codes[error]: Validation.print_invalid_arg(offending_arg)
		if not_all_valid: Validation.print_usage_description()

	@staticmethod
	def validate_args(dirty_args):
		invalid_syntax = []
		invalid_args = []
		errors = {}
		clean_args = {}
		
		if len(dirty_args) % 2 != 0:
			errors['e1'] = ''
			return errors
		else:
			for i in range(0, len(dirty_args), 2):
				# Checking if syntax is valid
				if dirty_args[i] not in Validation.arg_to_regex.keys():
					invalid_syntax.append(dirty_args[i])
				else:
					if Validation.arg_to_regex[dirty_args[i]].match(dirty_args[i+1]) == None:
						invalid_args.append(dirty_args[i])
					else:
						# Arguments should be deemed clean at this point
						clean_args = Util.convert_args_to_dict(dirty_args)
		if len(invalid_syntax) > 0:
			errors['e4'] = invalid_syntax

		if len(invalid_args) > 0:
			errors['e2'] = invalid_args		
		
		if len(clean_args) > 0 and '--p1score' in clean_args.keys() and '--p2score' in clean_args.keys() and clean_args['--p1score'] == 'Advantage'and clean_args['--p2score'] == 'Advantage':
			errors['e3'] = ''

		if len(errors) > 0:
			return errors
		else:
			return clean_args
		
	@staticmethod
	def print_invalid_arg(arg_name):
		print 'Invalid input for ', arg_name, '.\nUsage description: ', Validation.arg_to_description[arg_name]

	@staticmethod
	def print_usage_description():
		for arg in Validation.arg_to_description:
			print arg, '\t', Validation.arg_to_description[arg]
	@staticmethod
	def print_blank_args(arg_name):
		print 'No args given for ', arg_name

class Util():
	
	@staticmethod
	def convert_args_to_dict(args):
		scrubbed_args = {}
		for i in range(0,len(args),2):
			scrubbed_args[args[i]] = args[i+1]
				
		return scrubbed_args
	
if __name__ == "__main__": main()
