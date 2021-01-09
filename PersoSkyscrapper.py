import numpy as np
import itertools as it
import typing
import re
clues = [
  0, 0, 1, 2,   
  0, 2, 0, 0,   
  0, 3, 0, 0, 
  0, 1, 0, 0 ]
sol = ( ( 2, 1, 4, 3 ), 
        ( 3, 4, 1, 2 ), 
        ( 4, 2, 3, 1 ), 
        ( 1, 3, 2, 4 ))

#! CONSTRAINT PROPAGATION NOTES FROM SUDOKU SOLVER:
#* I. If cell has 1 possible value, then remove this value from the cell's peers 
# --> If A1 is assigned value, 20 peers lose that possible value
#* II. corrolary following I.: If unit has 1 only possibility (out of9) for a value, place value there
# --> If all cells apart A2 in row (unit) lack a certain possible value, A2 is assigned that certain value 
#* III. Complimentary of I. and II. will change peers of peers, use: Notation, update possibilities and backtracking




def getCellIxFromRowIx(rowIx,N):
    """retuns an array of all cells
    indices from row index 
    >>> getCellIxFromRowIx(2,4)
        iter(8,9,10,11)
    """
    firstCellOfRow = rowIx * N
    return [cellIx for cellIx in range(firstCellOfRow, firstCellOfRow + N)]

def getCellIxFromColIx(colIx,N):
    """returns an array of all cells 
    indices from col index
    >>> getCellIxFromColIx(0,4)
        iter(0,4,8,12)
    """
    firstCellOfCol = colIx
    return [firstCellOfCol + i * N for i in range(N)]

def getCellIxFromClueIx(clueIx,N):
    """returns an array of all cells
    indices from value index (from leftupmost cell, 0 to 15 going clockwise)
    >>> warning: CellIx and ClueIx are different in their disposition !!!
    >>> getCellIxFromClueIx()
    """
    for i in range(1,N+1):#1 to 4, 4 edges
        relativePosClue = clueIx % N
        if clueIx < N*i:
            if i == 1:#top edge
                return getCellIxFromColIx(relativePosClue,N)
            elif i == 2:#right edge
                return getCellIxFromRowIx(relativePosClue, N)[::-1]
            elif i == 3:#bottom edge
                return getCellIxFromColIx(abs(relativePosClue - (N - 1)), N)[::-1] #relative position in relation to the down right corner...
            else: #left edge
                return getCellIxFromRowIx(abs(relativePosClue- (N - 1)), N) # '' '' to the down left corner


#! Current state of vars: general important variables in global() scope (->allow recursive local changes)

class State(object):
    def __init__(self,clues=list()):
        self.clues = clues
        N = len(self.clues)//4
        board = [set([j for j in range(1,N+1)]) for i in range(N**2)]
        self.N,self.board = N,board

    def __repr__(self): 
        return 'State({!r})->N and Board\r\n \
            Current state of vars: \
            general important variables in global() scope \
            (->allow recursive local changes)'.format(self.clues)


def solveSkyscraper(clues):
    state = State(clues)
    pass 
    #? [...]
    return state

#!state = State(clues)
#!assert bool(globals()['edgeConstraintCellWithClue'])


def performEdgeClueIntialization(state=State(clues)):
    """#If clue = N,  unit is from clue pos: 1,2,3,4,5     AND if clue 1:  unit starts with 5
    ##In general, this rule can be expressed as follows. On an N * N board, for clues c where 
    ##1 < c < N, where d is the distance from the edge counting from zero, we can cross off all
    ##values from N - c + 2 + d up to N, inclusive."""
    STATE = state
    def edgeConstraintCellWithClue(cell=set(),clue=int(),distance=0):
        # if not all([cell,clue,distance]):
        #     raise ValueError('Enter valid values for the three parameters')
        # """This might be inside another one later on
        # -> it describes the Edge constraint rule when propagating values"""

        minimum_value = state.N - clue + 2 + distance

        for i in range(minimum_value,state.N + 1):
            try:
                cell.remove(i) #del cell[i]
            except KeyError as err:
                print(err)
        
        return cell
    one = 0
    twothree = 0
    zero = 0
    for clueIx,clue in enumerate(state.clues):
        cellIndices = getCellIxFromClueIx(clueIx,state.N)
        print(cellIndices)
        if 1 < clue < state.N:
            for edgeDistance,cellIx in enumerate(cellIndices):
                cell = state.board[cellIx]
                cell = edgeConstraintCellWithClue(cell,clue,edgeDistance)

                twothree += 1


                STATE.board[cellIx] = cell

        elif clue == 1:
            cell = state.board[cellIndices[0]]
            cell.clear()
            cell.add(state.N)

            one+= 1

            STATE.board[cellIndices[0]] = cell
        elif clue == state.N:
            for edgeDistance,cellIx in enumerate(cellIndices): #!Instad of zip UPDATE 1.0
                cell = state.board[cellIx]
                cell.clear()
                cell.add(edgeDistance+1)

                STATE.board[cellIx] = cell
        else:
            
            zero+= 1
    print('Zero: ', zero, '  One: ', one, '  TwoThree: ', twothree,end='\n'*3)
    return STATE



state = performEdgeClueIntialization()

#*Constraint propagation; elimination of newly impossible values\
"""
#!Add CP queue (FIFO?) for optimization for very long and random puzzles
#!https://www.ibm.com/support/knowledgecenter/SSSA5P_20.1.0/ilog.odms.cplex.help/refcppcplex/html/propagation.html
"""
def propagateConstraints(state=State(clues)):

    STATE = state

    def getCrossIxFromCell(state,cellIx):
        """Cool to returns all cells in the row and column of the given cell
        >>> getCrossIxFromCell(...state, 2) and state.N=4
                [0,1,3,6,10,14]"""
        rowIx,colIx = divmod(cellIx,state.N) #row jump by Nix(truediv), col by 1ix (mod)

        peers = set(getCellIxFromRowIx(rowIx,state.N))\
            ^ (set(getCellIxFromColIx(colIx,state.N))) #Binary op as .symetric_difference()
        return list(peers)

    def propagateFromSolvedCell(initialState,cellIx): #?-> State():
        """ for input cell, if it is solved then eliminate all
        poss of the res value in the cell's row and col """
        cell = initialState.board[cellIx]
        solvedValueToEliminate =  next(iter(cell)) if len(cell) == 1 else None

        crossIndices = getCrossIxFromCell(initialState,cellIx)
        for crossIx in crossIndices:
            try:
                initialState.board[crossIx].remove(solvedValueToEliminate)
            except (KeyError,AttributeError):
                pass
            else:
                continue
        
        return initialState

    for cellIx,cell in enumerate(STATE.board):
        #print(STATE.board)
        STATE = propagateFromSolvedCell(STATE,cellIx)
    
    return STATE #Would yield be more efficient?

state = propagateConstraints(state)

if __name__ == '__main__':
    def chunk(N,arr):
        
	    for i in range(0, len(arr), N):  
		    yield arr[i:i + N]

    x = list((chunk(4,state.board)))

    def nestedRecursiveCastString(item):

        if isinstance(item, list):
            return [nestedRecursiveCastString(x) for x in item if x]
        else:
            return str(item).center(20)

    z = nestedRecursiveCastString(x)

    for i in z:
        print(i)