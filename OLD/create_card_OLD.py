from PIL import Image, ImageDraw, ImageFont
from os.path import isfile
from os import remove

### Варианты шаблона ###
TEMPLATES = {"Вертикальный": "vertical", "Горизонтальный": "horizontal"}
### ################ ###

### Размеры вставок ###
HEADER_WIDTH      = 70
HEADER_MARGIN     = 14
HEADER_LENGTH     = 400

TEXT_MARGIN       = 140
TEXT_MARGIN_SHIFT = 80
### ############### ###

### Размеры шрифта ###
START_HEADER_FONT_SIZE = 50
START_TEXT_FONT_SIZE   = 30
### ############# ###

### Размеры карты ###
CARD_W = 750
CARD_H = 1050
### ############# ###

### Размеры A4 ###
A4_W = 2480
A4_H = 3508
### ########## ###

### Отступы ###
HORIZONTAL_MARGIN = (A4_W - 3*CARD_W)//4
VERTICAL_MARGIN   = (A4_H - 3*CARD_H)//4
### ####### ###

### Варианты сохранения ###
SAVE_MODES = ["Одиночная карточка", "Сетка для печати"]
### ################### ###

### Выбор шаблона ###

print("Выберите шаблон:")
for no, tem in enumerate(TEMPLATES.keys()):
    print(f"{no + 1}\t{tem}")
template_type = list(TEMPLATES.values())[int(input()) - 1]

try:
    template = Image.open(f"files/template_{template_type}.png")
except FileNotFoundError:
    template = Image.open(f"default/template_{template_type}.png")

template.convert("RGBA")
W, H = template.size

card = Image.new("RGBA", (W, H))


### Изображения ###

# Добавление изображения

