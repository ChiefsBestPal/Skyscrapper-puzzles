#bruh
import numpy as np
def chunks(arr, n):
    for i in range(0, len(arr), n):
        yield arr[i: i+n]

Indices = {0 : (15,0) , #?Indices of clues (clue VALUES) associated with appropriate index of, outcome (outcome KEYS) #! 0 always first; if not codes detech Nones as 0
            1 : (None,1) , 
            2 : (None,2) , #!order in tuple is: tup[0] -> row value ; tup[1] -> col value [el for el in range(15) if el%4 == ix%4]
            3 : (4,3) , 
            4 : (14,None) ,
            7 : (5,None) , 
            8 : (13,None) ,
            11: (6,None) ,
            12: (12,11) ,
            13: (None,10) ,
            14: (None,9) , 
            15: (7,8) }

inv_Indices = {value:key for key, value in Indices.items()}
#?inv_Indices = dict(zip(inv_Indices, map(tuple, inv_Indices.values())))
print(inv_Indices)
#! Pseudo Bisection search possible ?            
def solve_puzzle(clues):
    global Indices
    outcome = [0,0,0,0,
               0,0,0,0,
               0,0,0,0,
               0,0,0,0]
    for ix,clue in enumerate(clues):
        if clue == 1:
             #the key of the original list is outcome_ix; invert key search here
            for clues_ix in Indices.values():
                if ix in clues_ix:
                    outcome[inv_Indices[clues_ix]] = 4
    outcome = np.array(list(chunks(outcome,4)))
    for ix,clue in enumerate(clues):
        if clue == 4:
            for clues_ix in Indices.values():
                if ix in clues_ix:
                    key = inv_Indices[clues_ix]
                    if clues_ix.index(ix) == 1: #COLUMN
                        down_or_up = lambda y: (y,1) if y < 4 else (y%4,-1)
                        col = [num for num in range(1,5)] [::down_or_up(key)[1]] #use key, OUTCOME IX
                        outcome[:, down_or_up(key)[0]] = col
                    else: # == 0 ROW
                        right_or_left = lambda x: (x//4,-1) if x < 8 else (abs(x - int((4**2)-1)),1)
                        row = [num for num in range(1,5)] [::right_or_left(ix)[1]] #use ix, CLUES IX
                        outcome[right_or_left(ix)[0]] = row
    return outcome
clues = (
( 4, 2, 1, 3,  
  2, 2, 3, 1,  
  1, 2, 2, 3,  
  3, 2, 1, 3 ),
( 0, 0, 1, 2,   
  0, 2, 0, 0,   
  0, 3, 0, 0, 
  0, 1, 0, 0 )
)
print(solve_puzzle(list(clues[0])))
#print(*list(chunks(solve_puzzle(list(clues[0])),4)),sep="\n")




outcomes = (
( ( 1, 3, 4, 2 ),       
  ( 4, 2, 1, 3 ),       
  ( 3, 4, 2, 1 ),
  ( 2, 1, 3, 4 ) ),

( ( 2, 1, 4, 3 ), 
  ( 3, 4, 1, 2 ), 
  ( 4, 2, 3, 1 ), 
  ( 1, 3, 2, 4 ) )
)