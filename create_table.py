from csv import reader
from PIL import Image
from tools.paste import paste_image, paste_line, paste_text
from tools.input import input_text
from tools.control import Main

def create_cell(text: str) -> Image:
  cell = Image.new('RGBA', (700, 550))

  template = Image.open('default/template_cell.png')
  cell = paste_image(cell, template, (0, 0, 700, 550))
  template.close()

  lines = text.replace('\\n', '\n').split('\n')
  ability_name = lines[0]
  ability_text = lines[1:]

  cell = paste_line(cell, ability_name, (100, 80, 600, 160),
                    font_path='default/font.ttf', font_size=80)

  cell = paste_text(cell, ability_text, (100, 210, 600, 480),
                    font_path='default/font.ttf', font_size=40)

  return cell


def create_row(texts: list[str], level: str) -> Image:
  row = Image.new('RGBA', (2300, 1250))

  row = paste_line(row, level, (1030, 0, 1270, 120),
                   font_path='default/font.ttf', font_size=120)

  match len(texts):
    case 1:
      row = paste_image(row, create_cell(texts[0]), (800, 150, 1500, 700))
    case 2:
      row = paste_image(row, create_cell(texts[0]), (450, 150, 1150, 700))
      row = paste_image(row, create_cell(texts[1]), (1150, 150, 1850, 700))
    case 3:
      row = paste_image(row, create_cell(texts[0]), (100, 150, 800, 700))
      row = paste_image(row, create_cell(texts[1]), (800, 150, 1500, 700))
      row = paste_image(row, create_cell(texts[2]), (1500, 150, 2200, 700))
    case 4:
      row = paste_image(row, create_cell(texts[0]), (450, 150, 1150, 700))
      row = paste_image(row, create_cell(texts[1]), (1150, 150, 1850, 700))
      row = paste_image(row, create_cell(texts[2]), (450, 700, 1150, 1250))
      row = paste_image(row, create_cell(texts[3]), (1150, 700, 1850, 1250))
    case 5:
      row = paste_image(row, create_cell(texts[0]), (100, 150, 800, 700))
      row = paste_image(row, create_cell(texts[1]), (800, 150, 1500, 700))
      row = paste_image(row, create_cell(texts[2]), (1500, 150, 2200, 700))
      row = paste_image(row, create_cell(texts[3]), (450, 700, 1150, 1250))
      row = paste_image(row, create_cell(texts[4]), (1150, 700, 1850, 1250))

  return row


@Main
def create_table():
  Image.MAX_IMAGE_PIXELS = None
  table = Image.new('RGBA', (2480, 3508))

  template = Image.open('default/template_table.png')
  table = paste_image(table, template, (0, 0, 2480, 3508))
  template.close()

  location_name = input_text('Введите название локации:')
  table = paste_line(table, location_name, (390, 150, 2090, 400),
                     font_path='default/font.ttf', font_size=225)
  
  with open('files/table.csv', 'r', encoding='utf-8') as f:
    rows = list(reader(f, delimiter='|'))

  levels = rows[0]
  texts = rows[1]
  
  texts_1 = [text for i, text in enumerate(texts) if text != '' and levels[i] == 'I']
  row_1 = create_row(texts_1, 'I')
  table = paste_image(table, row_1, (90, 450, 2390, 1700))
  row_1.close()

  texts_2 = [text for i, text in enumerate(texts) if text != '' and levels[i] == 'II']
  row_2 = create_row(texts_2, 'II')
  table = paste_image(table, row_2, (90, 1250, 2390, 2500))
  row_2.close()

  texts_3 = [text for i, text in enumerate(texts) if text != '' and levels[i] == 'III']
  row_3 = create_row(texts_3, 'III')
  table = paste_image(table, row_3, (90, 2050, 2390, 3300))
  row_3.close()
  
  table.save(f'result/Таблица {location_name}.png')
  table.close()
