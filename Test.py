from Driver import * 
import unittest

class TestDriverUtil(unittest.TestCase):

	valid_commands = ['--p1name', '--p2name', '--p1score', '--p2score', 'p1wins', '--p2wins', '--mode']

	def test_convert_args_to_dict(self):
		self.assertEqual(Util.convert_args_to_dict(['', '']), {'' : ''})
		self.assertEqual(Util.convert_args_to_dict(['--p1name', 'Rob', '--p2name', 'Player2']), {'--p1name' : 'Rob', '--p2name' : 'Player2'})
		self.assertEqual(Util.convert_args_to_dict(['--p1name', 'Rob', '--p2name', 'John', '--p2score', 'Thirty', '--p1wins', '3', '--p2wins', '2', '--mode', 'set']), {'--p1name':'Rob', '--p2name' : 'John', '--p2score':'Thirty', '--p1wins':'3', '--p2wins': '2', '--mode': 'set'})
	
	def test_arg_validation(self):
		good_names = ['Rob', 'John', 'Will', 'Lindsey', 'asdnjlksajncdlkjnsac', '432DSADSAsds$#$', 'R']
		bad_names = ['']
		
		bad_scores = ['love', 'thirty', 'fifteen', 'advantage', 'FifteeN', 'LovE', 'AdvantagE', 'Lov', 'Thirt', 'Fiftee', 'Advantag', 'Fort', 'forty', 'FortY']
		good_scores = ['Love', 'Thirty', 'Fifteen', 'Forty']
		
		bad_wins = ['-1', '7', '10', '11', '120384', '-10']
		good_wins = ['0', '1', '2', '3', '4', '5', '6']
		
		bad_modes = ['sete', 'Set', 'se', 'gam', 'Game', 'gamE', 'seT']
		good_modes = ['set', 'game']
		
		for good_name in good_names:
			self.assertEqual(Validation.arg_to_regex['--p1name'].match(good_name) != None, True)
			self.assertEqual(Validation.arg_to_regex['--p2name'].match(good_name) != None, True)

		for bad_name in bad_names:
			self.assertEqual(Validation.arg_to_regex['--p1name'].match(bad_name) == None, True)
                        self.assertEqual(Validation.arg_to_regex['--p2name'].match(bad_name) == None, True)
		
		for good_score in good_scores:
                        self.assertEqual(Validation.arg_to_regex['--p1score'].match(good_score) != None, True)
                        self.assertEqual(Validation.arg_to_regex['--p2score'].match(good_score) != None, True)

                for bad_score in bad_scores:
                        self.assertEqual(Validation.arg_to_regex['--p1score'].match(bad_score) == None, True)
                        self.assertEqual(Validation.arg_to_regex['--p2score'].match(bad_score) == None, True)
		
		for good_win in good_wins:
                        self.assertEqual(Validation.arg_to_regex['--p1wins'].match(good_win) != None, True)
                        self.assertEqual(Validation.arg_to_regex['--p2wins'].match(good_win) != None, True)

                for bad_win in bad_wins:
                        self.assertEqual(Validation.arg_to_regex['--p1wins'].match(bad_win) == None, True)
                        self.assertEqual(Validation.arg_to_regex['--p2wins'].match(bad_win) == None, True)

		for bad_mode in bad_modes:
			self.assertEqual(Validation.arg_to_regex['--mode'].match(bad_mode) == None, True)
		
		for good_mode in good_modes:
			self.assertEqual(Validation.arg_to_regex['--mode'].match(good_mode) != None, True)

	def test_validate_args(self):
		"""
		Since args to dict conversion and arg pattern matching are tested elsewhere, these tests focus on verifying
		the program's ability to distinguish between sets of invalid args and sets of valid args, as well as its ability
		to decide which arguments are causing issues.
		"""
		# e1 = Invalid number of args
		# e2 = Args with invalid format (i.e. 7 wins or Set instead of set)
		# e3 = Both players have advantage
		# e4 = Invalid syntax (i.e. -p1wins instead of --p1wins)
		
		badsyntax1 = ['--p1name', 'Rob', '-p2name', 'John']
		badsyntax2 = ['-mode', 'set']
		badsyntax3 = ['mode', 'set']
		badsyntax4 = ['p1wins', '6', '--p2wins', '2']
		badsyntax5 = ['--p1name', 'Rob', '-p1wins', '2', '-mode', 'set', '--p2name', 'Joe']
		goodsyntax1 = ['--p1name', 'Rob', '--p2name', 'John', '--p2score', 'Thirty', '--p1wins', '3', '--p2wins', '2', '--mode', 'set']
		
		
		self.assertEqual(Validation.validate_args(badsyntax1)['e4'], ['-p2name'])
		self.assertEqual(Validation.validate_args(badsyntax2)['e4'], ['-mode'])
		self.assertEqual(Validation.validate_args(badsyntax3)['e4'], ['mode'])
		self.assertEqual(Validation.validate_args(badsyntax4)['e4'], ['p1wins'])
		self.assertEqual(Validation.validate_args(badsyntax5)['e4'], ['-p1wins', '-mode'])
		self.assertEqual(Validation.validate_args(goodsyntax1), {'--p1name':'Rob', '--p2name' : 'John', '--p2score':'Thirty', '--p1wins':'3', '--p2wins': '2', '--mode': 'set'})
		
	 	badargs1 = ['--p1name', 'Rob', '--p1score', 'thirty', '--p2score', 'Forty', '--mode', 'game']
		badargs2 = ['--p1wins', '-1', '--p1name', 'Kyle', '--p2wins', '0', '--mode', 'gam']
		badargs3 = ['--p1wins', '7', '--p1name', 'Billy Bob']
		badargs4 = ['--p2wins', '--p1name']

		self.assertEqual(Validation.validate_args(badargs1)['e2'], ['--p1score'])
		self.assertEqual(Validation.validate_args(badargs2)['e2'], ['--p1wins', '--mode'])
		self.assertEqual(Validation.validate_args(badargs3)['e2'], ['--p1wins'])
		self.assertEqual(Validation.validate_args(badargs4)['e2'], ['--p2wins'])
		
		self.assertEqual('e1' in Validation.validate_args([]).keys(), False)
		self.assertEqual('e1' in Validation.validate_args(['--p1score']), True)
		self.assertEqual('e1' in Validation.validate_args(['--p1name', 'Julie', '--p1score']), True)
		
		
		# Testing multiple error type detection
		allbad1 = ['-p1wins', '5', '--p2wins', '9', '--p1name', 'Rob', '--mod', 'game']
		
		self.assertEqual(Validation.validate_args(allbad1), {'e4': ['-p1wins', '--mod'], 'e2': ['--p2wins']})
		
		# Testing advantage mis-match
		self.assertEqual('e3' in Validation.validate_args(['--p1score', 'Advantage', '--p1name', 'Rob', '--p2score', 'Advantage']), True)
		
	def test_session(self):
		
		# New session has only default values
		session = Session({})
		
		# Testing game scoring decision making
		self.assertEqual(session.decide_game_score(), 'Love - Love') 
		session.increment_score('Player1')
		self.assertEqual(session.decide_game_score(), 'Fifteen - Love')
                session.increment_score('Player1')
		self.assertEqual(session.decide_game_score(), 'Thirty - Love')
                session.increment_score('Player2')
		self.assertEqual(session.decide_game_score(), 'Thirty - Fifteen')
                session.increment_score('Player2')
		self.assertEqual(session.decide_game_score(), 'Thirty - Thirty')
		session.increment_score('Player2')
                self.assertEqual(session.decide_game_score(), 'Thirty - Forty')
		session.increment_score('Player1')
                self.assertEqual(session.decide_game_score(), 'Forty - Forty')
		session.increment_score('Player2')
                self.assertEqual(session.decide_game_score(), 'Player2 advantage!')
		session.increment_score('Player1')
                self.assertEqual(session.decide_game_score(), 'Deuce!')
		session.increment_score('Player1')
                self.assertEqual(session.decide_game_score(), 'Player1 advantage!')
		session.increment_score('Player2')
                self.assertEqual(session.decide_game_score(), 'Deuce!')
		session.increment_score('Player2')
                self.assertEqual(session.decide_game_score(), 'Player2 advantage!')
		session.increment_score('Player2')
                self.assertEqual(session.decide_game_score(), 'Player2 wins the game')
		
if __name__ == '__main__':
	unittest.main()
	
