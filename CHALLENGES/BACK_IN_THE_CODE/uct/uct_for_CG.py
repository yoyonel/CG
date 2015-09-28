from math import *
import random
import sys
import math


class BTTCState:
    """ A state of the game of Back to The Code, i.e. the game board.
        The board is a 2D array where 0 = empty (.), 1 = player 1 (X), 2 = player 2 (O).
    """

    def __init__(self, sz_l=35, sz_h=20):
        self.playerJustMoved = 1  # At the root pretend the player just moved is p2 - p1 has the first move
        self.board = []  # 
        self.size = (sz_l, sz_h)
        assert sz_l == int(sz_l) and sz_h == int(sz_h)  # size must be integral
        for y in range(sz_h):
            self.board.append([-1] * sz_l)
        self.pos = [[0, 0]]*2
        self.distance = [0]*2

    def Clone(self):
        """ Create a deep clone of this game state.
        """
        st = BTTCState()
        st.playerJustMoved = self.playerJustMoved
        st.board = [self.board[i][:] for i in range(self.size[1])]
        st.size = self.size
        st.pos = self.pos
        return st

    def DoMove(self, move):
        """ Update a state by carrying out the given move.
            Must update playerToMove.
        """
        (x, y) = (move[0], move[1])
        # on affecte la board avec le deplacement
        self.board[y][x] = self.playerJustMoved if self.board[y][x] == -1 else self.board[y][x]
        # on deplace le joueur sur la board
        self.pos[self.playerJustMoved] = list(move)
        # on affecte la distance de deplacement
        self.distance[self.playerJustMoved] += 1
        self.playerJustMoved = 1 - self.playerJustMoved
        
    def DoMoveForReal(self, move):
        """ Update a state by carrying out the given move.
            Must update playerToMove.
        """
        self.DoMove(move)
        self.distance[self.playerJustMoved] = 0

    def GetMoves(self):
        """ Get all possible moves from this state.
        """
        if self.distance[self.playerJustMoved] < 10:
            x, y = self.pos[self.playerJustMoved]
            return [
                (x+dx, y+dy) 
                for dy in range(-1, 2) 
                for dx in range(-1, 2) 
                if (abs(dx+dy) == 1) and self.IsOnBoard(x+dx, y+dy) and self.board[y+dy][x+dx] == -1
            ]
        else:
            return []

    def IsOnBoard(self, x, y):
        return 0 <= x < self.size[0] and 0 <= y < self.size[1]

    def GetResult(self, playerjm):
        """ Get the game result from the viewpoint of playerjm.
        """
        jmcount = len(
            [0
             for y in range(self.size[1])
             for x in range(self.size[0])
             if self.board[y][x] == playerjm]
        )
        notjmcount = len(
            [0
             for y in range(self.size[1])
             for x in range(self.size[0])
             if self.board[y][x] == -1]
             )
        if jmcount > notjmcount:
            return 1.0
        elif notjmcount > jmcount:
            return 0.0
        else:
            return 0.5  # draw

    def __repr__(self):
        pass

    def Update(self, board_from_cg, x, y):
        """

        :param board_from_cg:
        :return:
        """
        #self.board = board_from_cg
        self.board = [map(lambda x: -1 if x == '.' else int(x), row) for row in board_from_cg]
        self.pos[0] = [x, y]


class Node:
    """ A node in the game tree. Note wins is always from the viewpoint of playerJustMoved.
        Crashes if state not specified.
    """

    def __init__(self, move=None, parent=None, state=None):
        self.move = move  # the move that got us to this node - "None" for the root node
        self.parentNode = parent  # "None" for the root node
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.GetMoves()  # future child nodes
        self.playerJustMoved = state.playerJustMoved  # the only part of the state that the Node needs later

    def UCTSelectChild(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
        """
        s = sorted(self.childNodes, key=lambda c: c.wins / c.visits + sqrt(2 * log(self.visits) / c.visits))[-1]
        return s

    def AddChild(self, m, s):
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
        """
        n = Node(move=m, parent=self, state=s)
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n

    def Update(self, result):
        """ Update this node - one additional visit and result additional wins. result must be from the viewpoint of playerJustmoved.
        """
        self.visits += 1
        self.wins += result

    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/" + str(self.visits) + " U:" + str(
            self.untriedMoves) + "]"

    def TreeToString(self, indent):
        s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
            s += c.TreeToString(indent + 1)
        return s

    def IndentString(self, indent):
        s = "\n"
        for i in range(1, indent + 1):
            s += "| "
        return s

    def ChildrenToString(self):
        s = ""
        for c in self.childNodes:
            s += str(c) + "\n"
        return s


def UCT(rootstate, itermax, verbose=False):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
        Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""

    rootnode = Node(state=rootstate)

    for i in range(itermax):
        node = rootnode
        state = rootstate.Clone()

        # Select
        while node.untriedMoves == [] and node.childNodes != []:  # node is fully expanded and non-terminal
            node = node.UCTSelectChild()
            state.DoMove(node.move)

        # Expand
        if node.untriedMoves != []:  # if we can expand (i.e. state/node is non-terminal)
            m = random.choice(node.untriedMoves)
            state.DoMove(m)
            node = node.AddChild(m, state)  # add child and descend tree

        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while state.GetMoves() != []:  # while state is non-terminal
            state.DoMove(random.choice(state.GetMoves()))

        # Backpropagate
        while node != None:  # backpropagate from the expanded node and work back to the root node
            node.Update(state.GetResult(
                node.playerJustMoved))  # state is terminal. Update node with result from POV of node.playerJustMoved
            node = node.parentNode

    # Output some information about the tree - can be omitted
    """
    if (verbose):
        print >> sys.stderr, rootnode.TreeToString(0)
    else:
        print >> sys.stderr, rootnode.ChildrenToString()
    """
    return sorted(rootnode.childNodes, key=lambda c: c.visits)[-1].move  # return the move that was most visited


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

opponent_count = int(raw_input()) # Opponent count

state = BTTCState(35, 20)

board_cg = []

m = (17, 10)

# game loop
while 1:
    game_round = int(raw_input())
     # x: Your x position
     # y: Your y position
     # back_in_time_left: Remaining back in time
    x, y, back_in_time_left = [int(i) for i in raw_input().split()]
    for i in xrange(opponent_count):
         # opponent_x: X position of the opponent
         # opponent_y: Y position of the opponent
         # opponent_back_in_time_left: Remaining back in time of the opponent
        opponent_x, opponent_y, opponent_back_in_time_left = [int(j) for j in raw_input().split()]
    for i in xrange(20):
        line = raw_input() # One line of the map (-1 = free, '0' = you, otherwise the id of the opponent)
        #
        board_cg.append(line)

    state.Update(board_cg, x, y)
    
    if state.GetMoves():
        m = UCT(rootstate=state, itermax=50, verbose=False)
        #
        state.DoMoveForReal(m)
    
    #print >> sys.stderr, "state.GetMoves(): ", state.GetMoves()
    
    print m[0], ' ', m[1]
    
    # Write an action using print
    # To debug: print >> sys.stderr, "Debug messages..."

    # action: "x y" to move or "BACK rounds" to go back in time
    #print "17 10"


