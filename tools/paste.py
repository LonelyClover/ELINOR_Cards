from dataclasses import dataclass
from PIL import Image, ImageDraw, ImageFont

@dataclass
class Box:
  x1: int
  y1: int
  x2: int
  y2: int

  def size(self) -> (int, int):
    return (self.x2 - self.x1, self.y2 - self.y1)
  
  def center(self) -> (int, int):
    return ((self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2)

  def contains(self, other) -> bool:
    return self.x1 <= other.x1 and \
           self.y1 <= other.y1 and \
           self.x2 >= other.x2 and \
           self.y2 >= other.y2


def paste_image(background: Image, image: Image, box: (int, int, int, int)) -> Image:
  box = Box(*box)

  image = image.convert('RGBA')
  image = image.resize(box.size())

  image_paster = Image.new('RGBA', background.size)
  image_paster.paste(image, (box.x1, box.y1))

  background = Image.alpha_composite(background, image_paster)
  image_paster.close()

  return background


def paste_line(background: Image, line: str, box: (int, int, int, int), *, font_path: str, font_size: int, fill: (int, int, int) = (0, 0, 0)) -> Image:
  box = Box(*box)

  draw = ImageDraw.Draw(background)
  current_box = Box(box.x1 + 1, box.y1 + 1, box.x2 + 1, box.y2 + 1)
  font_size += 1

  while not box.contains(current_box) and font_size > 1:
    font_size -= 1
    font = ImageFont.truetype(font_path, font_size, encoding='UTF-8')
    current_box = Box(*draw.textbbox(box.center(), line, font=font, anchor='mm', align='center'))

  font = ImageFont.truetype(font_path, font_size, encoding='UTF-8')
  draw.text(box.center(), line, font=font, fill=fill, anchor='mm', align='center')
 
  return background


def paste_text(background: Image, lines: list[str], box: (int, int, int, int), *, font_path: str, font_size: int, fill: (int, int, int) = (0, 0, 0)) -> Image:
  box = Box(*box)

  draw = ImageDraw.Draw(background)
  current_box = Box(box.x1 + 1, box.y1 + 1, box.x2 + 1, box.y2 + 1)
  font_size += 1
  text = ''

  while not box.contains(current_box) and font_size > 1:
    font_size -= 1
    font = ImageFont.truetype(font_path, font_size, encoding="UTF-8")
    text = ''

    for line in lines:
      line += '\n'

      for word in line.split(' '):
        current_box = Box(*draw.multiline_textbbox(box.center(), text + ' ' + word, font=font, anchor="mm", align="left"))

        if not box.contains(current_box):
          text += '\n'
        elif text != '' and text[-1] != '\n':
          text += ' '
        
        text += word

  current_box = Box(*draw.multiline_textbbox(box.center(), text, font=font, anchor="mm", align="left"))

  font = ImageFont.truetype(font_path, font_size, encoding="UTF-8")
  draw.multiline_text(box.center(), text, font=font, fill=fill, anchor="mm", align="left")
  
  return background


def paste_on_grid(grid_size: (int, int), image: Image, *, margin: int = 0):
  grid = Image.new('RGBA', grid_size)

  x = 0

  while x <= grid_size[0] - image.size[0]:
    y = 0

    while y <= grid_size[1] - image.size[1]:
      grid.paste(image, (x, y))
      y += image.size[1] + margin

    x += image.size[0] + margin

  return grid
