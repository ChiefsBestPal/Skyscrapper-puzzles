import numpy as np
import itertools as it
def chunks(arr, n):
	for i in range(0, len(arr), n):
		yield arr[i: i+n]
from collections import Counter,OrderedDict

def duplicate(Input,parameter="row"):
	if parameter == "col":
		Input = np.array(Input)
		Input = [list(Input[:,n]) for n in range(len(Input))]
		Input = map(tuple,Input)
	else:
		Input = map(tuple,Input)
	freqDict = Counter(Input)

	dupes = []
	#!print(freqDict.items())
	for (row,freq) in freqDict.items():
		if freq>1:
			dupes.append(row)
	return bool(dupes)
def verify(Input):
	return bool(list(filter(None,(duplicate(Input),duplicate(Input,"col")))))

Indices = {0 : (0,15) , #?Indices of clues (clue VALUES) associated with appropriate index of, outcome (outcome KEYS)
			1 : (1,None) , #not using fromkeys(), specific values and prevents from using set.add() (always max 2 values(corners))
			2 : (2,None) ,
			3 : (3,4) ,
			4 : (14,None) ,
			7 : (5,None) ,
			8 : (13,None) ,
			11: (6,None) ,
			12: (11,12) ,
			13: (10,None) ,
			14: (9,None) ,
			15: (7,8) }

inv_Indices = {value:key for key, value in Indices.items()}
#?inv_Indices = dict(zip(inv_Indices, map(tuple, inv_Indices.values())))
#! Pseudo Bisection search possible ?

clues = (
  0, 0, 1, 2,
  0, 2, 0, 0,
  0, 3, 0, 0,
  0, 1, 0, 0
)


outcome = [0,0,0,0] * 4
S = np.array(list(chunks(outcome,4)))

#comb = it.combinations(range(1,4),3)
#! FOR PRACTICE
raw_poss = list(it.product(range(1,5),range(1,5),repeat=2))
raw_poss = map(list,raw_poss)
predicate = lambda poss: list(dict.fromkeys(poss)) != poss 
poss = list(it.filterfalse(predicate, raw_poss))

#!FLATTEN d2 = {k: list(it.chain(*v)) for k, v in dic.items()}

#clue_one = first is 4
#clue_four = col or row is 1,2,3,4

def num_clue(poss):
	i = poss
	count = 0
	while len(i) > 0:
		count += 1
		i = list(filter(lambda x: x > i[0],i))
	return count

poss_with_clues = [(num_clue(i),i) for i in poss] #?config with clue num tuples
dic = {}
for a,b in poss_with_clues: #?key value pairs
	dic.setdefault(a,[]).append(b)

dic_of_poss = {c+1:dic[i] for c,i in enumerate(sorted(dic.keys(), reverse=False))} #?reverse key value pairs order



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


S = solve_puzzle(list(clues)) #AUTOMATIC PLACEMENT FOR CLUE1 AND CLUE4
S = list(it.chain(*S)) #FLATTEN


printS = lambda S: np.array(list(chunks(S,4)))#!affichage seulement
#! C is for test matrix, ix is for actually filling up the grid       REDUCE THIS GRID AFTERWARDS

#col
C0,ix0 = [S[0],S[4],S[8],S[12]],[0,4,8,12]
C1,ix1 = [S[1],S[5],S[9],S[13]],[1,5,9,13]
C2,ix2 = [S[2],S[6],S[10],S[14]],[2,6,10,14]
C3,ix3 = [S[3],S[7],S[11],S[15]],[3,7,11,15]
#row
C12,ix12 = [S[12],S[13],S[14],S[15]],[12,13,14,15]
C13,ix13 = [S[8],S[9],S[10],S[11]],[8,9,10,11]
C14,ix14 = [S[4],S[5],S[6],S[7]],[4,5,6,7]
C15,ix15 = [S[0],S[1],S[2],S[3]],[0,1,2,3]
#reverse_col
C8,ix8 = C3[::-1],list(reversed(ix3))
C9,ix9 = C2[::-1],list(reversed(ix2))
C10,ix10 = C1[::-1],list(reversed(ix1))
C11,ix11 = C0[::-1],list(reversed(ix0))
#reverse_row
C4,ix4 = C15[::-1],list(reversed(ix15))
C5,ix5 = C14[::-1],list(reversed(ix14))
C6,ix6 = C13[::-1],list(reversed(ix13))
C7,ix7 = C12[::-1],list(reversed(ix12))

all_segment_indexes = [ix0,ix1,ix2,ix3,ix4,ix5,ix6,ix7,ix8,ix9,ix10,ix11,ix12,ix13,ix14,ix15]
print(dic_of_poss)

#!VERIFY(INPUT) NE DOIT PAS ETRE TRUE
for ix_C,C in enumerate(clues):
	if C in (0,4):
		pass
	else:
		segment_indexes = all_segment_indexes[ix_C] #"ix??""
		all_segment_poss = dic_of_poss[C]#C is used as key here

		print(all_segment_poss)
		print(segment_indexes)
		for segment_pos in all_segment_poss: #exemple: for [1,2,3,4] in dic_of_poss[4]
			for ix_poss,indexes in enumerate(segment_indexes):
				S[indexes] = segment_pos[ix_poss]
				print(S)
				print(printS(S))
			exit()
	






Input  = [[3, 2, 3, 1, 0, 1],
			[1, 0, 1, 0, 0, 1],
			[3, 0, 3, 1, 0, 0],
			[1, 2, 1, 4, 0, 1],
			[0, 0, 0, 0, 0, 1],
			[0, 1, 0, 0, 0, 1]]
#print(verify(Input))