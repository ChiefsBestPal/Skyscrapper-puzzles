from PIL import Image, ImageDraw, ImageFont


def unFlatten(arr, n):
	for i in range(0, len(arr), n):
		yield arr[i: i+n]

#!out.show()
# with open('file_path', 'w') as file: 
#     file.write('hello world !')
cell_width,cell_height = 300,100 
Board_Size = 4
out = Image.new("RGB", (cell_width * Board_Size, cell_height * Board_Size), (255, 255, 255))
width,height = out.size[0],out.size[1]
fnt = ImageFont.truetype("C:/Users/Antoine/Desktop/Coding+/Animation/AntenderHandwriting-Regular-Final1.ttf", 40)
d = ImageDraw.Draw(out)
margin = 100
corners_img = [0,0,width,0,0,height,width,height]
corners_board = list(map((lambda x: x+margin if x == 0 else x-margin),corners_img))
p1,p2,p3,p4 = list(unFlatten(corners_board,2))

print(corners_board)
d.line(p1 + p2,fill=000)
d.line(p1 + p3,fill=000)
d.line(p3 + p4,fill=000)
d.line(p2 + p4,fill=000)
print(out.size)

for i in range(1,Board_Size):
    sep1,sep2 = [(p[0],p[1]+(cell_height*i)) for p in [p1,p2]]
	print(sep1,sep2)
	d.line(sep1+sep2,fill=111)

#d.multiline_text((10,10), "Hello\nWorld", font=fnt, fill=(0, 0, 0))

out.show()