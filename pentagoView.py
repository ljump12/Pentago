# pentagoView.py    version 1.0     2-apr-2009      Bill Manaris
#
# This is the View (user interafce) component of the Pentago game.
#
# See http://en.wikipedia.org/wiki/Pentago
#
# NOTES: 
#
#  1) On Mac OS X, graphics22.py (actually, tkinter) has a problem with 
#     capturing coordinates of mouse clicks properly.  The "fix" is to 
#     click on the title bar and reposition the window once (when first displayed).
#     Then mouse clicking should work fine.
#
#  2) graphics22.py does not seem to handle .GIF image transparency properly.
#     That's a pity, because the turn-arrows overlay image looks best semi-transparent.
#

from graphics22 import *
#from graphics import *

class PentagoView():
    """Defines the view (user interafce) component of the Pentago game.
    
         
    """

    def __init__(self):
    
    # ideally, we should get the images from the client
    #def __init__(self, boardImage, blackBallImage, whiteBallImage, turnImage):

        #######################################################################
        # Load various images
        
        self._boardImage  = "board.gif"         # the board image
        self._boardWidth  = 410                 # hardcode dimensions for now...
        self._boardHeight = 400

        # ideally... 
        # find out the width and height of the board image
        #self._boardImage = boardImage  
        #boardPixels = Pixmap(boardImage)
        #self._boardWidth = boardPixels.getWidth()
        #self._boardHeight = boardPixels.getHeight()
        #print self._boardWidth, self._boardHeight
        
        self._blackBallImage = "black.gif"      # the black ball image
        self._ballWidth      = 50               # hardcode for now...
        self._ballHeight     = self._ballWidth  # it's a square
        
        self._whiteBallImage = "white.gif"      # the white ball image

        self._turnImage  = "turnArrows1.gif"    # the turn arrows image
        self._turnWidth  = self._boardWidth     # overlay on board (same dimensions)
        self._turnHeight = self._boardHeight

        #######################################################################
        # Define various image coordinates (in pixels)
        #
        # Coordinates below are hardcoded because the board image does not have perfect geometry.
        #
        # NOTE: If a board image with perfect geometry is available, it is most desirable
        #        (elegent, conceptually efficient) to create coordinates relative to the image size.
        #

        #######################################################################
        # Board holes

        # define hole centers
                       # 1st row
        self._holes = (Point(48, 40), Point(110, 40), Point(172, 40),
                       Point(233, 40), Point(296, 40), Point(359, 40), 
                      
                       # 2nd row
                       Point(48, 102), Point(110, 102), Point(172, 102),  
                       Point(233, 102), Point(296, 102), Point(359, 102),

                       # 3rd row
                       Point(48, 164), Point(110, 164), Point(172, 164),  
                       Point(233, 164), Point(296, 164), Point(359, 164), 
                      
                       # 4th row
                       Point(46, 226), Point(110, 226), Point(174, 226),  
                       Point(234, 226), Point(297, 226), Point(361, 226), 
 
                       # 5th row
                       Point(46, 291), Point(110, 291), Point(174, 291),  
                       Point(234, 291), Point(297, 291), Point(361, 291),

                       # 6th row
                       Point(46, 354), Point(110, 354), Point(174, 354),  
                       Point(234, 354), Point(297, 354), Point(361, 354))

        # how far can user click from the hole center and still be inside hole
        self._holeRadius = 25    # i.e., ballWidth / 2 

        #######################################################################
        # Turn arrows
        #
        # board quadrants are numbered as follows:
        #
        #               +---+---+
        #               | 0 | 1 |
        #               +---+---+
        #               | 2 | 3 |
        #               +---+---+

        # turn-arrows are superimposed over certain holes, so define their centers
        self._q0_turnCW  = self._holes[2]   # clockwise
        self._q0_turnCCW = self._holes[12]  # counter-clockwise
        self._q1_turnCW  = self._holes[17]  # clockwise
        self._q1_turnCCW = self._holes[3]   # counter-clockwise
        self._q2_turnCW  = self._holes[18]  # clockwise
        self._q2_turnCCW = self._holes[32]  # counter-clockwise
        self._q3_turnCW  = self._holes[33]  # clockwise
        self._q3_turnCCW = self._holes[23]  # counter-clockwise

        # put turn centers in a list (for efficiency)
        self._turnArrows = (self._q0_turnCW, self._q0_turnCCW,
                            self._q1_turnCW, self._q1_turnCCW,
                            self._q2_turnCW, self._q2_turnCCW,
                            self._q3_turnCW, self._q3_turnCCW)

        # how far can user click from the turn-arrow center and still be over it
        self._turnRadius = self._holeRadius 
      
        #######################################################################
        # Finally, create and display the window
        self._win = GraphWin("Pentago", self._boardWidth, self._boardHeight)

        # load and display board image (at center of window)
        self._board = Image(Point(self._win.width/2, self._win.height/2), self._boardImage)
        self._board.draw(self._win)

        # put created balls in a list (36 empty slots for now)
        self._balls = [None]*len(self._holes)


    def getMove(self):
        """Returns which hole was clicked (0..35) or -1 (if click was elsewhere). """

        # initialize
        whichHoleClicked = -1    # assume error click

        # get coordinates of mouse click
        click = self._win.getMouse()
        
        # find which hole was clicked (if any)
        for i in range(len(self._holes)):
            
            # within area of this hole?
            holeCenter = self._holes[i]
            if abs(click.getX() - holeCenter.getX()) <= self._holeRadius and \
               abs(click.getY() - holeCenter.getY()) <= self._holeRadius :
                
               whichHoleClicked = i   # yes!
        
        return whichHoleClicked


    def getTurn(self):
        """Returns which quadrant and turn direction was clicked, 
           e.g., (0, "counter-clockwise"), or (2, "clockwise").
           
           If user click is outside of available turn arrows, 
           it returns (0, "").
        """
        
        # display turn-arrows (superimpose on board)
        turnArrows = Image(Point(self._win.width/2, self._win.height/2), self._turnImage)
        turnArrows.draw(self._win)

        # initialize
        quadrant = -1    # assume error click
        direction = ""
        whichQuadrantArrowClicked = -1

        # get coordinates of mouse click
        click = self._win.getMouse()

        # find which turn-arrow was clicked (if any)
        for i in range(len(self._turnArrows)):
            
            # within area of turn-arrow (hole)?
            turnCenter = self._turnArrows[i]
            if abs(click.getX() - turnCenter.getX()) <= self._turnRadius and \
               abs(click.getY() - turnCenter.getY()) <= self._turnRadius :
               
               whichQuadrantArrowClicked = turnCenter

        # now, we know which arrow was selected (if any),
        # so convert to external representation
        if whichQuadrantArrowClicked == self._q0_turnCW:
            quadrant = 0
            direction = "clockwise"
        elif whichQuadrantArrowClicked == self._q0_turnCCW:
            quadrant = 0
            direction = "counter-clockwise"
        elif whichQuadrantArrowClicked == self._q1_turnCW:
            quadrant = 1
            direction = "clockwise"
        elif whichQuadrantArrowClicked == self._q1_turnCCW:
            quadrant = 1
            direction = "counter-clockwise"
        elif whichQuadrantArrowClicked == self._q2_turnCW:
            quadrant = 2
            direction = "clockwise"
        elif whichQuadrantArrowClicked == self._q2_turnCCW:
            quadrant = 2
            direction = "counter-clockwise"
        elif whichQuadrantArrowClicked == self._q3_turnCW:
            quadrant = 3
            direction = "clockwise"
        elif whichQuadrantArrowClicked == self._q3_turnCCW:
            quadrant = 3
            direction = "counter-clockwise"
        
        # done, so hide turn-arrows
        turnArrows.undraw()
        turnArrows = None

        return (quadrant, direction)


    def displayBoard(self, board):
        """Displays a board configuration.

           board -- a list of 36 strings, each either "", "w", or "b"
                    (where "" is empty, "w" is white ball, and "b" is black ball)
        """

        # update view based on board configuration
        for hole in range(len(self._holes)):
            if board[hole] == "":
                self.clearHole(hole)
            elif board[hole] == "w":
                self.putWhiteBall(hole) 
            elif board[hole] == "b":
                self.putBlackBall(hole)
            else:
                raise ValueError, "Unexpected value '" + board[hole] + "' in input parameter."                


    def putWhiteBall(self, hole):
        """Puts a white ball in a board hole (0..35). """

        if hole not in range(0,36):
            raise IndexError, "Hole " + str(hole) + " is outside of the board."

        # create white ball image at proper hole coordinates
        if not self._balls[hole]:
            ball = Image(self._holes[hole], self._whiteBallImage)
            ball.draw(self._win)
        else:
            raise ValueError, "Hole " + str(hole) + " has a ball already."

        # remember this ball image
        self._balls[hole] = ball


    def putBlackBall(self, hole):
        """Puts a black ball in a board hole (0..35). """

        if hole not in range(0,36):
            raise IndexError, "Hole " + str(hole) + " is outside of the board."

        # create white ball image at proper hole coordinates
        if not self._balls[hole]:
            ball = Image(self._holes[hole], self._blackBallImage)
            ball.draw(self._win)
        else:
            raise ValueError, "Hole " + str(hole) + " has a ball already."

        # remember this ball image
        self._balls[hole] = ball


    def clearHole(self, hole):
        """Empties a hole (0..35). OK to clear an empty hole."""

        if hole not in range(0,36):
            raise IndexError, "Hole " + str(hole) + " is outside of the board."

        # remove ball (if any) from hole
        if self._balls[hole]:
            self._balls[hole].undraw()
            self._balls[hole] = None
 

