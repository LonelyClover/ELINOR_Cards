from traceback import print_exc

class Main:
  def __init__(self, func):
    self.func = func
    self.func()

  def __call__(self):
    try:
      self.func()
    except:
      print('Exception occured:')
      print_exc()
      input('Press the ENTER key to continue...')
