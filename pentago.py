from minimax import *
from pentagoView import *
from game import *
import time

class pentago():

    def __init__(self):
		self.state = state()
		
    def run_game(self):
        new_game = Game()
        our_state = self.state

        view = PentagoView()  # create the board UI
        print "Initial Board:"
        while True:
            view.displayBoard(our_state.board)
            hole = view.getMove()
            view.putWhiteBall(hole)
            print "white ball in hole", hole
            # get which quadrant to turn and in which direction
            quadrant, direction = view.getTurn()
            user_move = move(direction, quadrant, hole)
            our_state = new_game.make_move(new_game.to_move(our_state), user_move, our_state) 
            view.displayBoard(our_state.board)
            
            print new_game.to_move(our_state)+"'s turn: Searching..."
            new_game.time_stamp_begin = time.time()
            next_move = minimax_decision(our_state,new_game)
            print "Made Move:",next_move
            our_state = new_game.make_move(new_game.to_move(our_state), next_move, our_state) 
            new_game.display(our_state)          
            

class state():
	def __init__(self):
		self.board 		= [" "]*36
		self.to_move 	= "W"
	
if __name__ == "__main__":
    pentago_game = pentago()
    pentago_game.run_game()