if __name__ == "__main__":

    view = PentagoView()  # create the board UI

    # NOTE: The following code demos available view methods:
    
    # create an arbitrary board configuration
    board = [""]*36               # initialize an empty board configuration
    for i in range(36):
        if i%2 == 0:    # even hole?
            board[i]   = "w"     # put white ball in it
        elif i%3 == 0:  # an odd multiple of 3?
            board[i] = "b"       # put black ball in it
        else:
            pass                 # leave empty
            #board[i] = ""
    # now, board is ready to display

    # update UI given board configuration
    #view.displayBoard(board)

    # get some input...
    for i in range(15):

        # one move consists of placing a ball and turning a quadrant, so...
        # WHITE: get a hole and place a white ball
        hole = view.getMove()
        view.putWhiteBall(hole)
        print "white ball in hole", hole
        # get which quadrant to turn and in which direction
        quadrant, direction = view.getTurn()
        print "quadrant =", quadrant, ", direction=", direction

        # another move...
        # BLACK: get a hole and place a black ball
        hole = view.getMove()
        view.putBlackBall(hole)
        print "black ball in hole", hole
        # get which quadrant to turn and in which direction
        quadrant, direction = view.getTurn()
        print "quadrant =", quadrant, ", direction=", direction

        # get a hole and clear it
        hole = view.getMove()
        view.clearHole(hole)
        print "cleared hole", hole

##        # NOTE: The following should be used for debugging only!
##        # get board coordinates clicked
##        click = view._win.getMouse()
##        print click.getX(), click.getY()
        
    #win.close()