from PIL import Image, ImageDraw, ImageFont
from os.path import isfile
from os import remove

### Размеры наклейки ###
LABEL_W = 400
LABEL_H = 100

MARGIN = 10
### ################ ###

### Размеры шрифта ###
START_HEADER_FONT_SIZE = 80
### ############# ###

### Размеры A4 ###
A4_W = 2480
A4_H = 3508
### ########## ###

print("Введите имя навыка:")
name = input()

label = Image.new("RGBA", (LABEL_W, LABEL_H))

draw = ImageDraw.Draw(label)

font_path = "files/font.ttf"
if not isfile(font_path):
    font_path = "default/font.ttf"

def include(box1, box2):
   l1, t1, r1, b1 = box1
   l2, t2, r2, b2 = box2
   return l1 <= l2 and t1 <= t2 and r1 >= r2 and b1 >= b2

def add_header(text, border, x, y, fill=(0, 0, 0)):
    box = map(lambda x: x+1, border)
    font_size = START_HEADER_FONT_SIZE + 1
    
    while not include(border, box) and font_size > 1:
        font_size -= 1
        font = ImageFont.truetype(font_path, font_size, encoding="UTF-8")
        box = draw.textbbox((x, y),
                            text,
                            font=font,
                            anchor="mm",
                            align="center")

    font = ImageFont.truetype(font_path, font_size, encoding="UTF-8")
    draw.text((x, y),
              text,
              font=font,
              fill=fill,
              anchor="mm",
              align="center")


size = (0, 0, LABEL_W-1, LABEL_H-1)
draw.rectangle(size, fill=(255, 255, 255), outline=(0, 0, 0))

border = (MARGIN, MARGIN, LABEL_W-MARGIN, LABEL_H-MARGIN)
add_header(name, border, LABEL_W//2, LABEL_H//2)

grid = Image.new("RGBA", (A4_W, A4_H))

for x in range(0, A4_W, LABEL_W):
    for y in range(0, A4_H, LABEL_H):
        grid.paste(label, (x, y))

label.close()

filename = f"result/Наклейка {name}.png"
if isfile(filename):
    remove(filename)

grid.save(filename)
grid.close()