if template_type == "vertical":
    try:
        image = Image.open("files/image.png")
    except FileNotFoundError:
        image = Image.open("default/image.png")

    image = image.resize((W, W))
    image = image.convert("RGBA")
    paste_center = H//4 +(HEADER_WIDTH + 2*HEADER_MARGIN)//2 # 1050/4 + 49 = 311,5 ~= 310
    image = image.crop((0, W//2 - paste_center, # 0, 65
                W, W//2 + H//2 - paste_center)) # 750, 
    card.paste(image, (0, 0))
    image.close()

# Добавление шаблона

card = Image.alpha_composite(card, template)
template.close()

# Добавление символа

try:
    symbol = Image.open("files/symbol.png")
except FileNotFoundError:
    symbol = Image.open("default/symbol.png")

symbol = symbol.resize((HEADER_WIDTH, HEADER_WIDTH))
symbol = symbol.convert("RGBA")

symbol_paster = Image.new("RGBA", (W, H), (255, 255, 255, 0))
symbol_paster.paste(symbol, (W-HEADER_WIDTH-HEADER_MARGIN, (H-HEADER_WIDTH)//2))

card = Image.alpha_composite(card, symbol_paster)
symbol_paster.close()


### Тексты ###

draw = ImageDraw.Draw(card)

font_path = "files/font.ttf"
if not isfile(font_path):
    font_path = "default/font.ttf"

def include(box1, box2):
   l1, t1, r1, b1 = box1
   l2, t2, r2, b2 = box2
   return l1 <= l2 and t1 <= t2 and r1 >= r2 and b1 >= b2

def add_header(text, border, x, y):
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
              fill=(0, 0, 0),
              anchor="mm",
              align="center")

def add_text(lines, border, x, y):
    box = map(lambda x: x+1, border)
    font_size = START_TEXT_FONT_SIZE + 1
    text = ""

    while not include(border, box) and font_size > 1:
        font_size -= 1
        font = ImageFont.truetype(font_path, font_size, encoding="UTF-8")

        text = ""
        for line in lines:
            for word in line.split(' '):
                box = draw.multiline_textbbox((x, y),
                                              text + ' ' + word,
                                              font=font,
                                              anchor="mm",
                                              align="left")
                
                if include(border, box):
                    if text != "" and text[-1] != '\n':
                        text += ' '
                else:
                    text += '\n'
                text += word

        box = draw.multiline_textbbox((x, y),
                                      text,
                                      font=font,
                                      anchor="mm",
                                      align="left")

    font = ImageFont.truetype(font_path, font_size, encoding="UTF-8")
    draw.multiline_text((x, y),
                        text,
                        font=font,
                        fill=(0, 0, 0),
                        anchor="mm",
                        align="left")

# Чтение текстов

try:
    f = open("files/text.txt", "r", encoding="UTF-8")
except FileNotFoundError:
    f = open("default/text.txt", "r", encoding="UTF-8")

lines = f.readlines()
f.close()

assert len(lines) >= 4, "В текстовом файле должно быть не менее четырех строк"

name = lines[0].strip()
kind = lines[1].strip()
cost = lines[2].strip()
text_lines = lines[3:]

# Название

border = ((W-HEADER_LENGTH)//2, HEADER_MARGIN,
          (W+HEADER_LENGTH)//2, HEADER_MARGIN+HEADER_WIDTH)
add_header(name, border, W//2, HEADER_MARGIN+HEADER_WIDTH//2)

# Тип

border = ((W-HEADER_LENGTH)//2, H-HEADER_WIDTH-HEADER_MARGIN,
          (W+HEADER_LENGTH)//2, H-HEADER_MARGIN)
add_header(kind, border, W//2, H-HEADER_MARGIN-HEADER_WIDTH//2)

# Стоимость

border = (HEADER_MARGIN, (H-HEADER_WIDTH)//2,
          HEADER_MARGIN+HEADER_WIDTH, (H+HEADER_WIDTH)//2)
add_header(cost, border, HEADER_MARGIN+HEADER_WIDTH//2, H//2)

# Текст

border = (TEXT_MARGIN, TEXT_MARGIN,
          W-TEXT_MARGIN, H-TEXT_MARGIN)
x = W//2
y = H//2
if template_type == "vertical":
    border = (TEXT_MARGIN-TEXT_MARGIN_SHIFT//2, H//2+TEXT_MARGIN_SHIFT,
              W-TEXT_MARGIN+TEXT_MARGIN_SHIFT//2, H-TEXT_MARGIN)
    y = (3*H)//4+(TEXT_MARGIN_SHIFT-TEXT_MARGIN)//2

add_text(text_lines, border, x, y)


### Сетка ###

# Подгонка карты

ready_card = Image.new("RGBA", (CARD_W, CARD_H))

if template_type == "horizontal":
    ready_card = ready_card.resize((CARD_H, CARD_H))
    card = card.resize((CARD_H, CARD_W))
    ready_card.paste(card,
                     (0, (CARD_H-CARD_W)//2))
    ready_card = ready_card.rotate(90).crop(((CARD_H-CARD_W)//2, 0,
                             CARD_H-(CARD_H-CARD_W)//2, CARD_H))
else:
    ready_card = card.resize((CARD_W, CARD_H))

card.close()

# Создание сетки

grid = Image.new("RGBA", (A4_W, A4_H), (255, 255, 255))

for x in range(HORIZONTAL_MARGIN, A4_W, CARD_W+HORIZONTAL_MARGIN):
    for y in range(VERTICAL_MARGIN, A4_H, CARD_H+VERTICAL_MARGIN):
        grid.paste(ready_card, (x, y))

### Сохранение ###

print("Выберите результат:")
for no, mode in enumerate(SAVE_MODES):
    print(f"{no + 1}\t{mode}")
save_mode = SAVE_MODES[int(input()) - 1]

if save_mode == "Одиночная карточка":
    filename = f"result/{name}.png"
    if isfile(filename):
        remove(filename)
        
    ready_card.save(filename)
else:
    filename = f"result/{name} ПЕЧАТЬ.png"
    if isfile(filename):
        remove(filename)
    grid.save(filename)

ready_card.close()
grid.close()

