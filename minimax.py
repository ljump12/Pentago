# Minimax Search (from AIMA textbook)
#file based on recursion on of functions

from utils import *

def minimax_decision(state, game):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states. [Fig. 6.4]"""

    player = game.to_move(state)

    def max_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
		#same as min value function except v=-infinity
        v = -infinity
        for (a, s) in game.successors(state):
            v = max(v, min_value(s))
        return v

    def min_value(state):
		#base case
        if game.terminal_test(state):
            return game.utility(state, player)
		#infinity is best that this can do
        v = infinity
		#return list of a,s
        for (a, s) in game.successors(state):
            v = min(v, max_value(s))
        return v

    # Body of minimax_decision starts here:
    action, state = argmax(game.successors(state),
                           lambda ((a, s)): min_value(s))
    return action
 