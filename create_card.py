from PIL import Image
from tools.control import Main
from tools.input import input_choice, input_file
from tools.paste import paste_image, paste_line, paste_text, paste_on_grid

def create_vertical_card() -> (Image, str):
  card = Image.new('RGBA', (750, 1050))

  image = Image.open('files/image.png')
  card = paste_image(card, image, (0, -65, 750, 685))
  image.close()

  image = Image.open('default/template_vertical.png')
  card = paste_image(card, image, (0, 0, 750, 1050))
  image.close()

  symbol = Image.open('files/symbol.png')
  card = paste_image(card, symbol, (680-14, 490, 750-14, 560))
  symbol.close()

  lines = input_file('files/card.txt', 4)
  name = lines[0]
  kind = lines[1]
  cost = lines[2]
  text = lines[3:]

  card = paste_line(card, name, (175, 0+14, 575, 70+14),
                    font_path='default/font.ttf', font_size=50)

  card = paste_line(card, kind, (175, 980-14, 575, 1050-14),
                    font_path='default/font.ttf', font_size=50)

  card = paste_line(card, cost, (0+14, 490, 70+14, 560),
                    font_path='default/font.ttf', font_size=50)

  card = paste_text(card, text, (100, 565, 650, 970),
                    font_path='default/font.ttf', font_size=30)

  return card, name


def create_horizontal_card() -> (Image, str):
  card = Image.new('RGBA', (1050, 750))

  image = Image.open('default/template_horizontal.png')
  card = paste_image(card, image, (0, 0, 1050, 750))
  image.close()

  symbol = Image.open('files/symbol.png')
  card = paste_image(card, symbol, (980-14, 340, 1050-14, 410))
  symbol.close()

  lines = input_file('files/card.txt', 4)
  name = lines[0]
  kind = lines[1]
  cost = lines[2]
  text = lines[3:]

  card = paste_line(card, name, (325, 0+14, 725, 70+14),
                    font_path='default/font.ttf', font_size=50)

  card = paste_line(card, kind, (325, 680-14, 725, 750-14),
                    font_path='default/font.ttf', font_size=50)

  card = paste_line(card, cost, (0+14, 340, 70+14, 410),
                    font_path='default/font.ttf', font_size=50)

  card = paste_text(card, text, (140, 140, 910, 610),
                    font_path='default/font.ttf', font_size=30)

  return card, name


@Main
def create_card():
  template = input_choice('Выберите шаблон:',
                          vertical='Вертикальный',
                          horizontal='Горизонтальный')

  match template:
    case 'vertical':
      card, name = create_vertical_card()

    case 'horizontal':
      card, name = create_horizontal_card()
      card = card.rotate(90, expand=True)

  save_mode = input_choice('Выберите результат:',
                           single='Одиночная карточка',
                           grid='Сетка для печати')

  match save_mode:
    case 'single':
      card.save(f'result/{name}.png')
      card.close()

    case 'grid':
      grid = paste_on_grid((2480, 3508), card)
      grid.save(f'result/{name} ПЕЧАТЬ.png')
      grid.close()
      card.close()
