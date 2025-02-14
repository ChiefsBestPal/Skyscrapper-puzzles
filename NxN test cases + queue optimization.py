from tkinter.constants import SOLID
import numpy as np
import itertools as it
import typing
import re
import operator as op
import itertools as it
from collections import Counter
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
clues = ( 0, 3, 0, 5, 3, 4, 
          0, 0, 0, 0, 0, 1,
          0, 3, 0, 3, 2, 3,
          3, 2, 0, 3, 1, 0)
          
expected = (( 5, 2, 6, 1, 4, 3 ), 
            ( 6, 4, 3, 2, 5, 1 ), 
            ( 3, 1, 5, 4, 6, 2 ), 
            ( 2, 6, 1, 5, 3, 4 ), 
            ( 4, 3, 2, 6, 1, 5 ), 
            ( 1, 5, 4, 3, 2, 6 ))
""" ON GITHUB, CHIEFSBESTPAL """ 
def solve_puzzle(clues):
    import time
    import sys,os
    
    def display(state) -> '__main__':
        #global state
        os.system( 'cls' )
        def chunk(N,arr):
            
            for i in range(0, len(arr), N):  
                yield arr[i:i + N]

        x = list((chunk(state.N,state.board)))

        def nestedRecursiveCastString(item):

            if isinstance(item, list):
                return [nestedRecursiveCastString(x) for x in item if x]
            else:
                return str(item).center(20)

        z = nestedRecursiveCastString(x)
        delete = "\b" * 20
        print("\n{0}{1}\n{0}{2}\n{0}{3}\n{0}{4}\n{0}{5}\n{0}{6}\n".format(delete,\
            z[0],z[1],z[2],z[3],z[4],z[5])) 
        
        #for i in z:
        #   print(i)
        #print('')
        sys.stdout.flush()
        time.sleep(0.001)
    #! CONSTRAINT PROPAGATION NOTES FROM SUDOKU SOLVER:
    #* I. If cell has 1 possible value, then remove this value from the cell's peers 
    # --> If A1 is assigned value, 20 peers lose that possible value
    #* II. corrolary following I.: If unit has 1 only possibility (out of9) for a value, place value there
    # --> If all cells apart A2 in row (unit) lack a certain possible value, A2 is assigned that certain value 
    #* III. Complimentary of I. and II. will change peers of peers, use: Notation, update possibilities and backtracking
    class helper():
        pass


    def getCellIxFromRowIx(rowIx,N) -> helper():
        """retuns an array of all cells
        indices from row index 
        >>> getCellIxFromRowIx(2,4)
            iter(8,9,10,11)
        """
        firstCellOfRow = rowIx * N
        return [cellIx for cellIx in range(firstCellOfRow, firstCellOfRow + N)]

    def getCellIxFromColIx(colIx,N) -> helper():
        """returns an array of all cells 
        indices from col index
        >>> getCellIxFromColIx(0,4)
            iter(0,4,8,12)
        """
        firstCellOfCol = colIx
        return [firstCellOfCol + i * N for i in range(N)]

    def getCellIxFromClueIx(clueIx,N) -> helper():
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
                    err
                    #// print(err)
                    pass
            
            return cell
        one = 0
        twothree = 0
        zero = 0
        for clueIx,clue in enumerate(state.clues):
            cellIndices = getCellIxFromClueIx(clueIx,state.N)
            #// print(cellIndices)
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
        #// print('Zero: ', zero, '  One: ', one, '  TwoThree: ', twothree,end='\n'*3)
        return STATE



    state = performEdgeClueIntialization()

    #*Constraint propagation; elimination of newly impossible values\
    """
    #TODO Add CP queue (FIFO?) for optimization for very long and random puzzles
    #TODO https://www.ibm.com/support/knowledgecenter/SSSA5P_20.1.0/ilog.odms.cplex.help/refcppcplex/html/propagation.html
    """
    def getCrossIxFromCell(state,cellIx) -> helper():
        """Cool to returns all cells in the row and column of the given cell
        >>> getCrossIxFromCell(...state, 2) and state.N=4
                [0,1,3,6,10,14]"""
        rowIx,colIx = divmod(cellIx,state.N) #row jump by Nix(truediv), col by 1ix (mod)=> shown in other helper functions!

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


    def propagateConstraints(state=State(clues)):

        STATE = state

        for cellIx,cell in enumerate(STATE.board):

            STATE = propagateFromSolvedCell(STATE,cellIx)
        
        return STATE #Would yield be more efficient?


    state = propagateConstraints(state)

    #*Process of Elimination: Solve value if it is not present in other cells in its row and/or column
    """  """

    def getRowIxFromCellIx(state,cellIx) -> helper():
        """ invert input and output of getCellIxFromRowIx
            similar logic as cross helper function """
        rowIx = cellIx // state.N
        return sorted({cellIx} ^ set(getCellIxFromRowIx(rowIx,state.N)))
        

    def getColIxFromCellIx(state,cellIx) -> helper():
        """ invert input and output of getCellIxFromColIx
            similar logic as cross helper function """
        colIx = cellIx % state.N
        return sorted({cellIx} ^ set(getCellIxFromColIx(colIx,state.N)))

    #TODO Missing: state.queue, which right now is a list of newly-resolved cell indices from which constraints need to be propagated

    def poeCellSearch(state,modifiedCellIx,deletedValue):
        """ Consider value no longer a constraints for a certain cell 
            1. Get all row ix that have this value as poss 
                and store them in filtered array
            2. if and only if len(arr) == 1, then newcellIx/arr[0] == value
            3. repeat for columns 
            (might need optimization for larger grids) """
        
        if deletedValue not in state.board[modifiedCellIx]:#! This is because there is no queue yet so we iterate everything to check
            return state

        rowIndices,colIndices = map(op.methodcaller(r'__call__',state,modifiedCellIx),\
                                    [getRowIxFromCellIx,getColIxFromCellIx]) #callable *arg

        unpackedIndicesForCellIx = [*rowIndices,*colIndices]

        filteredArr = lambda cellIndices : list(filter(lambda ix: deletedValue in state.board[ix], cellIndices))# >>> see docstring

        R,C = map(filteredArr,[rowIndices,colIndices])#filtered row and col
        newCellWithValueIx = list(R+C) if not (bool(R) and bool(C)) else [] #*abs(~(len(R) & len(C))) If col OR row have 0 poss, ternary returns true/arr[0] >>> see docstring

        if len(filteredArr(unpackedIndicesForCellIx)) <= 1: #0: works for col and row 1: works for one, still have to place it (constraint) 
            state.board[modifiedCellIx] = {deletedValue}
            try:
                state.board[newCellWithValueIx[0]] = state.board[newCellWithValueIx[0]] - {deletedValue}
            except IndexError:
                #//print('\t0 poss in col and 0 poss in row')
                pass

        else:#same structure as if
            #//print('Cells with value in row: ' + str(R) + '  in col: ' + str(C))
            #//print(str(newCellWithValueIx) + ' <-- new Cell with valueix')
            if newCellWithValueIx: #row OR col has 0 cell with possible value;
                state.board[modifiedCellIx] = {deletedValue}
                for cellIx in newCellWithValueIx:
                    #// print('i')
                    state.board[cellIx] = state.board[cellIx] - {deletedValue} 

        RES = state
        return RES

    display(state)
    #TODO print('SHOULD WORK FOR NxN up to here')

    #* clue elimination using the sequence filtration technique


    def possibleSequencesForClueUnit(state,clueIx) -> helper(): #TODO Look up optimization... O(n) This has greatest impact on performance for larger puzzles
        """ from clue, all combinations with unique elements respecting order
            of cells/sets """
        cellIndices = getCellIxFromClueIx(clueIx,state.N)
        arr = []
        for cellIx in cellIndices:
            arr.append(state.board[cellIx])

        return list( {el for el in it.product(*arr) if len(set(el)) == state.N})
        


    def filterValidSequences(clue,*sequences):
        """ for all possible sequence of row or col (unit) of clue,
            filter the ones that respect the clue
            >>> SEQ = possibleSequencesForUnit(state,3)
            >>> list(validSequences(2,*SEQ))
                [(3, 1, 2, 4), (3, 2, 1, 4)] (example) """
        for sequence in sequences:
            visible,max = 0,0
            for value in sequence:
                if value > max:
                    visible += 1
                    max = value

            if visible == clue:
                yield sequence


    def clueElimination(state,clueIx,validSequences):
        """ replace constraints lists with validSequences 
        for clue and itsaffected cells  """
        STATE = state
    
        def seqToConstraintList(validSequences) -> helper():
            """ convert list of working sequences
            into list of sets used in state.board
            >>> seqToConstraintList(...,...,[(3, 1, 2, 4), (3, 2, 1, 4)]) 
                [{3},{1,2},{2,1},{4}] """
            return [set(possValue) for possValue in zip(*validSequences)]

        cluePossibilities = seqToConstraintList(validSequences)
        cellIndicesOfClue =  getCellIxFromClueIx(clueIx,state.N)
        
        for cellIx,cluePoss in zip(cellIndicesOfClue,cluePossibilities):
            # assign new sequence value to state.board at clue ix
            STATE.board[cellIx] = cluePoss
        return STATE


    def elimClue(clues,state):
        for clueIx,clue in enumerate(clues):
            if clue != 0:
                sequences = possibleSequencesForClueUnit(state,clueIx)
                validSequences = list(filterValidSequences(clue,*sequences))
                state = clueElimination(state,clueIx,validSequences)
        return state

    def isSolved(state) -> State():
        for set in state.board:
            if len(set) != 1:
                return False
        return True

    def countPossibility(state):
        """ DEBUGGING """
        solution = list(map(lambda set: next(iter(set)),list(filter(lambda x: len(x) == 1,state.board))))
        for num in range(1,state.N+1):
            if solution.count(num) == state.N:
                solution = list(filter((num).__ne__, solution))
        
        return solution#placed values
        #!return max(dict.fromkeys(solution),key= solution.count)
    import random
    def countNums(state):
        arr = list(filter(lambda x: len(x) != 1,state.board))
        arr = list(map(list,arr))
        flat = [item for sublist in arr for item in sublist]
        return Counter(flat)


    state = elimClue(clues,state)
    state = propagateConstraints(state)

    #// ---------------------------------------------------------------------------------------------
    #print('\n\n\n...') #TODO FIND CONSTRAINT LIST ORDER.....)
    previous = int()
    """ need to see if mutations happened to least uncertain value, 0 mutation, then check second least uncertain
        when mutation, apply deletedvalue to PoE"""
    count = 0
    while not isSolved(state):
        #//print('Iteration number: ' + str(count))
        count += 1
        counterOfListConstraints = countNums(state)
        #//print(counterOfListConstraints.keys())
        #//print(counterOfListConstraints)
        display(state)


        try:
            leastUncertainDeletedValue = list(counterOfListConstraints.keys())[-1] #! Make so that if other values are equal to l[-1], then choose the one that ...
            leastUncertainDelValuesList = {leastUncertainDeletedValue}

            for k,v in counterOfListConstraints.items():
                if v == counterOfListConstraints[leastUncertainDeletedValue]:
                    #//print("AN EQUALLY CERTAIN COUNT APPEARED!")
                    leastUncertainDelValuesList.add(k)
                if v < counterOfListConstraints[leastUncertainDeletedValue]:
                    leastUncertainDeletedValue = k
                    #//print("MORE CERTAIN COUNT APPEARED!")
                    break

            leastUncertainDeletedValue = max(leastUncertainDelValuesList) #!arbitrary #!choose a value over another if its countPossibility() is better (more placed values)
            #//print(leastUncertainDeletedValue,' BRUH')
            previous = leastUncertainDeletedValue

        except IndexError as emptyConstraintLists:
            #//print('All constraint lists are empty')
            break
        for ix in range(state.N**2):
            state = poeCellSearch(state,ix,leastUncertainDeletedValue)
        display(state)
        #//print('')
        state = elimClue(clues,state)
        display(state)
        #//print('just eliminated clues')
        while state != propagateConstraints(state):
            #//print(r'removed conflicting possibilities with current placed values')
            state = propagateConstraints(state)
        while state != elimClue(clues,state): #! Heavy on time complexity...
            #//print(r'eliminate current/newly possible values based on clues given')
            state = elimClue(clues,state)


        display(state)
        if count >= 100: #TODO __DEBUG__ : GO TO NEXT: NOW ITS STUCK ON FIVE BECAUSE IT HASNT SOLVED ALL N POSSIBLE CELLS FOR 5 ! GO TO SECOND LEAST UNCERTAIN AND SO ON
            break
        
    def chunkTup(N,arr): 
	    for i in range(0, len(arr), N):  
		    yield tuple(arr[i:i + N])
    solution = list(map(lambda set: next(iter(set)),state.board))

    return tuple(chunkTup(state.N,solution))    

for line in solve_puzzle(clues):
    print(line)

