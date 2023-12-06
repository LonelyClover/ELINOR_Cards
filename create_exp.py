from PIL import Image
from tools.control import Main
from tools.input import input_text
from tools.paste import paste_image, paste_line, paste_on_grid

@Main
def create_exp():
  name = input_text("Введите название локации:")
  
  cost = input_text("Введите стоимость:")

  exp = Image.new('RGBA', (350, 350))

  with Image.open('default/ring.png') as ring:
    exp = paste_image(exp, ring, (0, 0, 350, 350))

  exp = paste_line(exp, cost, (70, 70, 280, 280),
                   font_path='default/font.ttf', font_size=250,
                   fill=(200, 200, 200))
  
  exp = paste_line(exp, name, (40, 100, 310, 250),
                   font_path='default/font.ttf', font_size=180)
  
  grid = paste_on_grid((2480, 3508), exp)
  
  grid.save(f'result/Опыт {name} {cost}.png')
  
  exp.close()
  grid.close()
