from minimax import *
from pentagoView import *
from game import *

class pentago():

    def __init__(self):
		self.state = state()
		
class state():
	def __init__(self):
		self.board 		= [" "]*36
		self.to_move 	= "W"
	