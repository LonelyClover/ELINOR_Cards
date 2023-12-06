from typing import TypeVar, Generator

def input_text(message: str) -> str:
  print(message)
  return input()


T = TypeVar('T')
def input_choice(message: str, **variants) -> T:
  print(message)
  
  for no, var in enumerate(variants.values()):
    print(f'{no + 1}\t{var}')
  
  return list(variants.keys())[int(input()) - 1]

def input_file(filepath: str, n: int) -> list[str]:
  with open(filepath, 'r') as f:
    lines = f.readlines()

  assert len(lines) >= n, f'Файл {filepath} должен содержать хотя бы {n} строк'
  
  return list(map(lambda s: s.strip(), lines))
