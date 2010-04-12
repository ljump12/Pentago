from copy import deepcopy
import time
from pentago import *

class Game:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement
    legal_moves, make_move, utility, and terminal_test. You may
    override display and successors or you can inherit their default
    methods. You will also need to set the self.initial instance variable
    to the initial state; this can be done in the constructor."""

    def __init__(self):
        self.time_stamp_begin = 0

    def legal_moves(self, state):
        "Return a list of the allowable moves at this point."
        all_moves = []
        for ball_location in range(36):
            for quadrant in range(4):
                all_moves.append(move("clockwise",quadrant,ball_location))
                all_moves.append(move("counter-clockwise",quadrant,ball_location))
                all_moves.append(move("None",quadrant,ball_location))
        
        legal_moves = []
        for poss_move in all_moves:
            if state.board[poss_move.ball_location] == " ":
                legal_moves.append(poss_move)
        
        return legal_moves
        
    def make_move(self, player, move, state):
        "Return the state that results from making a move from a state."
        state = self.__place_ball(player, move, state)
        state = self.__make_turn(move, state)
        
        state.to_move = opponent(state.to_move)	
        return state
            
    def __place_ball(self, player, move, state):
        state.board[move.ball_location] = player
        return state

    def __make_turn(self, move, state):
        #print move
        quadrant = [None,None,None,None]
        quadrant[0] = [0,1,2,6,7,8,12,13,14]
        quadrant[1] = [3,4,5,9,10,11,15,16,17]
        quadrant[2] = [18,19,20,24,25,26,30,31,32]
        quadrant[3] = [21,22,23,27,28,29,33,34,35]
        
        new_state = deepcopy(state)

        #print new_state.board
		
        ## Compute left rotation
        if move.turn_direction == "counter-clockwise":
            if move.turn_quadrant == 0:
                init_pos = 2
            elif move.turn_quadrant == 1:
                init_pos = 5
            elif move.turn_quadrant == 2:
                init_pos = 20
            else: init_pos = 23
                
            ## Computes new state for left rotation TODO:: COMMENT BETTER
            counter = 1
            pos = init_pos
            for value in quadrant[move.turn_quadrant]:
                new_state.board[value] = state.board[pos]
                pos += 6
                if counter % 3 == 0:
                    init_pos -= 1
                    pos = init_pos
                counter += 1
        
        if move.turn_direction == "clockwise":
            if move.turn_quadrant == 0:
                init_pos = 12
            elif move.turn_quadrant == 1:
                init_pos = 15
            elif move.turn_quadrant == 2:
                init_pos = 30
            else: init_pos = 33
                
            ## Computes new state for right rotation TODO:: COMMENT BETTER
            counter = 1
            pos = init_pos
            for value in quadrant[move.turn_quadrant]:
                new_state.board[value] = state.board[pos]
                pos -= 6
                if counter % 3 == 0:
                    init_pos += 1
                    pos = init_pos
                counter += 1

        return new_state

        
    def utility(self, state, player):
        "Return the value of this final state to player."
        ## First let's check the horizontal rows for the player, and get a score
        horiz_score = self.__horiz_points(state, player)

        ## Now let's check the vertical columns for the player, and get a score
        vert_score = self.__vert_points(state, player)

        ## Now we need to check the columns and rows for the opposite player.
        opp_horiz_score = self.__horiz_points(state, opponent(player))
        opp_vert_score  = self.__vert_points(state, opponent(player))

        ## Our total Utility is the players score, minus the opponents score.
        return (horiz_score - opp_horiz_score) + (vert_score - opp_vert_score)

    def __horiz_points(self, state, player):
        ## First let's check horizontal combinations.
        board = state.board
        total_horiz_points = 0
        for row in range(6):
            max_combination = 0
            combination = 0
            for col in range(6):
                if board[col+(6*row)] == player:
                    combination += 1
                else:
                    combination = 0
                if combination >= max_combination:
                    max_combination = combination

            if max_combination == 2:
                total_horiz_points += 1
            elif max_combination == 3:
                total_horiz_points += 2
            elif max_combination == 4:
                total_horiz_points += 4
            elif max_combination == 5:
                total_horiz_points += 1000000
        return total_horiz_points

    def __vert_points(self, state, player):
        ## First let's check vertical combinations.
        board = state.board
        total_vert_points = 0
        for col in range(6):
            max_combination = 0
            combination = 0
            for row in range(6):
                if board[(6*row)+col] == player:
                    combination += 1
                else:
                    combination = 0
                if combination >= max_combination:
                    max_combination = combination
            
            if max_combination == 2:
                total_vert_points += 1
            elif max_combination == 3:
                total_vert_points += 2
            elif max_combination == 4:
                total_vert_points += 4
            elif max_combination == 5:
                total_vert_points += 1000000
        return total_vert_points

    def terminal_test(self, state):
        "Return True if this is a final state for the game."
        #good place to implement the time cut off for pentago
        #to kill function if time runs out before legal moves run out

        if not self.legal_moves(state) or self.utility(state, self.to_move(state)) >= 10000 or time.time() - self.time_stamp_begin > 4:
            return True
        else:
            return False

    def to_move(self, state):
        "Return the player whose move it is in this state."
        return state.to_move

    def display(self, state):
        "Print or otherwise display the state."
        print ""
        for row in range(6):
            print state.board[0+(6*row)],state.board[1+(6*row)],state.board[2+(6*row)],"|",
            print state.board[3+(6*row)],state.board[4+(6*row)],state.board[5+(6*row)]
        #print state.board


    def successors(self, state):
        "Return a list of legal (move, state) pairs."
        return [(move, self.make_move(self.to_move(state), move, deepcopy(state)))
                for move in self.legal_moves(state)]

    def __repr__(self):
        return '<%s>' % self.__class__.__name__
        

        
class move:

    def __init__(self, turn_direction, turn_quadrant, ball_location):
        self.turn_quadrant  = turn_quadrant
        self.turn_direction = turn_direction
        self.ball_location  = ball_location
    
    def __str__(self):
        return "ball_pos="+str(self.ball_location)+",turn_direction="+self.turn_direction+",turn_quadrant="+str(self.turn_quadrant)

def opponent(player):
    if player == "W":
        return "B"
    else:
        return "W"

if __name__ == "__main__":
    new_game = Game()
    our_state = state()
    our_state.board[2] = "W" 
    our_state.board[5] = "B"
    our_state.board[11] = "B"
    our_state.board[17] = "B"
    our_state.board[23] = "B"
    our_state.board[16] = "B"
    
    new_game.display(our_state)
    new_game.utility(our_state, "W")
    
    moves = new_game.legal_moves(our_state)
    #print moves

    #print new_game.successors("W",our_state)

    #for move, state in new_game.successors("W",our_state):
    #    print move
    #    new_game.display(state)
    
    our_move = move("clockwise",0, 1)
    our_state = new_game.make_move("W",our_move,our_state)
    new_game.display(our_state)
    new_game.utility(our_state, "W")
    
    our_move = move("clockwise",0, 1)
    our_state = new_game.make_move("W",our_move,our_state)
    new_game.display(our_state)
    new_game.utility(our_state, "W")
    
    our_move = move("None",3, 6)
    our_state = new_game.make_move("W",our_move,our_state)
    new_game.display(our_state)
    new_game.utility(our_state, "W")

    our_move = move("None", 0, 18)
    our_state = new_game.make_move("W",our_move,our_state)
    new_game.display(our_state)
    new_game.utility(our_state, "W")

    max_utility = 0
    best_move = None
    for move,state in new_game.successors("W",our_state):
        if new_game.utility(state, "W") > max_utility:
            max_utility = new_game.utility(state,"W")
            print "Found new best move",move
            best_move = move

    our_state = new_game.make_move("W",best_move,our_state)
    new_game.display(our_state)
    print new_game.utility(our_state, "W")
