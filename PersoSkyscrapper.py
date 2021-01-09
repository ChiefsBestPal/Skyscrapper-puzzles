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
def chunk(N,arr):
	for i in range(0, len(arr), N):  
		yield arr[i:i + N]




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
def edgeDistancesForRowNCol(N):
    """Distances cells have from given clue in board;
    to be zip* iterated with cellIx to performEdge clue Initialization"""
    arr = [i for i in range(0, N // 2)]
    if N % 2 == 0:
        return arr + arr[::-1]
    else:
        return arr + [N//2] + arr[::-1]

def performEdgeClueIntialization(state=State(clues)):
    """#If clue = N,  unit is from clue pos: 1,2,3,4,5     AND if clue 1:  unit starts with 5
    ##In general, this rule can be expressed as follows. On an N * N board, for clues c where 
    ##1 < c < N, where d is the distance from the edge counting from zero, we can cross off all
    ##values from N - c + 2 + d up to N, inclusive."""
    STATE = state.board
    def edgeConstraintCellWithClue(cell=set(),clue=int(),distance=0):
        # if not all([cell,clue,distance]):
        #     raise ValueError('Enter valid values for the three parameters')
        # """This might be inside another one later on
        # -> it describes the Edge constraint rule when propagating values"""

        minimum_value = state.N - clue + 2 + distance
        print('MINIMUM\t',minimum_value,clue)
        #print(cell,'\tCELL')
        for i in range(minimum_value,state.N + 1):
            try:
                cell.remove(i) #del cell[i]
            except KeyError as err:
                print('ERROR #000')
        
        return cell
    one = 0
    twothree = 0
    zero = 0
    for clueIx,clue in enumerate(clues):
        cellIndices = getCellIxFromClueIx(clueIx,state.N)
        print(cellIndices)
        edgeDistances = edgeDistancesForRowNCol(state.N)
        if 1 < clue < state.N:
            for edgeDistance,cellIx in zip(edgeDistances,cellIndices):
                cell = state.board[cellIx]
                cell = edgeConstraintCellWithClue(cell,clue,edgeDistance)

                twothree += 1
                print(cell,'\tCELL')
                print(cellIx, 'TWOTHREE')
                STATE[cellIx] = cell

        elif clue == 1:
            cell = state.board[cellIndices[0]]
            cell.clear()
            cell.add(state.N)

            one+= 1
            print(cell,'\tCELL')
            print(cellIndices[0],'ONE')
            STATE[cellIndices[0]] = cell
        elif clue == state.N:
            for edgeDistance,cellIx in zip(edgeDistances,cellIndices):
                cell = state.board[cellIx]
                cell.clear()
                cell.add(edgeDistance+1)

                STATE[cellIx] = cell
        else:
            
            zero+= 1
        print('\n\n\n')
        print(np.array(list(chunk(4,STATE))))
        print('\n\n\n')
    print('Zero: ', zero, '  One: ', one, '  TwoThree: ', twothree)
    return STATE

x = list(performEdgeClueIntialization())

print(x)
def SpecialPrint(x):
    y = [set() for _ in range(16)]
    y[0] = x[0]
    y[1] = x[1]
    y[2] = x[2]
    y[3] = x[3]
    y[4] = x[14]
    y[5] = x[7]

