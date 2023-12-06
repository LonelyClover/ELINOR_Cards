from PIL import Image, ImageDraw, ImageFont
from os.path import isfile
from os import remove

### Размеры опыта ###
EXP_W = 350
EXP_H = 350

COST_MARGIN = 70
NAME_HORIZONTAL_MARGIN = 40
NAME_VERTICAL_MARGIN = 100
### ############# ###

### Размеры шрифта ###
START_HEADER_FONT_SIZE = 300
START_TEXT_FONT_SIZE   = 50
### ############# ###

### Размеры A4 ###
A4_W = 2480
A4_H = 3508
### ########## ###

### Отступы ###
HORIZONTAL_MARGIN = (A4_W - 7*EXP_W)//8
VERTICAL_MARGIN   = (A4_H - 10*EXP_H)//9
### ####### ###

print("Введите название локации:")
name = input()

print("Введите стоимость:")
cost = input()

exp = Image.new("RGBA", (EXP_W, EXP_H))

try:
    ring = Image.open("files/exp.png")
except FileNotFoundError:
    ring = Image.open("default/exp.png")

ring = ring.resize((EXP_W, EXP_H))
ring = ring.convert("RGBA")

exp = Image.alpha_composite(exp, ring)
ring.close()

draw = ImageDraw.Draw(exp)

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


border = (COST_MARGIN, COST_MARGIN,
          EXP_W-COST_MARGIN, EXP_H-COST_MARGIN)
add_header(cost, border, EXP_W//2, EXP_H//2, fill=(200, 200, 200))

border = (NAME_HORIZONTAL_MARGIN, NAME_VERTICAL_MARGIN,
          EXP_W-NAME_HORIZONTAL_MARGIN, EXP_H-NAME_VERTICAL_MARGIN)
add_header(name, border, EXP_W//2, EXP_H//2)

grid = Image.new("RGBA", (A4_W, A4_H))

for x in range(HORIZONTAL_MARGIN, A4_W, EXP_W+HORIZONTAL_MARGIN):
    for y in range(VERTICAL_MARGIN, A4_H, EXP_H+VERTICAL_MARGIN):
        grid.paste(exp, (x, y))

exp.close()

filename = f"result/Опыт {name} {cost}.png"
if isfile(filename):
    remove(filename)
    
grid.save(filename)
grid.close()
