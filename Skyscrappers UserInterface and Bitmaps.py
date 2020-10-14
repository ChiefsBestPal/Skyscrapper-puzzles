from PIL import Image, ImageDraw, ImageFont

clues = (
  0, 0, 0, 2, 2,0,
  0, 0, 0, 6,3,0,
  0, 4, 0, 0,0,0,
  4, 4, 0, 3,0,0
)

deffnt = ImageFont.truetype("C:/Users/Antoine/Desktop/Coding+/Animation/arial.ttf", 40)

def unFlatten(arr, n):
	for i in range(0, len(arr), n):
		yield arr[i: i+n]

#!out.show()
# with open('file_path', 'w') as file: 
#     file.write('hello world !')
Board_Size = 6 #?input("Enter N for a NxN Skyscrapper")
cell_width,cell_height = 300,100 
out = Image.new("RGB", (cell_width * Board_Size, cell_height * Board_Size), (255, 255, 255))
width,height = out.size[0],out.size[1]
AntEnderfnt = ImageFont.truetype("C:/Users/Antoine/Desktop/Coding+/Animation/AntenderHandwriting-Regular-Final1.ttf", 40)
d = ImageDraw.Draw(out)
margin = 50
corners_img = [0,0,width,0,0,height,width,height]
corners_board = list(map((lambda x: x+margin if x == 0 else x-margin),corners_img))
p1,p2,p3,p4 = list(map(tuple,unFlatten(corners_board,2)))


print(corners_board)
d.line(p1 + p2,fill=000)
d.line(p1 + p3,fill=000)
d.line(p3 + p4,fill=000)
d.line(p2 + p4,fill=000)

x_dephasage_manuel_estimation_text = deph_x = -13 #x = 37 centers letter X with vertical vertices instead of margin of 50 (default)
y_dephasage_manuel_estimation_text = deph_y = -22

clues_positions = list()
new_cell_height = (height - (2*margin))//Board_Size
new_cell_width = (width - (2*margin))//Board_Size
for c,i in enumerate(range(1,Board_Size+1)):
	middle_text_pos_factor = mt = 1 + (2*c)
	
	sep1,sep2 = [(p[0],p[1]+(new_cell_height*i)) for p in [p1,p2]] #sep horizontales
	sep3,sep4 = [(p[0]+(new_cell_width*i),p[1]) for p in [p1,p3]] #sep verticales

	d.line(sep1+sep2,fill=000)
	d.line(sep3+sep4,fill=000)

	second_margin = margin

	#respect given orders of indexes through 0 to 15 (see Skyscrappers.py)
	clues_positions.append((deph_x + p1[0]+((new_cell_width//2*mt)),
	p1[1]-second_margin))

	clues_positions.append((p2[0]+ second_margin//2 #second_margin//2 because max pixel is weird with letters and wont show unlike the 0th one
	,deph_y + p1[1]+((new_cell_height//2*mt))))

	clues_positions.append((deph_x + p3[0]+((new_cell_width//2*mt)),
	p3[1]+second_margin//2-20)) #second_margin//2 -20 because max pixel is weird with letters and height of letter is often bigger than width

	clues_positions.append((p1[0]-second_margin
	,deph_y + p1[1]+((new_cell_height//2*mt))))
print((clues_positions))

sorted_clue_coords = sorted(clues_positions,key = lambda x: clues_positions.index(x) % 4,reverse=False)

chunk_clue_coords = list(unFlatten(sorted_clue_coords,Board_Size))

final_coords_clues = chunk_clue_coords[0] + chunk_clue_coords[1]+chunk_clue_coords[2][::-1] + chunk_clue_coords[3][::-1]

for ix_clue,clue_position in enumerate(final_coords_clues): #!put in class for object as input
	d.text(clue_position, str(clues[ix_clue]), font=deffnt, fill=(0, 0, 1))

#while

out.show()
#? MADE BY ANT_ENDER FOR SKYSCRAPPER PUZZLES FROM CODEWARS: https://www.codewars.com/kata/5671d975d81d6c1c87000022/train/python
