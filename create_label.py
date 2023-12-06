from PIL import Image, ImageDraw
from tools.control import Main
from tools.input import input_text, input_choice, input_file
from tools.paste import paste_line, paste_image, paste_on_grid

def create_single_label(name: str = None) -> (Image, str):
  if name is None:
    name = input_text('Введите имя навыка:')

  label = Image.new('RGBA', (400, 100))

  draw = ImageDraw.Draw(label)
  draw.rectangle((0, 0, 399, 99), outline=(0, 0, 0))

  label = paste_line(label, name, (15, 15, 385, 85),
                     font_path='default/font.ttf', font_size=85)

  return (label, name)


def create_single_grid():
  label, name = create_single_label()

  grid = paste_on_grid((2480, 3508), label)

  grid.save(f'result/Наклейка {name}.png')

  label.close()
  grid.close()


def create_set_grid():
  set_name = input_text('Введите имя набора наклеек:')

  set_grid = Image.new('RGBA', (2480, 3508))

  box_table = [
    (0, 0, 1200, 1100),
    (1200, 0, 2400, 1100),
    (0, 1100, 1200, 2200),
    (1200, 1100, 2400, 2200),
    (0, 2200, 1200, 3300),
    (1200, 2200, 2400, 3300)
  ]

  for i, name in enumerate(input_file('files/labels.txt', 6)[:6]):
    label, _ = create_single_label(name)
    
    grid = paste_on_grid((1200, 1100), label)
    
    set_grid = paste_image(set_grid, grid, box_table[i])

    label.close()
    grid.close()

  set_grid.save(f'result/Набор наклеек {set_name}.png')

  set_grid.close()


@Main
def create_label():
  choice = input_choice('Выберите режим:',
                        single='Одна наклейка',
                        multiple='Набор наклеек')

  match choice:
    case 'single':
      create_single_grid()
    case 'multiple':
      create_set_grid()

